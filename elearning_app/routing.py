import os
from django.core.asgi import get_asgi_application

#set up django environment before routing
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'elearning_app.settings')
django_asgi_app = get_asgi_application()

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import chat.routing

application = ProtocolTypeRouter({
    #standard HTTP requests (normal web pages) are route here
    "http": django_asgi_app,

    #websocket traffic (the real-time chat) are route here
    "websocket": AuthMiddlewareStack(
        URLRouter(
            chat.routing.websocket_urlpatterns
        )
    ),
})