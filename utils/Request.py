from pprint import pprint
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import HttpRequest

def TokenCheck(request: HttpRequest):
    if not hasattr(request,'auth'):
        return None
    
    if not request.auth or request.auth['token_type'] == 'access':
        return None
    
    refreshTokenClass = RefreshToken(str(request.auth))
    access_token = str(refreshTokenClass.access_token)
    return access_token

