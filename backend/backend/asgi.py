"""
ASGI config for backend project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
import django
django.setup()
from django.core.management import call_command

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
  # Replace with your app name

from django.urls import path


from django.core.asgi import get_asgi_application

application = ProtocolTypeRouter({
    "http": get_asgi_application(),  # Handles standard HTTP requests
    "websocket": AuthMiddlewareStack(  # Handles WebSocket connections
        URLRouter([
        ])
    ),
})