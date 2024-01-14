# asgi.py
import os

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

from django.core.asgi import get_asgi_application
# from .routing import application as routing_application
from .routing import ws_urlpatterns

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'BioSim.settings')

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": AuthMiddlewareStack(URLRouter(ws_urlpatterns)),
    }
)
