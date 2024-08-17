import os,sys,time,threading
from datetime import datetime
from loguru import logger
from .websocket_reverse_server import OneBotWebSocketReverseServer

def onebot_v12_websocket_reverse():
    global client
    onebot_url = str(os.getenv("onebot_ip"))
    onebot_port = str(os.getenv("onebot_port"))
    if onebot_url.strip() == '':
        logger.error("onebot_v12链接ip不能为空！请填写链接ip！")
        time.sleep(5)
        sys.exit()
    if onebot_port.strip() == '':
        logger.error("onebot_v12链接端口号不能为空！请填写链接端口号！")
        time.sleep(5)
        sys.exit()
        
    client = OneBotWebSocketReverseServer(onebot_url, onebot_port)
    thread = threading.Thread(target=client.run)
    thread.start()
    start_hookmsg_server(hookmsgport)
    # return thread
        
def start_hookmsg_server(hookmsgport):
    from .hookmsg_server import HookMsgSocketServerManager
    server_manager = HookMsgSocketServerManager(port=int(hookmsgport))
    server_manager.start_server()

hookport = os.getenv("PORT")
hookmsgport = os.getenv("HOOK_PORT")

today = (datetime.today()).strftime("%Y-%m-%d")
logger.add(f"{os.path.join(os.getcwd(),'logs',today)}.log")

onebot_v12_websocket_reverse()
# start_hookmsg_server(hookmsgport)