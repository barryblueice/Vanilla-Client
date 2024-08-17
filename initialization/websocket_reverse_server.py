import asyncio
import websockets
import os
from datetime import datetime
from loguru import logger
import ujson as json
from connection.ws_reversed.api.ActionHandle import ActionHandle
from .lstep import welcome_info
from connection.ws_reversed.event import MetaEvent

class OneBotWebSocketReverseServer:
    today = (datetime.today()).strftime("%Y-%m-%d")
    log_path = os.path.join(os.getcwd(), 'logs', f"{today}.log")
    logger.add(log_path)

    def __init__(self, host: str, port: int, path: str = "/onebot/v12/ws"):
        self.uri = f"ws://{host}:{port}{path}"
        self.message_queue = asyncio.Queue()
        self.websocket = None

    async def connect(self):
        while True:
            try:
                async with websockets.connect(self.uri) as websocket:
                    self.websocket = websocket
                    logger.success(f'已连接到反向服务器: {self.uri}')
                    self_information = welcome_info()
                    logger.success(f"欢迎回来！用户：{self_information[0]}，wxid：{self_information[1]}")
                    await MetaEvent.MetaEvent.connect(self)
                    await MetaEvent.MetaEvent.status_update(self,self_information[1])
                    consumer_task = asyncio.create_task(self.listen(websocket))
                    producer_task = asyncio.create_task(self.send_requests())
                    await asyncio.gather(consumer_task, producer_task)
            except websockets.ConnectionClosedError as e:
                logger.error(f"WebSocket连接错误，代码: {e.code}, 原因: {e.reason}")
                if e.code == 1012:
                    # 处理1012错误，等待服务器重启
                    logger.warning("收到服务器重启请求，等待重新连接...")
                await asyncio.sleep(5)
            except Exception as e:
                logger.error(f"反向服务器连接错误: {e}")
                await asyncio.sleep(5)

    async def listen(self, websocket):
        try:
            async for message in websocket:
                await self.handle_message(message)
        except websockets.ConnectionClosed as e:
            logger.warning(f"反向服务器连接关闭 {e.code} - {e.reason}")
            raise  # 重新引发异常，以便connect方法处理
        except Exception as e:
            logger.error(f"监听服务器消息时出现错误：{e}")

    async def handle_message(self, message):
        # print(message)
        message = json.loads(message)
        action_handle = ActionHandle()
        await action_handle.MessageActionHandle(message)

    async def send_requests(self):
        while True:
            try:
                message = self.message_queue.get_nowait()
                if self.websocket:
                    try:
                        await self.websocket.send(message)
                    except Exception as e:
                        logger.error(f"向反向ws服务器发送消息时出现错误：{e}")
                self.message_queue.task_done()
            except asyncio.QueueEmpty:
                await asyncio.sleep(0.1)

    async def append_requests(self, message):
        await self.message_queue.put(message)

    def run(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop = asyncio.get_event_loop()
        try:
            loop.run_until_complete(self.connect())
            loop.run_forever()
        except KeyboardInterrupt:
            logger.info("停止进程")
