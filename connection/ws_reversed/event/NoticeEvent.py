from loguru import logger
from datetime import datetime
import os
import uuid
import time
import ujson as json
from initialization.websocket_reverse_server import OneBotWebSocketReverseServer

today = (datetime.today()).strftime("%Y-%m-%d")
logger.add(f"{os.path.join(os.getcwd(),'logs',today)}.log")

class NoticeEvent:
    
    @staticmethod

    async def friend_increase(
        self_id: str,
        user_id: str,
        client: OneBotWebSocketReverseServer
    ):
        try:
            message = json.dumps({
                "id": str(uuid.uuid4()),
                "self": {
                    "platform": "wechat",
                    "user_id": self_id
                },
                "time": time.time(),
                "type": "notice",
                "detail_type": "friend_increase",
                "sub_type": "",
                "user_id": user_id
            })
            
            await client.append_requests(message)
            logger.success(f'friend_increase事件：{user_id}')
        except Exception as e:
            logger.error(f'friend_increase事件发送失败：{e}')

    async def friend_decrease(
        self_id: str,
        user_id: str,
        client: OneBotWebSocketReverseServer
    ):
        try:
            message = json.dumps({
                "id": str(uuid.uuid4()),
                "self": {
                    "platform": "wechat",
                    "user_id": self_id
                },
                "time": time.time(),
                "type": "notice",
                "detail_type": "friend_decrease",
                "sub_type": "",
                "user_id": user_id
            })
            
            await client.append_requests(message)
            logger.success(f'friend_decrease事件：{user_id}')
        except Exception as e:
            logger.error(f'friend_decrease事件发送失败：{e}')

    async def friend_decrease(
        self_id: str,
        user_id: str,
        message_id: str,
        client: OneBotWebSocketReverseServer
    ):
        try:
            message = json.dumps({
                "id": str(uuid.uuid4()),
                "self": {
                    "platform": "wechat",
                    "user_id": self_id
                },
                "time": time.time(),
                "type": "notice",
                "detail_type": "private_message_delete",
                "sub_type": "",
                "user_id": user_id,
                "message_id":message_id
            })
            
            await client.append_requests(message)
            logger.success(f'private_message_delete事件：{user_id}')
        except Exception as e:
            logger.error(f'private_message_delete事件发送失败：{e}')