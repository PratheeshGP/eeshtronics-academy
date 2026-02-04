"""
WebSocket URL routing for Django Channels.
"""
from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/lab/(?P<session_id>\d+)/$', consumers.LabTerminalConsumer.as_asgi()),
]
