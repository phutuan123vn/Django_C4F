from pprint import pprint
from urllib.parse import parse_qs
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.tokens import AccessToken, TokenError, RefreshToken
from channels.sessions import CookieMiddleware, SessionMiddleware

User = get_user_model()


@database_sync_to_async
def get_user(user_id):
    try:
        return User.objects.get(id=user_id)
    except User.DoesNotExist:
        return AnonymousUser()
    

class WebSocketJWTAuthMiddleware:

    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        # parsed_query_string = parse_qs(scope["query_string"])
        # token = parsed_query_string.get(b"token")[0].decode("utf-8")
        # scope = dict(scope)
        # pprint(scope)
        cookies:dict = scope['cookies']
        refresh_token = cookies.get('refresh_token')

        try:
            token = RefreshToken(refresh_token)
            scope["user"] = await get_user(token["user_id"])
            scope['user_id'] = token["user_id"]
        except TokenError:
            # scope["user"] = AnonymousUser()
            raise ValueError("User is not authenticated")

        return await self.app(scope, receive, send)
    
    
def JWTAuthMiddlewareStack(inner): 
    return CookieMiddleware(WebSocketJWTAuthMiddleware(inner))