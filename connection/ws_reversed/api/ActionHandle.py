import json
from loguru import logger
from datetime import datetime
import os
import ujson as json
import asyncio
import requests
import time
import uuid
import shutil
import base64
from .MessageAction import MessageAction
from .UserAction import UserAction
from .FileAction import FileAction
import sqlite3
from initialization.lstep import GetSelfInfo as GetSelfInfoApi

today = (datetime.today()).strftime("%Y-%m-%d")
logger.add(f"{os.path.join(os.getcwd(),'logs',today)}.log")
onebot_url = str(os.getenv("onebot_ip"))
onebot_port = str(os.getenv("onebot_port"))
data_path = str(os.getenv("data_path"))
MemberDB = os.path.join(data_path,'member.db')
GroupDB = os.path.join(data_path,'group.db')

img_path = os.path.join(data_path,'image')
audio_path = os.path.join(data_path,'audio')
video_path = os.path.join(data_path,'video')
file_path = os.path.join(data_path,'file')

connect_url = os.getenv("connect_url")
PORT = os.getenv("PORT")

loop = asyncio.get_event_loop()

FILE_TYPES = {
    0: ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.svg'],
    1: ['.mp4', '.mov', '.avi', '.mkv', '.flv', '.wmv'],
    2: ['.mp3', '.wav', '.aac', '.flac', '.ogg', '.m4a']
}

