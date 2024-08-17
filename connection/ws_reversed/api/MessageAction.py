from loguru import logger
from datetime import datetime
import os
import uuid
import time
import ujson as json
import numpy as np
import numpy as np
from initialization import onebot

today = (datetime.today()).strftime("%Y-%m-%d")
onebot_url = str(os.getenv("onebot_ip"))
onebot_port = str(os.getenv("onebot_port"))
logger.add(f"{os.path.join(os.getcwd(),'logs',today)}.log")

class MessageAction:
    
    @staticmethod
    
    async def MessageSentAction(
        status: str,
        retcode: int,
        msgId: str,
        createdtime: float,
        message: str,
        echo: str
        ):
        retcode = np.int64(retcode)
        try:
            message = json.dumps({
                "status": status,
                "retcode": retcode,
                "data": {
                    "message_id": msgId,
                    "time": createdtime
                },
                "message": message,
                "echo": echo
                }, default=lambda x: int(x))
            await onebot.client.append_requests(message)
        except Exception as e:
            logger.error(f'MessageSentAction请求失败：{e}')

    async def UnsupportedMessageAction(
        echo: str
    ):
        try:
            message = json.dumps({
                "status": 'failed',
                "retcode": 10002,
                "data": None,
                "message": '不支持的动作请求',
                "echo": echo
                }, default=lambda x: int(x))
            await onebot.client.append_requests(message)
        except Exception as e:
            logger.error(f'UnsupportedMessageAction请求失败：{e}')