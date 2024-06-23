from pprint import pprint
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from rest_framework import authentication
from rest_framework import exceptions as rest_exceptions
from rest_framework.request import Request
from rest_framework_simplejwt import authentication as jwt_authentication
from rest_framework_simplejwt.settings import api_settings


def enforce_csrf(request):
    check = authentication.CSRFCheck(request)
    reason = check.process_view(request, None, (), {})
    if reason:
      raise rest_exceptions.PermissionDenied('CSRF Failed: %s' % reason)


class CustomAuthentication(jwt_authentication.JWTAuthentication):
    def authenticate(self, request: Request):
        pprint(vars(request))
        header = self.get_header(request)
        if header is None:
            return None
        else:
            refresh_token = request.COOKIES.get(settings.SIMPLE_JWT['AUTH_COOKIE']) or None 
            access_token = self.get_raw_token(header)

        if access_token is None:
            return None
        
        validated_token = self.get_validated_token(access_token,refresh_token)
        
        enforce_csrf(request)
        return self.get_user(validated_token), validated_token
        
    def get_validated_token(self, access_token: bytes, refresh_token: bytes) -> jwt_authentication.Token:
        """
        Validates an encoded JSON web token and returns a validated token
        wrapper object.
        """
        token = [access_token, refresh_token]
        AuthToken = api_settings.AUTH_TOKEN_CLASSES
        if AuthToken[0].token_type == 'access':
            try:
                return AuthToken[0](token[0])
            except jwt_authentication.TokenError as e:
                try:
                    return AuthToken[1](token[1])
                except jwt_authentication.TokenError as e:
                    message = "Token is invalid or expired"
        else:
            try:
                return AuthToken[1](token[0])
            except jwt_authentication.TokenError as e:
                try:
                    return AuthToken[0](token[1])
                except jwt_authentication.TokenError as e:
                    message = "Token is invalid or expired"
                    
        raise jwt_authentication.InvalidToken(
            {
                "detail": _("Given token not valid for any token type"),
                "messages": message,
                "code": "token_not_valid",
            }
        )
