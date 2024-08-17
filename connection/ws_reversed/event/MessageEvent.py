from loguru import logger
from datetime import datetime
import os
import uuid
import time
import ujson as json
from initialization.websocket_reverse_server import OneBotWebSocketReverseServer

today = (datetime.today()).strftime("%Y-%m-%d")
logger.add(f"{os.path.join(os.getcwd(),'logs',today)}.log")

class MessageEvent:
    
    @staticmethod
    
    async def GroupMessageEvent(
        client: OneBotWebSocketReverseServer,
        self_id: str,
        user_id: str,
        group_id: str,
        message: str,
        raw_message: str,
        msgtime: int,
        msgId: str,
        isat: bool,
        otherat: bool
        ):
        
        if isat == True:
            message = [
                {
                    "type": "mention",
                    "data": {
                        "user_id": self_id
                    }
                },
                {
                    "type": "text",
                    "data" : {
                        "text" : message
                    }
                }
            ]
            
        else:
            message = [
                    {
                        "type": "text",
                        "data": {
                            "text": message
                        }
                    }
                    ]
        
        try:
            data = json.dumps({
                "id": str(uuid.uuid4()),
                "self": {
                "platform": "wechat",
                "user_id": self_id,
                },
                "time": msgtime,
                "type": "message",
                "detail_type": "group",
                "sub_type": "",
                "message_id": msgId,
                "message": message,
                "alt_message": raw_message,
                "group_id": group_id,
                "user_id": user_id
            })
            await client.append_requests(data)
        except Exception as e:
            logger.error(f'GroupMessageEvent元事件发送失败：{e}')
            
    async def PrivateMessageEvent(
        client: OneBotWebSocketReverseServer,
        user_id: str,
        message: str,
        raw_message: str,
        msgtime: int,
        msgId: str,
        self_id: str
        ):
        try:
            data = json.dumps({
                "id": str(uuid.uuid4()),
                "self": {
                "platform": "wechat",
                "user_id": self_id,
                },
                "time": msgtime,
                "type": "message",
                "detail_type": "private",
                "sub_type": "",
                "message_id": msgId,
                "message": [
                    {
                        "type": "text",
                        "data": {
                            "text": message
                        }
                    }
                    ],
                "alt_message": raw_message,
                "user_id": user_id
            })
            
            await client.append_requests(data)
        except Exception as e:
            logger.error(f'PrivateMessageEvent元事件发送失败：{e}')