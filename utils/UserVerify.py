from functools import wraps
from typing import Optional
from django.http import HttpRequest, JsonResponse
from django.shortcuts import redirect
from utils import is_ajax


def user_verify(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        request:HttpRequest = args[0]
        auth = request.user.is_authenticated
        ajaxRequest = is_ajax(request)
        if auth:
            return func(*args, **kwargs)
        elif is_ajax(request) and not auth:
            return JsonResponse({"status": "unauthenticated"})
        else:
            return redirect("/account/")
    return wrapper


def RedirectUser(urlPath:Optional[str] = None):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            path = urlPath or "/"
            request:HttpRequest = args[0]
            if request.user.is_authenticated:
                return redirect(path)
            else:
                return func(*args, **kwargs)
        return wrapper
    return decorator
# def RedirectUser(func):
#     @wraps(func)
#     def wrapper(*args, **kwargs):
#         request:HttpRequest = args[0]
#         urlPath = request.path
#         if request.user.is_authenticated:
#             return redirect("/")   
#         else:
#             return func(*args, **kwargs)
#     return wrapper
