"""
ASGI config for mysite project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os
from chatapp.socketIO import SIO
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
###### chat app
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
###########################################
from django.core.asgi import get_asgi_application
from socketio import ASGIApp
from django.urls import path, re_path
from middlewares.JWTMiddleware import JWTAuthMiddlewareStack
from . import settings
# Initialize Django ASGI application early to ensure the AppRegistry
# is populated before importing code that may import ORM models.
############ chat app
django_asgi_app = get_asgi_application()



application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": JWTAuthMiddlewareStack(
            ASGIApp(SIO,django_asgi_app)
        )
            # AuthMiddlewareStack(URLRouter(chatapp.routing.websocket_urlpatterns))
    }
)

########################
