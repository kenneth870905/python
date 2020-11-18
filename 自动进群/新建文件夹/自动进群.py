#encoding:utf-8
import json
import time

import telethon
from telethon import TelegramClient , events, sync
from telethon.tl.functions.account import ResetAuthorizationRequest, GetAuthorizationsRequest
from telethon.tl.functions.channels import JoinChannelRequest
from telethon import errors
from telethon.errors import MultiError
from telethon.tl.functions.messages import SendMessageRequest

config = {}
with open("config.json", 'r') as f:
    config = json.loads(f.read())
urllist = config['urllist']

client  = TelegramClient('登录', config['api_id'], config['api_hash'])
client.start()
client.connect()

def 进群1(url):
    print(url)
    try:
        client(JoinChannelRequest(url))
    except errors.FloodWaitError as e:
        print('需要等待才能进入下个群:', e.seconds)
        time.sleep(e.seconds + 5)
    except Exception as e:
        print('其他错误',e)

    # if ok == False:
    #     进群1(url)

def 进群():
    for url in urllist:
        进群1(url)
        time.sleep(10)

if __name__ == "__main__":
    进群()

