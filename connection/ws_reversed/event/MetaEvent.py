from loguru import logger
from datetime import datetime
import os
import uuid
import time
import ujson as json

today = (datetime.today()).strftime("%Y-%m-%d")
logger.add(f"{os.path.join(os.getcwd(),'logs',today)}.log")

class MetaEvent:
    
    @staticmethod
    
    async def connect(client):
        try:
            message = json.dumps({
                "id": str(uuid.uuid4()),
                "time": time.time(),
                "type": "meta",
                "detail_type": "connect",
                "sub_type": "",
                "version": {
                    "impl": "Vanilla-Client",
                    "version": os.getenv('V_version', '1.0.0'),
                    "onebot_version": "12"
                }
            })
            
            await client.append_requests(message)
            logger.success('已发送MetaEvent.connect元事件')
        except Exception as e:
            logger.error(f'MetaEvent.connect元事件发送失败：{e}')
            
    async def status_update(client, self_id: str, online: bool):
        try:
            message = json.dumps({
                "id": str(uuid.uuid4()),
                "time": time.time(),
                "type": "meta",
                "detail_type": "status_update",
                "sub_type": "",
                "status": {
                    "good": True,
                    "bots": [
                        {
                            "self": {
                                "platform": "wechat",
                                "user_id": self_id
                            },
                            "online": online
                        }
                    ]
                }
            })
            # print (message)
            await client.append_requests(message)
            logger.success('已发送MetaEvent.status_update元事件')
        except Exception as e:
            logger.error(f'MetaEvent.status_update元事件发送失败：{e}')