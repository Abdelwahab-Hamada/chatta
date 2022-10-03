import os

from django.core.asgi import get_asgi_application
from django.urls import path

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter,URLRouter

from .consumers import Consumer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

application = ProtocolTypeRouter(
    {
        "websocket": AuthMiddlewareStack(
            URLRouter(
                [path("", Consumer.as_asgi())]
            )
        ),
    }
)
