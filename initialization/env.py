import os,sys,time
import ujson as json
from loguru import logger
from datetime import datetime
from dotenv import find_dotenv, load_dotenv

env_default = f'''# 目标WeChat.exe被hook后的地址
connect_url = 127.0.0.1

# 目标WeChat.exe被hook后的端口
PORT = 19088

# HookMsg接收端口
HOOK_PORT = 8000

# 反向连接ip（暂时仅支持反向连接）
onebot_ip = 127.0.0.1

# 反向连接端口号（暂时仅支持反向连接）
onebot_port = 8080

# 数据路径（请使用绝对路径，范例：C:\\\data或C:\\data）
data_path = {os.path.join(os.getcwd(),'data')}

# 微信版本号（请勿修改！）
wx_version = 3.9.8.25

# Vanilla Client版本号（请勿修改！）
V_version = 1.1.1'''

def initial_env():
    try:
        if not load_dotenv(find_dotenv('.env')):
            with open(os.path.join(os.getcwd(),'.env'),'w',encoding='utf-8') as f:
                f.write(env_default)
            logger.info("环境变量文件已初始化完成，请编辑环境变量文件后重启Vallina Client！")
            time.sleep(5)
            sys.exit()
    except Exception as e:
        logger.error(f"错误：{e}")
        time.sleep(5)
        sys.exit()

def initial_member_data(data_path: str):
    try:
        if not os.path.exists(data_path):
            os.makedirs(data_path)
            
        if not os.path.exists(os.path.join(data_path,'member.json')):
            with open(os.path.join(data_path,'member.json'),'w') as f:
                json.dump({},f,indent=4)
    except Exception as e:
        logger.error(f"错误：{e}")
        time.sleep(5)
        sys.exit()
        
def initial_file_data(data_path: str):
    try:
        if not os.path.exists(data_path):
            os.makedirs(data_path)
        for i in ['image','audio','video','file']:
            if not os.path.exists(os.path.join(data_path,i)):
                os.makedirs(os.path.join(data_path,i))
    except Exception as e:
        logger.error(f"错误：{e}")
        time.sleep(5)
        sys.exit()
    
today = (datetime.today()).strftime("%Y-%m-%d")
logger.add(f"{os.path.join(os.getcwd(),'logs',today)}.log")
initial_env()
data_path = str(os.getenv("data_path"))
member_path = os.path.join(data_path,'member.json')
initial_member_data(data_path)
initial_file_data(data_path)