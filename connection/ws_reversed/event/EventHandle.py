import json
import threading
import socketserver
from loguru import logger
from datetime import datetime
import os
import ujson as json
from .MessageEvent import MessageEvent
from .NoticeEvent import NoticeEvent
import asyncio
import xml.etree.ElementTree as ET
from initialization.lstep import GetSelfInfo
import re

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
    
    async def EventHandle(self,msg,client):
        print(msg)
        self_information = GetSelfInfo()
        self_name = self_information[0]
        self_id = self_information[1]
        
        if str(msg['fromUser']).endswith("@chatroom"):
            try:
                if str(msg["content"]).startswith("wxid_"):
                    user_id = str(msg['content'])[:(str(msg['content']).find(':\n'))]
                    cleaned_text = user_id + ':\n'
                    if cleaned_text:
                        xml_data = str(msg["content"]).replace(cleaned_text,'',1)
                        root = ET.fromstring(xml_data)
                        await self.GroupNoticeEvent(
                            self_id=self_id,
                            user_id=user_id,
                            group_id=msg['fromUser'],
                            root=root,
                            client=client)
                    else:
                        raise ValueError
                else:
                    xml_data = str(msg["content"]).replace((f"{msg['fromUser']}:\n"),'',1)
                    root = ET.fromstring(xml_data)
                    await self.GroupNoticeEvent(
                        user_id = '',
                        group_id = msg['fromUser'],
                        self_id=self_id,
                        root=root,
                        client=client)
            except:
                await self.GroupMessageEvent(msg,client)

        elif str(msg['fromUser']).startswith("wxid_"):
            try:
                xml_data = str(msg["content"]).replace((f"{msg['fromUser']}:\n"),'',1)
                root = ET.fromstring(xml_data)
                await self.PrivateNoticeEvent(
                    self_id=self_id,
                    root=root,
                    client=client)
            except:
                await self.PrivateMessageEvent(msg,client)
            
    async def GroupMessageEvent(self,msg,client):
        _at_status = False
        _other_at_status = False
        _other_at_wx_id = ""
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
            
        match = re.search(r'^\@\w+', message)
        
        if match:
            
            at_content = match.group(0)
            
            with open (member_path,'r',encoding='utf-8') as f:
                member_list = json.load(f)
                
            for i in member_list:
                if at_content == member_list[i]:
                    _other_at_status = True
                    _other_at_wx_id = 'i'
                    break
        
        logger.info(f'{user_id} 在群聊 {group_id} 中发送了一条消息：{message}')
        await MessageEvent.GroupMessageEvent(
            client=client,
            user_id=user_id,
            group_id=group_id,
            self_id=self_id,
            message=message,
            raw_message=raw_message,
            msgtime=msgtime,
            msgId=msgId,
            isat=_at_status,
            otherat = _other_at_status,
            _other_at_wx_id = _other_at_wx_id
        )
        
    async def PrivateMessageEvent(self,msg,client):
        self_id = str(msg['toUser'])
        user_id = str(msg['fromUser'])
        msgtime = str(msg['createTime'])
        msgId = str(msg['msgId'])
        message = msg['content']
        logger.info(f'{user_id} 给你发送了一条私聊消息：{message}')
        user_name = str(user_id)
        
        with open(member_path,'r',encoding='utf-8') as f:
            member_list = json.load(f)
            
        if user_id not in member_list:
            
            member_list.update({user_id:user_name})
            
            with open(member_path,'w') as f:
                json.dump(member_list,f,indent=4,ensure_ascii=True)
            
        await MessageEvent.PrivateMessageEvent(
            client=client,
            user_id=user_id,
            message=message,
            raw_message=message,
            msgtime=msgtime,
            msgId=msgId,
            self_id=self_id
        )
        
    async def GroupNoticeEvent(
        self,
        self_id: str,
        user_id: str,
        group_id: str,
        root,
        client):
        sysmsg_type = str(root.attrib.get('type'))
        match sysmsg_type:
            
            case "pat":
                pattedusername = root.find('.//pattedusername').text
                if str(pattedusername) == self_id:
                    user_id = root.find('.//fromusername').text
                    group_id = str(root.find('.//chatusername').text)
                    logger.info(f'{user_id} 在群聊 {group_id} 中拍了拍你')
                    
                    await NoticeEvent.PatEvent(
                        client=client,
                        user_id=user_id,
                        self_id=self_id,
                        group_id=group_id
                    )

            case "revokemsg":
                msg_id = str(root.find('.//msgid').text)
                logger.info(f'{user_id} 在群聊 {group_id} 中撤回了一条消息')
                await NoticeEvent.GroupMessageDeleteEvent(
                    client=client,
                    group_id=group_id,
                    user_id=user_id,
                    self_id=self_id,
                    msg_id=msg_id
                )

    async def PrivateNoticeEvent(
        self,
        self_id: str,
        root,
        client):
        sysmsg_type = str(root.attrib.get('type'))
        match sysmsg_type:
            
            case "pat":
                pattedusername = root.find('.//pattedusername').text
                if str(pattedusername) == self_id:
                    user_id = root.find('.//fromusername').text
                    logger.info(f'{user_id} 在私聊消息中拍了拍你')
                    
                    await NoticeEvent.PatEvent(
                        client=client,
                        user_id=user_id,
                        self_id=self_id,
                        group_id=0
                    )

            case "revokemsg":
                msg_id = str(root.find('.//msgid').text)
                user_id = str(root.find('.//session').text)
                logger.info(f'{user_id} 在私聊消息中撤回了一条消息')
                await NoticeEvent.PrivateMessageDeleteEvent(
                    client=client,
                    user_id=user_id,
                    self_id=self_id,
                    msg_id=msg_id
                )