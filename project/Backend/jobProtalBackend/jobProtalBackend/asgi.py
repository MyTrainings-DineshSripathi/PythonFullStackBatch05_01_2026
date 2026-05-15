"""
ASGI config for jobProtalBackend project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jobProtalBackend.settings')

django_asgi_app = get_asgi_application()

# Import after Django is configured
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import re_path
from .jwt_auth_middleware import JwtAuthMiddleware
from jobs.consumers import NotificationConsumer

application = ProtocolTypeRouter({
    'http': django_asgi_app,
    'websocket': JwtAuthMiddleware(
        URLRouter([
            re_path(r'^ws/notifications/$', NotificationConsumer.as_asgi()),
        ])
    ),
})
