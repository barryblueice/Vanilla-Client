import os,sys,time,sqlite3
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

# 运行数据路径（请使用绝对路径，范例：C:\\\data或C:\\data）
data_path = {os.path.join(os.getcwd(),'data')}

# 微信数据路径（请使用绝对路径，范例：C:\\<路径>\\WeChat Files或C:\<路径>\WeChat Files。路径可自行在微信设置中查询，如果为空则部分功能可能受到限制）
wx_data_path = 

# websocket文件缓冲大小。默认为4，单位MB，不能为0或空。
ws_max_size = 4

# 微信版本号（请勿修改！）
wx_version = 3.9.8.25

# Vanilla Client版本号（请勿修改！）
V_version = 1.3.1'''

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
        
def check_env():
    for i in ['connect_url','PORT','HOOK_PORT','onebot_ip','onebot_port','data_path','ws_max_size','wx_version','V_version']:
        _env=os.getenv(i)
        if (str(_env).replace(' ','') == '') or (_env == None):
            logger.error(f"错误：变量“{i}”为空，请修改环境变量文件后重启Vallina Client！")
            time.sleep(5)
            sys.exit()
        
def makememberdb():
    try:
        conn = sqlite3.connect(os.path.join(data_path,'member.db'))
        try:
            cursor = conn.cursor()
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS Users (
                userid TEXT PRIMARY KEY,
                username TEXT
            )
            ''')
            conn.commit()
            logger.success("已连接到member.db数据库！")
        finally:
            conn.close()
        
        conn = sqlite3.connect(os.path.join(data_path,'group.db'))
        try:
            cursor = conn.cursor()
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS Groups (
                groupid TEXT PRIMARY KEY,
                groupname TEXT
            )
            ''')
            conn.commit()
            logger.success("已连接到group.db数据库！")
        finally:
            conn.close()
    except Exception as e:
        logger.error(f"错误：{e}")
        time.sleep(5)
        sys.exit()

def initial_member_data(data_path: str):
    try:
        if not os.path.exists(data_path):
            os.makedirs(data_path)
        makememberdb()
        # if not os.path.exists(os.path.join(data_path,'member.db')):
            # with open(os.path.join(data_path,'member.db'),'w') as f:
            #     json.dump({},f,indent=4)
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
check_env()
data_path = str(os.getenv("data_path"))
# member_path = os.path.join(data_path,'member.json')
initial_member_data(data_path)
initial_file_data(data_path)