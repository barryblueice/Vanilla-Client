import os,sqlite3
from datetime import datetime
from loguru import logger
import requests
import shutil

TargetFilePath = os.path.join(str(os.getenv("wx_data_path")))
datapath = os.path.join(str(os.getenv("data_path")))
TargetMemberDB = os.path.join(datapath,'member.db')
TargetGroupDB = os.path.join(datapath,'group.db')

today = (datetime.today()).strftime("%Y-%m-%d")
logger.add(f"{os.path.join(os.getcwd(),'logs',today)}.log")

import ctypes
import hashlib
import hmac

# pip install pycryptodome
from Crypto.Cipher import AES

SQLITE_FILE_HEADER = bytes('SQLite format 3', encoding='ASCII') + bytes(1)
KEY_SIZE = 32
DEFAULT_PAGESIZE = 4096
DEFAULT_ITER = 64000

def decrypt(password, input_file, out_file):
    password = bytes.fromhex(password.replace(' ', ''))
    with open(input_file, 'rb') as (f):
        blist = f.read()
    # print(len(blist))
    salt = blist[:16]
    key = hashlib.pbkdf2_hmac('sha1', password, salt, DEFAULT_ITER, KEY_SIZE)
    first = blist[16:DEFAULT_PAGESIZE]
    mac_salt = bytes([x ^ 58 for x in salt])
    mac_key = hashlib.pbkdf2_hmac('sha1', key, mac_salt, 2, KEY_SIZE)
    hash_mac = hmac.new(mac_key, digestmod='sha1')
    hash_mac.update(first[:-32])
    hash_mac.update(bytes(ctypes.c_int(1)))
    if hash_mac.digest() == first[-32:-12]:
        logger.success("数据库解密成功")
    else:
        logger.error("数据库解密失败，密钥错误")
        return Exception
    blist = [blist[i:i + DEFAULT_PAGESIZE] for i in range(DEFAULT_PAGESIZE, len(blist), DEFAULT_PAGESIZE)]
    with open(out_file, 'wb') as (f):
        f.write(SQLITE_FILE_HEADER)
        t = AES.new(key, AES.MODE_CBC, first[-48:-32])
        f.write(t.decrypt(first[:-48]))
        f.write(first[-48:])
        for i in blist:
            t = AES.new(key, AES.MODE_CBC, i[-48:-32])
            f.write(t.decrypt(i[:-48]))
            f.write(i[-48:])

def GetDBKey() -> str:
    hookport = os.getenv("PORT")
    connect_url = os.getenv('connect_url')
    url = f"http://{connect_url}:{hookport}/api/userInfo"
    payload = {}
    headers = {}
    response = requests.request("POST", url, headers=headers, data=payload).json()
    return response['data']['dbKey']

def WriteMemberInfo(DecryptedChatRoomUserDB,TargetMemberDB,TargetGroupDB):
    conn = sqlite3.connect(DecryptedChatRoomUserDB)
    cursor = conn.cursor()

    conn_user = sqlite3.connect(TargetMemberDB)
    cursor_user = conn_user.cursor()
    
    conn_group = sqlite3.connect(TargetGroupDB)
    cursor_group = conn_group.cursor()
    
    try:
        table_name = 'ChatRoomUserNameToId'

        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = [description[1] for description in cursor.fetchall()]
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()
        for row in rows:
            # print(f"{columns[0]}: {row[0]}")
            if columns[0] == 'UsrName':
                if str(row[0]).startswith('wxid_'):
                    cursor_user.execute('''
            INSERT OR REPLACE INTO Users (userid, username)
            VALUES (?, ?)
            ''', (row[0], row[0]))
                elif str(row[0]).endswith('@chatroom'):
                    cursor_group.execute('''
            INSERT OR REPLACE INTO Groups (groupid, groupname)
            VALUES (?, ?)
            ''', (row[0], row[0]))
        conn_user.commit()
        conn_group.commit()
    finally:
        conn.close()
        conn_user.close()
        conn_group.close()

def DataBaseDecryptedProcess(wxid: str):
    try:
        TargetDBPath = os.path.join(TargetFilePath,wxid,'Msg')
        ChatRoomUserDB = os.path.join(TargetDBPath,'ChatRoomUser.db')
        password = GetDBKey()
        DecryptedChatRoomUserDB = os.path.join(datapath,'ChatRoomUserDecrypted.db')
        decrypt(password, ChatRoomUserDB, DecryptedChatRoomUserDB)
        WriteMemberInfo(DecryptedChatRoomUserDB,TargetMemberDB,TargetGroupDB)
        logger.success('数据库更新成功')
    except Exception as e:
        logger.warning(logger.info(f'数据库更新失败：{e}，部分功能将无法使用。'))
    finally:
        try:
            os.remove(DecryptedChatRoomUserDB)
        except:
            pass