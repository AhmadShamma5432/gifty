# foodordering/asgi.py

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import re_path
from notifications.routing import websocket_urlpatterns

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'foodordering.settings')

# Standard WSGI application for HTTP requests
http_application = get_asgi_application()

application = ProtocolTypeRouter({
    "http": http_application,
    "websocket": websocket_urlpatterns,
})