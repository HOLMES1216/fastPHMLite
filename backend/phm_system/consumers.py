import json
import asyncio
import jwt
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.conf import settings
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async
from .utils.data_generator import generate_system_data

User = get_user_model()

class SystemDataConsumer(AsyncJsonWebsocketConsumer):
    """系统数据推送"""

    async def connect(self):
        """建立连接"""
        # 从 URL 路径中提取 token
        token = self.scope['url_route']['kwargs'].get('service_uid')
        if not token:
            await self.close()
            return

        # 验证 token
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user_id = payload.get('user_id')
            self.scope['user'] = await self.get_user(user_id)
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError, Exception) as e:
            print(f"Token 验证失败: {e}")
            self.scope['user'] = AnonymousUser()
            await self.close()
            return

        user = self.scope.get('user')
        
        if not user.is_authenticated:
            await self.close()
            return

        # 接受连接
        await self.accept()

        # 开始定时发送数据
        self.send_data_task = asyncio.create_task(self.send_data_periodically())

    async def disconnect(self, close_code):
        """断开连接"""
        # 取消定时任务
        if hasattr(self, 'send_data_task'):
            self.send_data_task.cancel()
            try:
                await self.send_data_task
            except asyncio.CancelledError:
                pass
        # 执行父类的断开处理
        await super().disconnect(close_code)

    async def send_data_periodically(self):
        """定期发送数据"""
        while True:
            try:
                data = generate_system_data()
                # 发送数据
                await self.send_json({
                    "contentType": "HOME_DATA",
                    "speed": data['speed'],
                    "motorTemp": data['motorTemp'],
                    "bearingVib": data['bearingVib'],
                    "brakePressure": data['brakePressure'],
                    "batteryVoltage": data['batteryVoltage'],
                    "tractionCurrent": data['tractionCurrent'],
                    "wheelTemp": data['wheelTemp'],
                    "airPressure": data['airPressure'],
                    "noiseLevel": data['noiseLevel'],
                    "gearboxTemp": data['gearboxTemp'],
                    "chartData": data['chartData'],
                    "normalCount": data['normalCount'],
                    "minorFaultCount": data['minorFaultCount'],
                    "severeFaultCount": data['severeFaultCount'],
                })
                # 等待5秒
                await asyncio.sleep(0.5)
            except Exception as e:
                print(f"Error sending data: {e}")
                import traceback
                traceback.print_exc()
                break

    async def push_message(self, event):
        """推送消息到客户端"""
        await self.send_json(event["json"])

    async def get_user(self, user_id):
        """异步获取用户对象"""
        try:
            user = await database_sync_to_async(User.objects.get)(id=user_id)
            return user
        except User.DoesNotExist:
            return AnonymousUser()