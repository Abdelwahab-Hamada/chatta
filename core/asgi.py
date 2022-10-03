import os
import django

from django.core.asgi import get_asgi_application
from django.urls import path

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter,URLRouter

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from .consumers import Consumer

application = ProtocolTypeRouter(
    {
        "websocket": AuthMiddlewareStack(
            URLRouter(
                [path("", Consumer.as_asgi())]
            )
        ),
    }
)
