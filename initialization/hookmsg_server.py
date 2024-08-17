import asyncio
import json
from loguru import logger
from datetime import datetime
import os
from connection.ws_reversed.event.EventHandle import EventHandle

today = (datetime.today()).strftime("%Y-%m-%d")
logger.add(f"{os.path.join(os.getcwd(), 'logs', today)}.log")

class ReceiveMsgAsyncServer:
    def __init__(self, host='127.0.0.1', port=8000):
        self.server = None
        self.host = host
        self.port = port

    async def handle_client(self, reader, writer):
        try:
            while True:
                ptr_data = await reader.readuntil(separator=b'\n')
                msg = json.loads(ptr_data)
                await self.msg_callback(msg)
        except asyncio.IncompleteReadError:
            pass
        except json.JSONDecodeError:
            logger.error("JSON解码错误")
        finally:
            writer.close()
            await writer.wait_closed()

    async def msg_callback(self, msg):
        from .onebot import client
        event_handle = EventHandle()
        await event_handle.EventHandle(msg, client)

    async def start_server(self):
        self.server = await asyncio.start_server(self.handle_client, self.host, self.port)
        logger.success(f"异步HookMsg接收服务器已启动，监听端口 {self.port}")
        async with self.server:
            await self.server.serve_forever()

    def stop_server(self):
        if self.server:
            self.server.close()
            logger.success("已停止异步HookMsg接收服务器")

class HookMsgSocketServerManager:
    def __init__(self, port: int = 8000):
        self.server = ReceiveMsgAsyncServer(port=port)

    async def start_server(self):
        await self.server.start_server()

    def stop_server(self):
        self.server.stop_server()
