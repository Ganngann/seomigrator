"""
ASGI config for seomigratorpy project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from migrator import consumers  # Remplacez "myapp" par le nom de votre application Django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'seomigratorpy.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": URLRouter([
        path("migrator/ws/", consumers.MigratorConsumer.as_asgi()),
    ]),
})
