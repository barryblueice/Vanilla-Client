from datetime import datetime
from loguru import logger
import os
import requests

today = (datetime.today()).strftime("%Y-%m-%d")
logger.add(f"{os.path.join(os.getcwd(),'logs',today)}.log")

def GetSelfInfo() -> list:
    hookport = os.getenv("PORT")
    connect_url = os.getenv('connect_url')
    url = f"http://{connect_url}:{hookport}/api/userInfo"
    payload = {}
    headers = {}
    response = requests.request("POST", url, headers=headers, data=payload).json()
    # logger.success(f"欢迎回来！用户：{response['data']['name']}，wxid：{response['data']['wxid']}")
    # print (response['data']['dbKey'])
    # print (response)
    return [response['data']['name'],response['data']['wxid']]