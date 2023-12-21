# routing.py

from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from fema.consumers import CityConsumer

application = ProtocolTypeRouter({
    "websocket": URLRouter(
        [
            path("ws/city/", CityConsumer.as_asgi()),
        ]
    ),
})
