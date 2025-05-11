
from django.urls import re_path
from chat.message.entrypoints.consumers import PrivateMessageConsumer

websocket_urlpatterns = [
    re_path(r'ws/chat/', PrivateMessageConsumer.as_asgi()),
]