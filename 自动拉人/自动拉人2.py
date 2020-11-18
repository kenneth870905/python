#encoding:utf-8
import json
import time

import telethon
from telethon import TelegramClient, events, sync, errors
from telethon.tl.functions.channels import  InviteToChannelRequest
from googletrans import Translator
# import ctypes
# whnd = ctypes.windll.kernel32.GetConsoleWindow()
# if whnd != 0:
#     ctypes.windll.user32.ShowWindow(whnd, 0)
#     ctypes.windll.kernel32.CloseHandle(whnd)


# 这里就是在那个网站上注册的  填上去就能换
# https://my.telegram.org/
config = {}
with open("config.json", 'r', encoding='UTF-8') as f:
    config = json.loads(f.read())




f = open("用户列表.txt")
str = ''
line = f.readline()
while line:
    str+=line
    line = f.readline()
f.close()
userList = str.split('\n')

client  = TelegramClient('登录', config['api_id'], config['api_hash'])
client.start()
client.connect()



def start():
    # 翻译
    translator = Translator()
    for usr in userList:
        print(usr)
        try:
            client(InviteToChannelRequest(
                channel=config['addchannel'],
                users=[usr]
            ))
#             client.send_message(api_channel, text)
        except errors.rpcerrorlist.UserPrivacyRestrictedError as e:
            print('_UserPrivacyRestrictedError_用户个人设置不允许', e)
            time.sleep(2)
            continue
        except errors.rpcerrorlist.PeerFloodError as e:
            print('_put too much requests_加人太多了，请关闭程序，明天再开', e)
            time.sleep(24 * 60 * 60)
        except errors.rpcerrorlist.ChatWriteForbiddenError as e:
            print('_ChatWriteForbiddenError_群里没权限，关闭程序，删除【登录.session】文件,重新登陆', e)
            time.sleep(24 * 60 * 60)
        except errors.SlowModeWaitError as e:
            print('_SlowModeWaitError_需要等待', e)
        except errors.FloodWaitError as e:
            print('_SlowModeWaitError_需要等待', e.seconds)
        except Exception as e:
            print("其他错误:", e)
            print("其他错误:（翻译）", translator.translate('The provided user is not a mutual contact (caused by InviteToChannelRequest)', dest='zh-CN').text)
        time.sleep(config['waiting'])

if __name__ == "__main__":
    start()