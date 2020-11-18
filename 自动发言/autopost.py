#encoding:utf-8
import asyncio
import logging
import time
import datetime
import telethon
from telethon import TelegramClient , events, sync
from telethon.tl.functions.account import ResetAuthorizationRequest, GetAuthorizationsRequest
from telethon.tl.functions.channels import JoinChannelRequest
from telethon import errors
from telethon.errors import MultiError
from telethon.tl.functions.messages import SendMessageRequest
import xml.etree.ElementTree as ET
# import traceback
import json
# import ctypes
# whnd = ctypes.windll.kernel32.GetConsoleWindow()
# if whnd != 0:
#     ctypes.windll.user32.ShowWindow(whnd, 0)
#     ctypes.windll.kernel32.CloseHandle(whnd)

# 写入日志
def rizhi():
    #https://python3-cookbook.readthedocs.io/zh_CN/latest/c13/p11_add_logging_to_simple_scripts.html
    time_now = datetime.datetime.now()
    logging.basicConfig(
        filename='log1/'+str(time_now.month)+'_'+str(time_now.day)+'.txt',
        level=logging.ERROR
    )
config = {}
with open("config.json", 'r') as f:
    config = json.loads(f.read())

et = ET.parse("text.xml")
text = et.find("text").text
# exit()
# 这里就是在那个网站上注册的  填上去就能换
# https://my.telegram.org/
client  = TelegramClient('登录', config['api_id'], config['api_hash'])
# client  = TelegramClient('login', 1368006, '0c01e40681ffd65816bdb765a67ada94')
client.start()
client.connect()
# 打印群信息
# dialogs = client.get_dialogs()
# my_channel = client.get_entity('https://t.me/FX2_usdt')
# print(my_channel)
# exit()


def get_client(client):
    if client is None:
        print("new login telegrame!")
        client = TelegramClient('登录', config['api_id'], config['api_hash'])
        client.start()
        client.connect()
        return client
    return client


urllist = config['urllist']


def tel_send(url, client):
    try:
        client = get_client(client)
        print("send to: %s" % url)
        client.send_message(url, text)
    except errors.SlowModeWaitError as e:
        print(url + '_SlowModeWaitError_需要等待,此群限制发言', e)
        client.disconnect()
        client = None
    except errors.FloodWaitError as e:
        print(url + '_SlowModeWaitError_需要等待', e.seconds)
        client.disconnect()
        client = None
    except Exception as e:
        print(url + '_其他错误', e)
        logging.info(e)
        client.disconnect()
        client = None
    return client


def tel_run():
    global client
    for url in urllist:
        client = tel_send(url, client)
        time.sleep(config['waiting'])


def jinqun():
    for obj in urllist:
        try:
            client(JoinChannelRequest(obj))
        except:
            logging.info('进群失败：'+obj)
            print('进群失败'+obj)
        time.sleep(20)


if __name__ == "__main__":
    rizhi()
    # logging.info(datetime.datetime.now().hour)
    # jinqun()
    while True:
        tel_run()
        print("finish all!")
        time.sleep(60 * 20)
