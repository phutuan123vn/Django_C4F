from django.http.response import HttpResponseBase
from django.middleware.csrf import CsrfViewMiddleware,get_token
from django.conf import settings
from typing import Any, Callable
from django.http import HttpRequest, HttpResponseForbidden

class CSRFCookieMiddleware(CsrfViewMiddleware):
    # def process_response(self, request, response):
    #     request.META[settings.CSRF_HEADER_NAME] = request.COOKIES.get("csrftoken")
    #     response = super().process_response(request, response)
    #     return response
    
    def process_view(self, request: HttpRequest,
                     callback: Callable[..., Any] | None, callback_args: tuple[Any, ...],
                     callback_kwargs: dict[str, Any])\
                         -> HttpResponseForbidden | None:
        request.META[settings.CSRF_HEADER_NAME] = request.COOKIES.get("csrftoken")
        # print("Cookie",request.COOKIES)

        return super().process_view(request, callback, callback_args, callback_kwargs)
    
    def process_response(self, request: HttpRequest, response: HttpResponseBase) -> HttpResponseBase:
        if request.COOKIES.get("csrftoken") is None and 'logout' not in request.path:
            get_token(request)
        return super().process_response(request, response)