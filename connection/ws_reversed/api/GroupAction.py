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

class GroupAction:
    
    @staticmethod

    async def GetGroupInfo(
        status: str,
        retcode: int,
        group_id: str,
        group_name: str,
        echo: str,
        message: str
        ):
        retcode = np.int64(retcode)
        try:
            message = json.dumps({
                "status": status,
                "retcode": retcode,
                "data": {
                    "group_id": group_id,
                    "group_name": group_name
                },
                "message": message,
                "echo": echo
                }, default=lambda x: int(x))
            await onebot.client.append_requests(message)
        except Exception as e:
            logger.error(f'GetGroupInfo请求失败：{e}')

    async def GetGroupList(
        status: str,
        retcode: int,
        group_id: str,
        group_name: str,
        data: list,
        echo: str,
        message: str
        ):
        retcode = np.int64(retcode)
        try:
            message = json.dumps({
                "status": status,
                "retcode": retcode,
                "data": data,
                "message": message,
                "echo": echo
                }, default=lambda x: int(x))
            await onebot.client.append_requests(message)
        except Exception as e:
            logger.error(f'GetGroupList请求失败：{e}')

    async def GetGroupMemberInfo(
        status: str,
        retcode: int,
        user_id: str,
        user_name: str,
        echo: str,
        message: str
        ):
        retcode = np.int64(retcode)
        try:
            message = json.dumps({
                "status": status,
                "retcode": retcode,
                "data": {
                    "user_id": user_id,
                    "user_name": user_name
                },
                "message": message,
                "echo": echo
                }, default=lambda x: int(x))
            await onebot.client.append_requests(message)
        except Exception as e:
            logger.error(f'GetGroupMemberInfo请求失败：{e}')

    async def GetGroupMemberList(
        status: str,
        retcode: int,
        group_id: str,
        group_name: str,
        data: list,
        echo: str,
        message: str
        ):
        retcode = np.int64(retcode)
        try:
            message = json.dumps({
                "status": status,
                "retcode": retcode,
                "data": data,
                "message": message,
                "echo": echo
                }, default=lambda x: int(x))
            await onebot.client.append_requests(message)
        except Exception as e:
            logger.error(f'GetGroupMemberList请求失败：{e}')

    async def SetGroupName(
        status: str,
        retcode: int,
        echo: str,
        message: str
        ):
        retcode = np.int64(retcode)
        try:
            message = json.dumps({
                "status": status,
                "retcode": retcode,
                "data": None,
                "message": message,
                "echo": echo
                }, default=lambda x: int(x))
            await onebot.client.append_requests(message)
        except Exception as e:
            logger.error(f'SetGroupName请求失败：{e}')

    async def LeaveGroup(
        status: str,
        retcode: int,
        echo: str,
        message: str
        ):
        retcode = np.int64(retcode)
        try:
            message = json.dumps({
                "status": status,
                "retcode": retcode,
                "data": None,
                "message": message,
                "echo": echo
                }, default=lambda x: int(x))
            await onebot.client.append_requests(message)
        except Exception as e:
            logger.error(f'LeaveGroup请求失败：{e}')