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

class FileAction:
    
    @staticmethod

    async def UploadFile(
        status: str,
        retcode: int,
        file_id: str,
        echo: str,
        message: str
        ):
        retcode = np.int64(retcode)
        try:
            message = json.dumps({
                "status": status,
                "retcode": retcode,
                "data": {
                    "file_id": file_id
                },
                "message": message,
                "echo": echo
                }, default=lambda x: int(x))
            await onebot.client.append_requests(message)
        except Exception as e:
            logger.error(f'GetGroupInfo请求失败：{e}')