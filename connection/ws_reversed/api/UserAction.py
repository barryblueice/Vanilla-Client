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

class UserAction:
    
    @staticmethod
    
    async def GetSelfInfo(
        status: str,
        retcode: int,
        self_id: str,
        self_name: str,
        message: str,
        echo: str
        ):
        retcode = np.int64(retcode)
        try:
            message = json.dumps({
                "status": status,
                "retcode": retcode,
                "data": {
                    "user_id": self_id,
                    "user_name": self_name,
                },
                "message": message,
                "echo": echo
                }, default=lambda x: int(x))
            await onebot.client.append_requests(message)
        except Exception as e:
            logger.error(f'GetSelfInfo请求失败：{e}')

    async def GetUserInfo(
        status: str,
        retcode: int,
        user_id: str,
        user_name: str,
        message: str,
        echo: str
        ):
        retcode = np.int64(retcode)
        try:
            message = json.dumps({
                "status": status,
                "retcode": retcode,
                "data": {
                    "user_id": user_id,
                    "user_name": user_name,
                },
                "message": message,
                "echo": echo
                }, default=lambda x: int(x))
            await onebot.client.append_requests(message)
        except Exception as e:
            logger.error(f'GetUserInfo请求失败：{e}')

    async def GetFriendList(
        status: str,
        retcode: int,
        user_id: str,
        user_name: str,
        message: str,
        echo: str,
        data: list
        ):
        retcode = np.int64(retcode)
        try:
            message = json.dumps({
                "status": status,
                "retcode": retcode,
                "data": data,
                "echo": echo
                }, default=lambda x: int(x))
            await onebot.client.append_requests(message)
        except Exception as e:
            logger.error(f'GetFriendList请求失败：{e}')