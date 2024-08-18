import os
import subprocess
import winreg
import wmi
import time
import sys
from datetime import datetime
from loguru import logger
from dotenv import load_dotenv,find_dotenv
import requests
import ujson as json

# wxchat_path = os.path.join(os.path.expanduser("~"),"Desktop")

def hook_initial(target_wx_version,hookport):
    connect_url = os.getenv('connect_url')
    subkey = r'Software\\Tencent\\WeChat'
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, subkey)
    value = 'Version'
    original_wxversion, type_no = winreg.QueryValueEx(key, value)
    hex_version = hex(int(original_wxversion))
    hex_str = hex_version[2:]
    new_hex_str = "0" + hex_str[1:]
    new_hex_num = int(new_hex_str, 16)
    major = (new_hex_num >> 24) & 0xFF
    minor = (new_hex_num >> 16) & 0xFF
    patch = (new_hex_num >> 8) & 0xFF
    build = (new_hex_num >> 0) & 0xFF
    original_wxversion = "{}.{}.{}.{}".format(major, minor, patch, build)
    
    if original_wxversion == target_wx_version:
        try:
            subkey = r'Software\\Tencent\\WeChat'
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, subkey)
            value = 'InstallPath'
            wxpath, type_no = winreg.QueryValueEx(key, value)
            try:
                os.remove(os.path.join(os.getcwd(),'config.ini'))
                os.remove(os.path.join(os.getcwd(),'dll','config.ini'))
            except:
                pass
            with open(os.path.join(os.getcwd(),'config.ini'),'w',encoding='utf-8') as f:
                f.write(f'''[config]\nport={hookport}''')
            with open(os.path.join(os.getcwd(),'dll','config.ini'),'w',encoding='utf-8') as f:
                f.write(f'''[config]\nport={hookport}''')
            subprocess.Popen(os.path.join(wxpath,'WeChat.exe'))
            logger.info('成功启动微信，正在进行Hook作业')
        except Exception as e:
            logger.error(f'Vanilla Client启动微信报错：{e}，请自行启动微信以进行Hook作业！')

        c = wmi.WMI()
        
        find_singal = False

        while True:
            for process in c.Win32_Process():
                if str(process.Name)=='WeChat.exe':
                    find_singal = True
                    break
            if find_singal == True:
                break

        command = [os.path.join(os.getcwd(),'dll',"ConsoleApplication.exe"), "-i", "WeChat.exe", "-p", os.path.join(os.getcwd(),'dll','wxhelper.dll')]
        subprocess.run(command, shell=True)

        logger.info("Hook作业完成，正在检测Hook是否生效……")

        try:
            url = f"http://{connect_url}:{hookport}/api/userInfo"
            payload = {}
            headers = {}
            requests.request("POST", url, headers=headers, data=payload)
        except Exception as e:
            logger.warning(f"Hook作业失败：{e}，请手动运行当前目录下dll文件夹中的dll-inject.bat以进行手动注入！")

        while True:
            try:
                url = f"http://{connect_url}:{hookport}/api/userInfo"
                payload = {}
                headers = {}
                requests.request("POST", url, headers=headers, data=payload)
                logger.success("Hook作业成功！")
                break
            except:
                pass
            
    else:
        logger.error(f"当前微信版本不支持hook，请安装版本号为{target_wx_version}的微信！")
        time.sleep(5)
        sys.exit()
        
    logger.info('正在检测登陆状态')
    while True:
        url = f"http://{connect_url}:{hookport}/api/checkLogin"
        response = requests.request("POST", url, headers=headers, data=payload).json()
        if response['code'] != 1:
            logger.error('请登录微信以进行下一步操作！')
        else:
            logger.success('微信已登录！')
            break
        time.sleep(1)

def hookmsg_server_initial(hookport,hookmsgport):
    connect_url = os.getenv('connect_url')
    logger.info('正在执行HookMsg作业')
    url = f"http://{connect_url}:{hookport}/api/hookSyncMsg"
    headers = {
        'Content-Type': 'application/json'
    }
    payload = json.dumps({
        "port": hookmsgport,
        "ip":connect_url,
        "url":f"http://localhost:{hookport}",
        "timeout":"3000",
        "enableHttp":False
    })
    
    while True:
        response = requests.request("POST", url, headers=headers, data=payload).json()
        try:
            if response['code'] == 0:
                logger.success('HookMsg作业成功！')
                break
            else:
                if response["msg"] == "success":
                    logger.success('HookMsg作业成功！')
                    break
                else:
                    logger.error(f'HookMsg错误：{response["msg"]}')
        except Exception as e:
            logger.error(f'HookMsg错误：{e}')
        time.sleep(1)

    
today = (datetime.today()).strftime("%Y-%m-%d")
logger.add(f"{os.path.join(os.getcwd(),'logs',today)}.log")
load_dotenv(find_dotenv('.env'))
target_wx_version = os.getenv("wx_version")
hookport = os.getenv("PORT")
hookmsgport = os.getenv("HOOK_PORT")
try:
    hook_initial(target_wx_version,hookport)
except:
    logger.error('微信安装错误，请重新安装！')
    time.sleep(5)
    sys.exit()
hookmsg_server_initial(hookport,hookmsgport)