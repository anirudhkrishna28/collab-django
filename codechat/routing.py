from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path("ws/collab/", consumers.CollabConsumer.as_asgi()),
]