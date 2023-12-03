"""
ASGI config for ChatAPI project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os

from channels.routing import URLRouter, ProtocolTypeRouter
from channels.security.websocket import AllowedHostsOriginValidator  
from django.core.asgi import get_asgi_application
from chat import routing  
from .tokenauth_middleware import TokenAuthMiddleware  

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ChatAPI.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AllowedHostsOriginValidator(  
        TokenAuthMiddleware(URLRouter(routing.websocket_urlpatterns)))
})