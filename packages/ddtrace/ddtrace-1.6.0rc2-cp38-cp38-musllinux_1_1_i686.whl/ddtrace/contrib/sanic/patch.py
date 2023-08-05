import asyncio

import sanic

import ddtrace
from ddtrace import config
from ddtrace.constants import ANALYTICS_SAMPLE_RATE_KEY
from ddtrace.ext import SpanTypes
from ddtrace.internal.utils.wrappers import unwrap as _u
from ddtrace.pin import Pin
from ddtrace.vendor import wrapt
from ddtrace.vendor.wrapt import wrap_function_wrapper as _w

from .. import trace_utils
from ...internal.logger import get_logger


log = get_logger(__name__)

config._add("sanic", dict(_default_service="sanic", distributed_tracing=True))

SANIC_VERSION = (0, 0, 0)


def _get_current_span(request):
    pin = Pin._find(request.ctx)
    if not pin or not pin.enabled():
        return None

    return pin.tracer.current_span()


def update_span(span, response):
    # Check for response status or headers on the response object
    # DEV: This object can either be a form of BaseResponse or an Exception
    #      if we do not have a status code, we can assume this is an exception
    #      and so use 500
    status_code = getattr(response, "status", 500)
    response_headers = getattr(response, "headers", None)
    trace_utils.set_http_meta(span, config.sanic, status_code=status_code, response_headers=response_headers)


def _wrap_response_callback(span, callback):
    # Only for sanic 20 and older
    # Wrap response callbacks (either sync or async function) to set HTTP
    # response span tags

    @wrapt.function_wrapper
    def wrap_sync(wrapped, instance, args, kwargs):
        r = wrapped(*args, **kwargs)
        response = args[0]
        update_span(span, response)
        return r

    @wrapt.function_wrapper
    async def wrap_async(wrapped, instance, args, kwargs):
        r = await wrapped(*args, **kwargs)
        response = args[0]
        update_span(span, response)
        return r

    if asyncio.iscoroutinefunction(callback):
        return wrap_async(callback)

    return wrap_sync(callback)


async def patch_request_respond(wrapped, instance, args, kwargs):
    # Only for sanic 21 and newer
    # Wrap the framework response to set HTTP response span tags
    response = await wrapped(*args, **kwargs)
    span = _get_current_span(instance)
    if not span:
        return response

    update_span(span, response)

    # Sanic 21.9.x does not dispatch `http.lifecycle.response` in `handle_exception`
    #  so we have to handle finishing the span here instead
    if (21, 9, 0) <= SANIC_VERSION < (21, 12, 0) and getattr(instance.ctx, "__dd_span_call_finish", False):
        span.finish()
    return response


def _get_path(request):
    """Get path and replace path parameter values with names if route exists."""
    path = request.path
    try:
        match_info = request.match_info
    except sanic.exceptions.SanicException:
        return path
    for key, value in match_info.items():
        try:
            value = str(value)
        except Exception:
            # Best effort
            continue
        path = path.replace(value, f"<{key}>")
    return path


async def patch_run_request_middleware(wrapped, instance, args, kwargs):
    # Set span resource from the framework request
    request = args[0]
    span = _get_current_span(request)
    if span is not None:
        span.resource = "{} {}".format(request.method, _get_path(request))
    return await wrapped(*args, **kwargs)


def patch():
    """Patch the instrumented methods."""
    global SANIC_VERSION

    if getattr(sanic, "__datadog_patch", False):
        return
    setattr(sanic, "__datadog_patch", True)

    SANIC_VERSION = tuple(map(int, sanic.__version__.split(".")))

    if SANIC_VERSION >= (21, 9, 0):
        _w("sanic", "Sanic.__init__", patch_sanic_init)
        _w(sanic.request, "Request.respond", patch_request_respond)
    else:
        _w("sanic", "Sanic.handle_request", patch_handle_request)
        if SANIC_VERSION >= (21, 0, 0):
            _w("sanic", "Sanic._run_request_middleware", patch_run_request_middleware)
            _w(sanic.request, "Request.respond", patch_request_respond)


def unpatch():
    """Unpatch the instrumented methods."""
    if not getattr(sanic, "__datadog_patch", False):
        return

    if SANIC_VERSION >= (21, 9, 0):
        _u(sanic.Sanic, "__init__")
        _u(sanic.request.Request, "respond")
    else:
        _u(sanic.Sanic, "handle_request")
        if SANIC_VERSION >= (21, 0, 0):
            _u(sanic.Sanic, "_run_request_middleware")
            _u(sanic.request.Request, "respond")

    setattr(sanic, "__datadog_patch", False)