class ActionHandle:
    def __init__(self):
        self.PORT = os.getenv('PORT')
        self.connect_url = os.getenv('connect_url')
        self.ActionUrl = f'http://{self.connect_url}:{self.PORT}'
        
    async def member_update(
        self,
        user_id: str,
        user_name: str
        ):
        conn = sqlite3.connect(MemberDB)
        try:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE Users
                SET username = ?
                WHERE userid = ?;
            """, (user_name, user_id))
            conn.commit()
        finally:
            conn.close()
            
    async def member_find_by_user_name(
        self,
        user_name: str
    ) -> str:
        try:
            conn = sqlite3.connect(MemberDB)
            cursor = conn.cursor()

            # 执行 SELECT 语句
            cursor.execute("""
                SELECT userid
                FROM Users
                WHERE username = ?;
            """, (user_name,))
            row = cursor.fetchone()

            if row:
                return str(row[0])
            else:
                raise ValueError('Username Not Found')
        finally:
            conn.close()
    
    async def member_find_by_user_id(
        self,
        user_id: str
        ) -> str:
        try:
            conn = sqlite3.connect(MemberDB)
            cursor = conn.cursor()
            cursor.execute("""
                SELECT *
                FROM Users
                WHERE userid = ?;
            """, (user_id,))
            row = cursor.fetchone()

            if row:
                return str(row[1])
            else:
                raise ValueError('Userid Not Found')
        finally:
            conn.close()
    
    async def MessageActionHandle(self,msg):
        # print (msg)
        match msg["action"]:

            case "send_message":

                if msg["params"]["detail_type"] == 'private':
                    user_id = msg["params"]["user_id"]
                    MsgTextList = ''
                    MsgImageList = []
                    MsgFileList = []
                    MsgEmojiList = []
                    echo = msg["echo"]
                    
                    try:
                        for i in list(msg["params"]["message"]):
                            match i["type"]:
                                case "mention":
                                    if i['data']['user_id'] == user_id:
                                        at_sender = True
                                    else:
                                        _at = True
                                        _at_user_id = i['data']['user_id']
                                case "mention_all":
                                    mention_all = True
                                case "text":
                                    MsgTextList += i['data']['text']
                                case "image":
                                    MsgImageList.append(i['data']['file_id'])
                                case "file":
                                    MsgFileList.append(i['data']['file_id'])
                                case _:
                                    MsgImageList.append(i['data']['file_id'])
                    except:
                        MsgTextList += msg["params"]["message"]
                    
                    await self.PrivateTextAction(
                        user_id,
                        MsgTextList,
                        echo)
                    
                    if MsgImageList != []:
                        for m in MsgImageList:
                            for i in os.listdir(img_path):
                                if str(i).startswith(m):
                                    await self.PrivateImageAction(
                                        user_id=user_id,
                                        img=os.path.join(img_path,i),
                                        echo=echo
                                    )
                                    break
                                
                    if MsgEmojiList != []:
                        for m in MsgEmojiList:
                            for i in os.listdir(img_path):
                                if str(i).startswith(m):
                                    await self.PrivateEmojiAction(
                                        user_id=user_id,
                                        img=os.path.join(img_path,i),
                                        echo=echo
                                    )
                                    break
                                
                    if MsgFileList != []:
                        for m in MsgFileList:
                            for i in os.listdir(audio_path):
                                if str(i).startswith(m):
                                    await self.PrivateFileAction(
                                        user_id=user_id,
                                        img=os.path.join(img_path,i),
                                        echo=echo
                                    )
                                    break
                            for i in os.listdir(video_path):
                                if str(i).startswith(m):
                                    await self.PrivateFileAction(
                                        user_id=user_id,
                                        img=os.path.join(img_path,i),
                                        echo=echo
                                    )
                                    break
                            for i in os.listdir(file_path):
                                if str(i).startswith(m):
                                    await self.PrivateFileAction(
                                        user_id=user_id,
                                        img=os.path.join(img_path,i),
                                        echo=echo
                                    )
                                    break
                            
                elif msg["params"]["detail_type"] == 'group':
                    at_sender = False
                    _at = False
                    _at_user_id = False
                    mention_all = False
                    user_id = msg["params"]["user_id"]
                    group_id = msg["params"]["group_id"]
                    echo = msg["echo"]
                    MsgTextList = ''
                    MsgImageList = []
                    MsgFileList = []
                    MsgEmojiList = []
                    for i in list(msg["params"]["message"]):
                        match i["type"]:
                            case "mention":
                                if i['data']['user_id'] == user_id:
                                    at_sender = True
                                else:
                                    _at = True
                                    _at_user_id = i['data']['user_id']
                            case "mention_all":
                                mention_all = True
                            case "text":
                                MsgTextList += i['data']['text']
                            case "image":
                                MsgImageList.append(i['data']['file_id'])
                            case "file":
                                MsgFileList.append(i['data']['file_id'])
                            case _:
                                MsgImageList.append(i['data']['file_id'])
                    
                    await self.GroupTextAction(
                        user_id=user_id,
                        group_id=group_id,
                        message=MsgTextList,
                        echo=echo,
                        at_sender=at_sender,
                        _at=_at,
                        _at_user_id=_at_user_id,
                        mention_all=mention_all
                    )
                    
                    if MsgImageList != []:
                        for m in MsgImageList:
                            for i in os.listdir(img_path):
                                if str(i).startswith(m):
                                    await self.GroupImageAction(
                                        group_id=group_id,
                                        img=os.path.join(img_path,i),
                                        echo=echo
                                    )
                                    break
                                
                    if MsgEmojiList != []:
                        for m in MsgEmojiList:
                            for i in os.listdir(img_path):
                                if str(i).startswith(m):
                                    await self.GroupEmojiAction(
                                        group_id=group_id,
                                        img=os.path.join(img_path,i),
                                        echo=echo
                                    )
                                    break
                                
                    if MsgFileList != []:
                        for m in MsgFileList:
                            for i in os.listdir(audio_path):
                                if str(i).startswith(m):
                                    await self.GroupFileAction(
                                        group_id=group_id,
                                        img=os.path.join(img_path,i),
                                        echo=echo
                                    )
                                    break
                            for i in os.listdir(video_path):
                                if str(i).startswith(m):
                                    await self.GroupFileAction(
                                        group_id=group_id,
                                        img=os.path.join(img_path,i),
                                        echo=echo
                                    )
                                    break
                            for i in os.listdir(file_path):
                                if str(i).startswith(m):
                                    await self.GroupFileAction(
                                        group_id=group_id,
                                        img=os.path.join(img_path,i),
                                        echo=echo
                                    )
                                    break
                    
            case "get_user_info":
                user_id = msg["params"]["user_id"]
                echo = msg["echo"]
                await self.GetUserInfoAction(
                    user_id,
                    echo
                )
                
            case "upload_file":
                _type = msg["params"]["type"]
                echo = msg["echo"]
                url='0'
                path='0'
                data='0'
                match _type:
                    case "path":
                        name = msg["params"]["name"]
                        path = msg["params"]["path"]
                    case "url":
                        name = msg["params"]["name"]
                        url = msg["params"]["url"]
                    case "data":
                        name = msg["params"]["name"]
                        data = msg["params"]["data"]
                    case _:
                        raise ValueError("Type Not Supported")
                await self.UploadFileAction(
                    _type=_type,
                    name=name,
                    url=url,
                    path=path,
                    data=data,
                    echo=echo
                )
            
            case "get_self_info":
                
                echo = msg["echo"]
                await self.GetSelfInfoAction(
                    echo=echo
                )
            
            case "get_friend_list":
                echo = msg["echo"]
                await self.GetFriendListAction(
                    echo=echo
                )
            
            # case "wx.link":
            #     echo = msg["echo"]
                # await self.GetFriendListAction(
                #     echo=echo
                # )
            
            case _:
                echo = msg["echo"]
                await self.UnsupportedMessageAction(
                    echo
                )

    async def PrivateTextAction(
            self,
            user_id: str,
            message: str,
            echo: str
        ):
        logger.info(f"向 {user_id} 发送消息: {message}")
        payload = json.dumps({
            "wxid": user_id,
            "msg": message
            })
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.request("POST", f"{self.ActionUrl}/api/sendTextMsg", headers=headers, data=payload).json()
        try:
            if response['code'] == 1:
                status = 'ok'
                retcode = 0
                msgId = str(int(time.time()))
                createdtime = time.time()
                message = ""
                echo = echo
            else:
                status = 'failed'
                retcode = 10001
                msgId = str(0)
                createdtime = time.time()
                message = response["msg"]
                echo = echo
        except:
            status = 'failed'
            retcode = 10001
            msgId = str(0)
            createdtime = time.time()
            message = response["msg"]
            echo = echo
        
        await MessageAction.MessageSentAction(
            status=status,
            retcode=retcode,
            msgId=msgId,
            createdtime=createdtime,
            message=message,
            echo=echo
        )

    async def GroupTextAction(
            self,
            user_id: str,
            group_id: str,
            message: str,
            echo: str,
            at_sender: bool,
            _at: bool,
            _at_user_id: str,
            mention_all: bool
        ):
        logger.info(f"向群聊 {group_id} 发送消息: {message}")
        headers = {
            'Content-Type': 'application/json'
        }
        if at_sender == True:
            payload = json.dumps({
                "wxids": user_id,
                "chatRoomId": group_id,
                "msg": message
                })
            response = requests.request("POST", f"{self.ActionUrl}/api/sendAtText", headers=headers, data=payload).json()
        else:
            payload = json.dumps({
                "wxid": group_id,
                "msg": message
                })
            response = requests.request("POST", f"{self.ActionUrl}/api/sendTextMsg", headers=headers, data=payload).json()
        try:
            if (response['code'] == 1) or (response["msg"] == "success"):
                status = 'ok'
                retcode = 0
                msgId = str(int(time.time()))
                createdtime = time.time()
                message = ""
                echo = echo
            else:
                status = 'failed'
                retcode = 10001
                msgId = str(0)
                createdtime = time.time()
                message = response["msg"]
                echo = echo
        except:
            status = 'failed'
            retcode = 10001
            msgId = str(0)
            createdtime = time.time()
            message = response["msg"]
            echo = echo

        await MessageAction.MessageSentAction(
            status=status,
            retcode=retcode,
            msgId=msgId,
            createdtime=createdtime,
            message=message,
            echo=echo
        )

    async def PrivateImageAction(
            self,
            user_id: str,
            img: str,
            echo: str,
        ):
        logger.info(f"向好友 {user_id} 发送私聊图片消息")
        headers = {
            'Content-Type': 'application/json'
        }
        payload = json.dumps({
            "wxid": user_id,
            "imagePath": img
            })
        response = requests.request("POST", f"{self.ActionUrl}/api/sendImagesMsg", headers=headers, data=payload).json()
        try:
            if (response['code'] == 1) or (response["msg"] == "success"):
                status = 'ok'
                retcode = 0
                msgId = str(int(time.time()))
                createdtime = time.time()
                message = ""
                echo = echo
            else:
                status = 'failed'
                retcode = 10001
                msgId = str(0)
                createdtime = time.time()
                message = response["msg"]
                echo = echo
        except:
            status = 'failed'
            retcode = 10001
            msgId = str(0)
            createdtime = time.time()
            message = response["msg"]
            echo = echo

        await MessageAction.MessageSentAction(
            status=status,
            retcode=retcode,
            msgId=msgId,
            createdtime=createdtime,
            message=message,
            echo=echo
        )

    async def GroupImageAction(
            self,
            group_id: str,
            img: str,
            echo: str,
        ):
        logger.info(f"向群聊 {group_id} 发送图片消息")
        headers = {
            'Content-Type': 'application/json'
        }
        payload = json.dumps({
            "wxid": group_id,
            "imagePath": img
            })
        response = requests.request("POST", f"{self.ActionUrl}/api/sendImagesMsg", headers=headers, data=payload).json()
        try:
            if (response['code'] == 1) or (response["msg"] == "success"):
                status = 'ok'
                retcode = 0
                msgId = str(int(time.time()))
                createdtime = time.time()
                message = ""
                echo = echo
            else:
                status = 'failed'
                retcode = 10001
                msgId = str(0)
                createdtime = time.time()
                message = response["msg"]
                echo = echo
        except:
            status = 'failed'
            retcode = 10001
            msgId = str(0)
            createdtime = time.time()
            message = response["msg"]
            echo = echo

        await MessageAction.MessageSentAction(
            status=status,
            retcode=retcode,
            msgId=msgId,
            createdtime=createdtime,
            message=message,
            echo=echo
        )

    async def PrivateEmojiAction(
            self,
            user_id: str,
            img: str,
            echo: str,
        ):
        logger.info(f"向好友 {user_id} 发送私聊Emoji消息")
        headers = {
            'Content-Type': 'application/json'
        }
        payload = json.dumps({
            "wxid": user_id,
            "filePath": img
            })
        response = requests.request("POST", f"{self.ActionUrl}/api/sendCustomEmotion", headers=headers, data=payload).json()
        try:
            if (response['code'] == 1) or (response["msg"] == "success"):
                status = 'ok'
                retcode = 0
                msgId = str(int(time.time()))
                createdtime = time.time()
                message = ""
                echo = echo
            else:
                status = 'failed'
                retcode = 10001
                msgId = str(0)
                createdtime = time.time()
                message = response["msg"]
                echo = echo
        except:
            status = 'failed'
            retcode = 10001
            msgId = str(0)
            createdtime = time.time()
            message = response["msg"]
            echo = echo

        await MessageAction.MessageSentAction(
            status=status,
            retcode=retcode,
            msgId=msgId,
            createdtime=createdtime,
            message=message,
            echo=echo
        )

    async def GroupEmojiAction(
            self,
            group_id: str,
            img: str,
            echo: str,
        ):
        logger.info(f"向群聊 {group_id} 发送Emoji消息")
        headers = {
            'Content-Type': 'application/json'
        }
        payload = json.dumps({
            "wxid": group_id,
            "filePath": img
            })
        response = requests.request("POST", f"{self.ActionUrl}/api/sendFileMsg", headers=headers, data=payload).json()
        try:
            if (response['code'] == 1) or (response["msg"] == "success"):
                status = 'ok'
                retcode = 0
                msgId = str(int(time.time()))
                createdtime = time.time()
                message = ""
                echo = echo
            else:
                status = 'failed'
                retcode = 10001
                msgId = str(0)
                createdtime = time.time()
                message = response["msg"]
                echo = echo
        except:
            status = 'failed'
            retcode = 10001
            msgId = str(0)
            createdtime = time.time()
            message = response["msg"]
            echo = echo

        await MessageAction.MessageSentAction(
            status=status,
            retcode=retcode,
            msgId=msgId,
            createdtime=createdtime,
            message=message,
            echo=echo
        )

    async def PrivateFileAction(
            self,
            user_id: str,
            file: str,
            echo: str,
        ):
        logger.info(f"向群聊 {user_id} 发送文件消息")
        headers = {
            'Content-Type': 'application/json'
        }
        payload = json.dumps({
            "wxid": user_id,
            "filePath": file
            })
        response = requests.request("POST", f"{self.ActionUrl}/api/sendFileMsg", headers=headers, data=payload).json()
        try:
            if (response['code'] == 1) or (response["msg"] == "success"):
                status = 'ok'
                retcode = 0
                msgId = str(int(time.time()))
                createdtime = time.time()
                message = ""
                echo = echo
            else:
                status = 'failed'
                retcode = 10001
                msgId = str(0)
                createdtime = time.time()
                message = response["msg"]
                echo = echo
        except:
            status = 'failed'
            retcode = 10001
            msgId = str(0)
            createdtime = time.time()
            message = response["msg"]
            echo = echo

        await MessageAction.MessageSentAction(
            status=status,
            retcode=retcode,
            msgId=msgId,
            createdtime=createdtime,
            message=message,
            echo=echo
        )

    async def GroupFileAction(
            self,
            group_id: str,
            file: str,
            echo: str,
        ):
        logger.info(f"向群聊 {group_id} 发送文件消息")
        headers = {
            'Content-Type': 'application/json'
        }
        payload = json.dumps({
            "wxid": group_id,
            "filePath": file
            })
        response = requests.request("POST", f"{self.ActionUrl}/api/sendFileMsg", headers=headers, data=payload).json()
        try:
            if (response['code'] == 1) or (response["msg"] == "success"):
                status = 'ok'
                retcode = 0
                msgId = str(int(time.time()))
                createdtime = time.time()
                message = ""
                echo = echo
            else:
                status = 'failed'
                retcode = 10001
                msgId = str(0)
                createdtime = time.time()
                message = response["msg"]
                echo = echo
        except:
            status = 'failed'
            retcode = 10001
            msgId = str(0)
            createdtime = time.time()
            message = response["msg"]
            echo = echo

        await MessageAction.MessageSentAction(
            status=status,
            retcode=retcode,
            msgId=msgId,
            createdtime=createdtime,
            message=message,
            echo=echo
        )

    async def GetUserInfoAction(
            self,
            user_id: str,
            echo: str
    ):
        logger.info(f"事件触发: GetUserInfoAction({user_id})")
        try:
            try:
                user_name = await self.member_find_by_user_id(user_id=user_id)
            except:
                user_name = user_id
            status = 'ok'
            retcode = 0
            message = ""
            echo = echo
        except Exception as e:
            user_name = user_id
            status = 'failed'
            retcode = 10001
            message = f"Error: {e}"
            echo = echo
        
        await UserAction.GetUserInfo(
            status,
            retcode,
            user_id,
            user_name,
            message,
            echo
        )
    
    async def UploadFileAction(
        self,
        _type: str,
        name: str,
        url: str,
        path: str,
        data: str,
        echo: str
    ):
        logger.info(f"事件触发: UploadFileAction")  
        message = ""
        echo = echo
        file_id = str(uuid.uuid4())
        # try:
        match _type:
            case "path":
                _, ext = os.path.splitext(path)
                for category,extensions in FILE_TYPES.items():
                    if ext in extensions:
                        match category:
                            case 0:
                                shutil.copy2(src=path,dst=os.path.join(img_path,f"{file_id + ext}"))
                            case 1:
                                shutil.copy2(src=path,dst=os.path.join(video_path,f"{file_id + ext}"))
                            case 2:
                                shutil.copy2(src=path,dst=os.path.join(audio_path,f"{file_id + ext}"))
                            case _:
                                shutil.copy2(src=path,dst=os.path.join(file_path,f"{file_id + ext}"))
                        break
                    else:
                        shutil.copy2(src=path,dst=os.path.join(file_path,f"{file_id + ext}"))
            case "url":
                response = requests.get(url)
                with open(os.path.join(img_path,f"{file_id}.png"),'wb') as file_obj:
                    file_obj.write(response.content)
            case "data":
                if type(data) != bytes:
                    data = base64.b64decode(data)
                with open(os.path.join(img_path,f"{file_id}.gif"),'wb') as file_obj:
                    file_obj.write(data)
            case _:
                raise ValueError("Type Not Supported")
        status = 'ok'
        retcode = 0
        # except Exception as e:
        #     status = 'failed'
        #     retcode = 10001
        #     message = f"Error: {e}"
            
        await FileAction.UploadFile(
            file_id=file_id,
            message=message,
            echo=echo,
            status=status,
            retcode=retcode
        )
    
    async def GetSelfInfoAction(
                self,
                echo: str
        ):
        try:
            logger.info(f"事件触发: GetSelfInfoAction")  
            self_information = GetSelfInfoApi()
            self_name = self_information[0]
            self_id = self_information[1]
            status = 'ok'
            retcode = 0
            message = ''
            
        except Exception as e:
            
            self_id = '0',
            self_name = '0'
            status = 'failed'
            retcode = 10001
            message = f"Error: {e}"
        
        await UserAction.GetSelfInfo(
            status=status,
            retcode=retcode,
            self_id=self_id,
            self_name=self_name,
            message=message,
            echo=echo
            )

    async def GetFriendListAction(
                self,
                echo: str
        ):
        member_list = []
        try:
            url = f"http://{connect_url}:{PORT}/api/getContactList"
            payload = {}
            headers = {}
            response = requests.request("POST", url, headers=headers, data=payload).json()
            for i in response['data']:
                if str(i['wxid']).startswith('wxid_'):
                    member_list.append({
                        "user_id": i['wxid'],
                        "user_name": i['nickname']
                    })
            status = 'ok'
            retcode = 0
            message = ''
            
        except Exception as e:
            
            self_id = '0',
            self_name = '0'
            status = 'failed'
            retcode = 10001
            message = f"Error: {e}"
        
        await UserAction.GetFriendList(
            status=status,
            retcode=retcode,
            self_id=self_id,
            self_name=self_name,
            message=message,
            echo=echo,
            data=member_list
            )
    
    async def UnsupportedMessageAction(
            self,
            echo: str
    ):
        logger.warning(f"事件触发: UnsupportedMessageAction，不支持的Action")  
        await MessageAction.UnsupportedMessageAction(
            echo
        )