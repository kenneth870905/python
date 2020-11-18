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
import threading

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
config_dict = {"text": text, "api_id": config['api_id'], "api_hash": config['api_hash'], "waiting": config['waiting']}


class SendThread(threading.Thread):
    def __init__(self, param_dict, config_dict):
        super(SendThread, self).__init__()
        self.param = param_dict
        self.config = config_dict
        self.client = None

    def run(self):
        print("start run new thread!")
        while len(self.param["url_list"]) > 0:
            url = self.param["url_list"].pop()
            self.param["count"] -= 1
            self.tel_send(url)
            self.param["up_time"] = time.time()
        self.param["finish"] = True

    def stop(self):
        self.stopped = True

    def get_client(self):
        if self.client is None:
            print("login telegrame!")
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            # 这里就是在那个网站上注册的  填上去就能换
            # https://my.telegram.org/
            client = TelegramClient('登录', self.config['api_id'], self.config['api_hash'])
            client.start()
            client.connect()
            self.client = client

    def tel_send(self, url):
        try:
            self.get_client()
            print("send to: %s, 还剩:%s" % (url, self.param["count"]))
            self.client.send_message(url, self.config["text"])
            self.dis_connect()
        except errors.ChatWriteForbiddenError as e:
            print(url + '此群没有发言权限', e)
            return
        except errors.SlowModeWaitError as e:
            print(url + '_SlowModeWaitError_需要等待,此群限制发言', e)
            self.dis_connect()
        except errors.FloodWaitError as e:
            print(url + '_SlowModeWaitError_需要等待', e.seconds)
            self.dis_connect()
        except Exception as e:
            print(url + '_其他错误', e)
            self.dis_connect()
        time.sleep(self.config['waiting'])

    def dis_connect(self):
        if self.client:
            self.client.disconnect()
            self.client = None


def tel_run():
    try:
        param_dict = {"url_list": config['urllist'].copy(), "up_time": time.time(), "finish": False, "count": len(config['urllist'])}
        new_thread = SendThread(param_dict, config_dict)
        new_thread.start()

        等待时间 = time.time()
        while True:
            time.sleep(10)

            if param_dict["finish"]:
                print("finish all %s!" % param_dict["count"])
                if new_thread.client:
                    new_thread.dis_connect()
                new_thread.stop()
                break
            # sub_sec = int(time.time() - param_dict["up_time"])
            sub_sec =int(time.time() - 等待时间)
            等待时间 = time.time()
            print('距离上次发言',sub_sec)
            # print("已等待:%s" % sub_sec)
            if sub_sec > 150:
                try:
                    if new_thread.client:
                        new_thread.dis_connect()
                    new_thread.stop()
                    new_thread = SendThread(param_dict, config_dict)
                    new_thread.start()
                except Exception as e:
                    print('_重开线程错误', e)
    except Exception as e:
        print('_运行错误', e)


if __name__ == "__main__":
    rizhi()
    # print(config['循环分钟'])
    while True:
        tel_run()
        time.sleep(60 * config['循环分钟'])
