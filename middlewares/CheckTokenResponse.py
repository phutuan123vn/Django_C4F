from pprint import pprint
from django.http import HttpRequest, HttpResponse
from django.utils.deprecation import MiddlewareMixin
from utils.Request import TokenCheck
from rest_framework.response import Response

class CheckTokenResponse(MiddlewareMixin):
    
    def process_response(self, request: HttpRequest, response: HttpResponse):
        access_token = TokenCheck(request)
        if access_token is not None:
            if isinstance(response, Response):
                response.data['access_token'] = access_token
                response._is_rendered = False
                response.render()
            # response.content = data
        return response