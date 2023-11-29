from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path

application = ProtocolTypeRouter({
    "http": get_asgi_application()
})
