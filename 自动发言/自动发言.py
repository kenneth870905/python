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
# import traceback
import json
import ctypes
whnd = ctypes.windll.kernel32.GetConsoleWindow()
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
with open("config.json", 'r', encoding='UTF-8') as f:
    config = json.loads(f.read())
msg = config['text']

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

urllist = config['urllist']


text ="""
    🏆⚽️亚博集团总部直招！🥇🥇🥇

💰丰厚年终奖🍹饮料🍬槟榔无限提供！仅餐补房补即超4000RMB！ 
-----------------------------
❤️诚聘优才（远超同行的薪酬‼️）
1）推广➕电销专员/组长/主管；
2）淘宝运营、自媒体运营等；
3）ios、Android、前端、PHP、技术总监、渗透、劫持等技术岗；
4）seo、sem不限量；
5）人事专员/组长/主管。
🈲限制：福建省 河南新乡 山东威海

🏅🏅🏅公司优势👇👇👇 
1️⃣人员规模10000+人，管理规范赔付透明！年净利超百亿！实力雄厚！
2️⃣远超同行的薪酬福利待遇！业绩岗、技术岗百万年薪等你来拿！💸
3️⃣至今全集团新冠0感染！若员工罹患，集团将全资治疗到底！🏥🏥🏥

开户网址： www.1319yb.com
更多详情请联系： @YBHR_xiaoj
此号不回复
"""


async def 发言(url):
    print(url)
    try:
        await client(SendMessageRequest(url, msg))
    except errors.SlowModeWaitError as e:
        print(url+'_SlowModeWaitError_需要等待,可以尝试删除此群', e)
        await asyncio.sleep(e.seconds+10)
        # await 发言(url)
    except errors.FloodWaitError as e:
        print(url+'_SlowModeWaitError_需要等待',e.seconds)
        await asyncio.sleep(e.seconds+10)
        # await 发言(url)
    except Exception as e:
        print(url+'_其他错误', e)

async def startAll(i=0) :

    for url in urllist:
        await 发言(url)
        await asyncio.sleep(10)

def 进群():
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
    # 进群()
    while True:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(startAll())
        time.sleep(60*20)

