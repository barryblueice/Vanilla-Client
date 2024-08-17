import threading,os
from .websocket_reverse_server import OneBotWebSocketReverseServer

hookport = os.getenv("PORT")
hookmsgport = os.getenv("HOOK_PORT")
onebot_url = str(os.getenv("onebot_ip"))
onebot_port = str(os.getenv("onebot_port"))
        
def start_hookmsg_server(hookmsgport):
    from .hookmsg_server import HookMsgSocketServerManager
    server_manager = HookMsgSocketServerManager(port=int(hookmsgport))
    server_manager.start_server()
    
def start_ws_reverse_server():
    global client
    client = OneBotWebSocketReverseServer(onebot_url, onebot_port)
    thread = threading.Thread(target=client.run)
    thread.start()
    start_hookmsg_server(hookmsgport)