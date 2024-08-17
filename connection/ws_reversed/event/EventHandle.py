import json
import threading
import socketserver
from loguru import logger
from datetime import datetime
import os
import ujson as json
from connection.ws_reversed.event import MessageEvent
import asyncio

today = (datetime.today()).strftime("%Y-%m-%d")
logger.add(f"{os.path.join(os.getcwd(),'logs',today)}.log")
onebot_url = str(os.getenv("onebot_ip"))
onebot_port = str(os.getenv("onebot_port"))
loop = asyncio.get_event_loop()
data_path = str(os.getenv("data_path"))
member_path = os.path.join(data_path,'member.json')

class EventHandle:
    def __init__(self):
        pass
    
    def EventHandle(self,msg,client):
        
        if str(msg['fromUser']).endswith("@chatroom"):
                
            self.GroupMessageEvent(msg,client)

        elif str(msg['fromUser']).startswith("wxid_"):
            
            self.PrivateMessageEvent(msg,client)
            
    def GroupMessageEvent(self,msg,client):
        _at_status = False
        _other_at_status = False
        user_id = str(msg['content'])[:(str(msg['content']).find(':\n'))]
        group_id = str(msg['fromUser'])
        self_id = str(msg['toUser'])
        msgtime = str(msg['createTime'])
        msgId = str(msg['msgId'])
        raw_message = str(msg['displayFullContent'])
        message = str(msg['content'])[(str(msg['content']).find(':\n'))+2:]
        user_name = str(msg['displayFullContent'])[:(str(msg['displayFullContent']).find(' :'))]
        
        with open(member_path,'r',encoding='utf-8') as f:
            member_list = json.load(f)
            
        member_list.update({user_id:user_name})
        
        with open(member_path,'w') as f:
            json.dump(member_list,f,indent=4,ensure_ascii=True)
        
        if raw_message.endswith("在群聊中@了你"):
            _at_status = True
            raw_message = f'{raw_message}: {message}'
        
        logger.info(f'{user_id} 在群 {group_id} 发送了一条消息：{message}')
        asyncio.run(MessageEvent.MessageEvent.GroupMessageEvent(
            client=client,
            user_id=user_id,
            group_id=group_id,
            self_id=self_id,
            message=message,
            raw_message=raw_message,
            msgtime=msgtime,
            msgId=msgId,
            isat=_at_status,
            otherat = _other_at_status
        ))
        
    def PrivateMessageEvent(self,msg,client):
        self_id = str(msg['toUser'])
        user_id = str(msg['fromUser'])
        msgtime = str(msg['createTime'])
        msgId = str(msg['msgId'])
        message = msg['content']
        logger.info(f'{user_id} 给你发送了一条私人消息：{message}')
        user_name = str(user_id)
        
        with open(member_path,'r',encoding='utf-8') as f:
            member_list = json.load(f)
            
        if user_id not in member_list:
            
            member_list.update({user_id:user_name})
            
            with open(member_path,'w') as f:
                json.dump(member_list,f,indent=4,ensure_ascii=True)
            
        asyncio.run(MessageEvent.MessageEvent.PrivateMessageEvent(
            client=client,
            user_id=user_id,
            message=message,
            raw_message=message,
            msgtime=msgtime,
            msgId=msgId,
            self_id=self_id
        ))