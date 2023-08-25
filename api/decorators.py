#!/usr/bin/env python
"""Django views for the api application"""

# Imports
from functools import wraps
from django.http import HttpResponseNotAllowed

def http_method_decorator(http_methods):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.method not in http_methods:
                return HttpResponseNotAllowed(http_methods)
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator

def require_get(view_func):
    return http_method_decorator(['GET'])(view_func)

def require_post(view_func):
    return http_method_decorator(['POST'])(view_func)

def require_delete(view_func):
    return http_method_decorator(['DELETE'])(view_func)