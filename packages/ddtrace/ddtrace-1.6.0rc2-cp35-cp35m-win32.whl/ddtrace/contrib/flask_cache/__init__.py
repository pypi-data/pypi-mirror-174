"""
The flask cache tracer will track any access to a cache backend.
You can use this tracer together with the Flask tracer middleware.

The tracer supports both `Flask-Cache <https://pythonhosted.org/Flask-Cache/>`_
and `Flask-Caching <https://flask-caching.readthedocs.io/>`_.

To install the tracer, ``from ddtrace import tracer`` needs to be added::

    from ddtrace import tracer
    from ddtrace.contrib.flask_cache import get_traced_cache

and the tracer needs to be initialized::

    Cache = get_traced_cache(tracer, service='my-flask-cache-app')

Here is the end result, in a sample app::

    from flask import Flask

    from ddtrace import tracer
    from ddtrace.contrib.flask_cache import get_traced_cache

    app = Flask(__name__)

    # get the traced Cache class
    Cache = get_traced_cache(tracer, service='my-flask-cache-app')

    # use the Cache as usual with your preferred CACHE_TYPE
    cache = Cache(app, config={'CACHE_TYPE': 'simple'})

    def counter():
        # this access is traced
        conn_counter = cache.get("conn_counter")

Use a specific ``Cache`` implementation with::

    from ddtrace import tracer
    from ddtrace.contrib.flask_cache import get_traced_cache

    from flask_caching import Cache

    Cache = get_traced_cache(tracer, service='my-flask-cache-app', cache_cls=Cache)

"""

from ...internal.utils.importlib import require_modules


required_modules = ["flask_cache", "flask_caching"]

with require_modules(required_modules) as missing_modules:
    if len(missing_modules) < len(required_modules):
        from .tracers import get_traced_cache

        __all__ = ["get_traced_cache"]
