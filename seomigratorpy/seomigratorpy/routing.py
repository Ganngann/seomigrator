from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from seomigratorpy import consumers

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": URLRouter([
        path("migrator/ws/", consumers.MigratorConsumer.as_asgi()),
    ]),
})