def patch_sanic_init(wrapped, instance, args, kwargs):
    """Wrapper for creating sanic apps to automatically add our signal handlers"""
    wrapped(*args, **kwargs)

    instance.add_signal(sanic_http_lifecycle_handle, "http.lifecycle.handle")
    instance.add_signal(sanic_http_routing_after, "http.routing.after")
    instance.add_signal(sanic_http_lifecycle_exception, "http.lifecycle.exception")
    instance.add_signal(sanic_http_lifecycle_response, "http.lifecycle.response")


async def patch_handle_request(wrapped, instance, args, kwargs):
    """Wrapper for Sanic.handle_request"""

    def unwrap(request, write_callback=None, stream_callback=None, **kwargs):
        return request, write_callback, stream_callback, kwargs

    request, write_callback, stream_callback, new_kwargs = unwrap(*args, **kwargs)

    if request.scheme not in ("http", "https"):
        return await wrapped(*args, **kwargs)

    with _create_sanic_request_span(request) as span:
        if write_callback is not None:
            new_kwargs["write_callback"] = _wrap_response_callback(span, write_callback)
        if stream_callback is not None:
            new_kwargs["stream_callback"] = _wrap_response_callback(span, stream_callback)

        return await wrapped(request, **new_kwargs)


def _create_sanic_request_span(request):
    """Helper to create sanic.request span and attach a pin to request.ctx"""
    pin = Pin()
    pin.onto(request.ctx)

    if SANIC_VERSION < (21, 0, 0):
        # Set span resource from the framework request
        resource = "{} {}".format(request.method, _get_path(request))
    else:
        # The path is not available anymore in 21.x. Get it from
        # the _run_request_middleware instrumented method.
        resource = None

    headers = request.headers.copy()

    trace_utils.activate_distributed_headers(ddtrace.tracer, int_config=config.sanic, request_headers=headers)

    span = pin.tracer.trace(
        "sanic.request",
        service=trace_utils.int_service(None, config.sanic),
        resource=resource,
        span_type=SpanTypes.WEB,
    )
    sample_rate = config.sanic.get_analytics_sample_rate(use_global_config=True)
    if sample_rate is not None:
        span.set_tag(ANALYTICS_SAMPLE_RATE_KEY, sample_rate)

    method = request.method
    url = "{scheme}://{host}{path}".format(scheme=request.scheme, host=request.host, path=request.path)
    query_string = request.query_string
    if isinstance(query_string, bytes):
        query_string = query_string.decode()
    trace_utils.set_http_meta(span, config.sanic, method=method, url=url, query=query_string, request_headers=headers)

    return span


async def sanic_http_lifecycle_handle(request):
    """Lifecycle signal called when a new request is started."""
    _create_sanic_request_span(request)


async def sanic_http_routing_after(request, route, kwargs, handler):
    """Lifecycle signal called after routing has been resolved."""
    span = _get_current_span(request)
    if not span:
        return

    pattern = route.raw_path
    # Sanic 21.9.0 and newer strip the leading slash from `route.raw_path`
    if not pattern.startswith("/"):
        pattern = "/{}".format(pattern)
    if route.regex:
        pattern = route.pattern

    span.resource = "{} {}".format(request.method, pattern)
    span.set_tag("sanic.route.name", route.name)


async def sanic_http_lifecycle_response(request, response):
    """Lifecycle signal called when a response is starting.

    Note: This signal does not get called when exceptions occur
          in 21.9.x. The issue was resolved in 21.12.x
    """
    span = _get_current_span(request)
    if not span:
        return
    try:
        update_span(span, response)
    finally:
        span.finish()


async def sanic_http_lifecycle_exception(request, exception):
    """Lifecycle signal called when an exception occurs."""
    span = _get_current_span(request)
    if not span:
        return

    # Do not attach exception for exceptions not considered as errors
    # ex: Http 400s
    # DEV: We still need to set `__dd_span_call_finish` below
    if not hasattr(exception, "status_code") or config.http_server.is_error_code(exception.status_code):
        ex_type = type(exception)
        ex_tb = getattr(exception, "__traceback__", None)
        span.set_exc_info(ex_type, exception, ex_tb)

    # Sanic 21.9.x does not dispatch `http.lifecycle.response` in `handle_exception`
    #  so we need to indicate to `patch_request_respond` to finish the span
    if (21, 9, 0) <= SANIC_VERSION < (21, 12, 0):
        request.ctx.__dd_span_call_finish = True
