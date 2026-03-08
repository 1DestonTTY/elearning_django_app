"""
ASGI config for elearning_app project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'elearning_app.settings')

# The traffic cop
application = ProtocolTypeRouter({
    # 1. Standard HTTP requests are routed to normal Django views
    "http": get_asgi_application(),
    
    # 2. WebSocket traffic will be routed here later!
    # "websocket": ...
})
