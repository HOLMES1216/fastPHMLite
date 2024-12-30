# -*- coding: utf-8 -*-
from django.urls import re_path
from django.urls import path
from application.websocketConfig import MegCenter
from phm_system.consumers import SystemDataConsumer
websocket_urlpatterns = [
    path('ws/<str:service_uid>/', MegCenter.as_asgi()),  
    re_path(r"ws/(?P<service_uid>[^/]+)/system_data/$", SystemDataConsumer.as_asgi()),
]
