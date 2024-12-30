import jwt
import logging
from django.conf import settings
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser

logger = logging.getLogger(__name__)

@database_sync_to_async
def get_user_from_token(token):
    from fastphmlite.system.models import Users  # 延迟导入模型
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        user_id = payload.get('user_id')
        if user_id:
            return Users.objects.get(id=user_id)
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError, Users.DoesNotExist):
        return AnonymousUser()
    return AnonymousUser()

class JWTAuthMiddleware:
    """
    JWT认证中间件，用于Channels。
    """

    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        query_string = scope.get('query_string', b'').decode()
        params = dict(part.split('=') for part in query_string.split('&') if '=' in part)
        token = params.get('token')

        if token:
            user = await get_user_from_token(token)
            logger.debug(f"解析的用户: {user} (Authenticated: {user.is_authenticated})")
        else:
            user = AnonymousUser()
            logger.debug("未提供JWT令牌，设置为AnonymousUser")

        scope['user'] = user
        return await self.inner(scope, receive, send)

def JWTAuthMiddlewareStack(inner):
    return JWTAuthMiddleware(inner)