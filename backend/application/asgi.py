import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator


# 1. 设置环境变量
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'application.settings')
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"

# 2. 获取 Django 的 ASGI 应用
django_asgi_app = get_asgi_application()
from application.routing import websocket_urlpatterns
from application.middleware import JWTAuthMiddlewareStack  # 导入自定义中间件
# 3. 配置 ProtocolTypeRouter
application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AllowedHostsOriginValidator(
        JWTAuthMiddlewareStack(
            URLRouter(
                websocket_urlpatterns
            )
        )
    ),
})