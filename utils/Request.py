from rest_framework_simplejwt.tokens import RefreshToken
from django.http import HttpRequest

def TokenCheck(request: HttpRequest):
    print(request.auth)
    if not request.auth or request.auth['token_type'] == 'access':
        return None
    refreshTokenClass = RefreshToken(str(request.auth))
    access_token = str(refreshTokenClass.access_token)
    return access_token

