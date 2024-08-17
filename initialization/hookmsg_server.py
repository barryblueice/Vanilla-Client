import json
import threading
import socketserver
from loguru import logger
from datetime import datetime
import os
import ujson as json
from connection.ws_reversed.event.EventHandle import EventHandle

today = (datetime.today()).strftime("%Y-%m-%d")
logger.add(f"{os.path.join(os.getcwd(),'logs',today)}.log")
onebot_url = str(os.getenv("onebot_ip"))
onebot_port = str(os.getenv("onebot_port"))

class ReceiveMsgSocketServer(socketserver.BaseRequestHandler):
    def handle(self):
        conn = self.request
        while True:
            try:
                ptr_data = b""
                while True:
                    data = conn.recv(1024)
                    ptr_data += data
                    if len(data) == 0 or data[-1] == 0xA:
                        break

                msg = json.loads(ptr_data)
                ReceiveMsgSocketServer.msg_callback(msg)

            except OSError:
                break
            except json.JSONDecodeError:
                pass
        conn.close()

    @staticmethod
    def msg_callback(msg):
        # print (msg)
        from .onebot import client
        event_handle = EventHandle()
        event_handle.EventHandle(msg,client)

class HookMsgSocketServerManager:
    def __init__(self, port: int = 8000, handler=ReceiveMsgSocketServer):
        self.connect_url = os.getenv('connect_url')
        port = int(os.getenv('HOOK_PORT'))
        self.ip_port = (self.connect_url, port)
        self.handler = handler
        self.server = socketserver.ThreadingTCPServer(self.ip_port, self.handler)
        self.thread = None

    def start_server(self):
        if not self.thread:
            self.thread = threading.Thread(target=self.server.serve_forever)
            self.thread.setDaemon(True)
            self.thread.start()
            logger.success(f"HookMsg接收服务器已监听{self.ip_port[1]}，进程号为{self.thread.ident}")
            return self.thread.ident
        else:
            logger.warning('HookMsg接收服务器已在运行')
            return self.thread.ident

    def stop_server(self):
        if self.server:
            self.server.shutdown()
            self.server.server_close()
            self.thread = None
            logger.success('已停止HookMsg接收服务器')

# if __name__ == '__main__':
#     hookmsgport = int(os.getenv("HOOK_PORT"))
#     server_manager = HookMsgSocketServerManager(port=hookmsgport)
#     server_manager.start_server()
