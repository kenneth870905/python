#!/usr/bin/python3
import pymysql
import datetime
import time
import asyncio
# 定时器 时避免 阻塞
import threading
# 调用接口
import requests
import json
import os


# db = pymysql.connect(host="172.247.253.212",user="aomen",passwd="L4pFB8azHMLnG3TJ",database="aomen")
# cursor = db.cursor(cursor=pymysql.cursors.DictCursor)



# 首次执行
oneGet=True

class allRecording():
    def __init__(self):
        self.api = 'https://his.duomaids.com'
        # 数据库已保存参数
        self.CurrentInfo =  {
            # "issue":'当前',
            # 'lastIssue':'上期'
        }

        # 获取最新
        # 已获取次数
        self.n1 = 0
        # 失败或没有结果间隔时间 
        self.t1 = 5
        # 最多调用5次 
        self.max1 = 5
        
        #获取近期开奖结果
        self.n2 = 0
        self.t2 = 2
        self.max2 = 5
         
    # async def start(self):
    def start(self):

        # res =  requests.get('http://127.0.0.1/php/aomenlhc/api.php?action=CurrentInfo', '', headers={'content-type': 'application/json'})
        # if (res.status_code == 200 ):
        #     self.CurrentInfo = json.loads(res.text)
        #     print('数据库现有结果',self.CurrentInfo)

        self.CurrentInfo = {'id': '1', 'issue': '2021125', 'lastIssue': '2021124'}
        print(self.CurrentInfo['issue'])

        # 更新CurrentInfo
        # res =  requests.post('http://127.0.0.1/php/aomenlhc/api.php?Update=CurrentInfo', json={'id': '1', 'issue': '2021125', 'lastIssue': '2021124'},headers={'content-type': 'application/json'})
        # resJson = json.loads(res.text)
        # print(resJson)
        
        # 获取开奖信息
        res =  requests.post(self.api+'/api/IssueOpenInfo', json={'lotteryId': 2032, 'issue': '2021124'},headers={'content-type': 'application/json'})
        


        return

        # 等上面完成了在走下面的
        # 获取近期开奖
        t2 = threading.Thread(target=self.opencode)
        t2.start()

        # 获取开奖记录  基本上只运行一次就好了
        print('oneGet',oneGet)
        if oneGet==True:
            t3 = threading.Thread(target=self.HistoryOpenInfo)
            # t3.start()
            

    # 获取开奖信息
    def getCurrentInfo(self):
        print('获取开奖信息')
        # 查询已保存结果
        res = requests.post(self.api+'/api/CurrentInfo', json={"lotteryId": 2032}, headers={'content-type': 'application/json'})
        if (res.status_code == 200 ):
            resjson = json.loads(res.text)
            # print('接口返回值',resjson)
            if resjson['code'] == 0:
                data = resjson['data']
                
                if  str(self.CurrentInfo['issue']) != data['issue']:
                    sql = "UPDATE `CurrentInfo` SET `issue`='"+data['issue']+"',`lastIssue`='"+data['lastIssue']+"' WHERE 1"
                    print('拿到最新结果')
                    self.CurrentInfo = {'issue':data['issue'],'lastIssue':data['lastIssue']} 
                    cursor.execute(sql)
                    db.commit()
                else:
                    print('没有拿到最新结果')
                    if self.n1 < self.max1:
                        time.sleep(self.t1)
                        self.n1 = self.n1+1
                        self.getCurrentInfo()
        else:
            print('获取开奖信息返回值错误')
            if self.n1 < self.max1:
                time.sleep(self.t1)
                self.n1 = self.n1+1
                self.getCurrentInfo()
    
    # 获取最近开奖个记录
    def opencode(self):
        print('获取最近开奖记录')
        # 这个接口比较特殊
        res = requests.get('http://api.bjjfnet.com/data/opencode/2032', '', headers={'content-type': 'application/json'})
        if  res.status_code==200:
            resjson = json.loads(res.text)
            if resjson['code']==0:
                data = resjson['data']
                print('获取到上期开奖结果')
                if str(data[0]['issue']) == str(self.CurrentInfo['lastIssue']):
                    sql = "INSERT INTO `history`(period , `content`, `t`) VALUES "
                    # sql = "REPLACE INTO history ( `period` ,`content`,`t`) VALUES "
                    for x in data:
                        sql = sql + "("+x['issue']+",'"+x['openCode']+"','"+x['openTime']+"'),"
                        # 下载文件
                        mp4Download('/lottery/video/2021/2032/'+x['issue']+'.mp4')
                    sql = sql[:-1]
                    sql = sql+"on duplicate key update period=VALUES(period),content=VALUES(content),t=VALUES(t)"
                    # print(sql)
                    cursor.execute(sql)
                    db.commit()

                # 没有获取到最新开奖
                else:
                    if self.n2 < self.max2:
                        time.sleep(self.t2)
                        self.n2 = self.n2+1
                        self.opencode()
        else:
            print('获取最近开奖记录返回值错误')
            if self.n2 < self.max2:
                time.sleep(self.t2)
                self.n2 = self.n2+1
                self.opencode()

    # 获取所有开奖记录
    def HistoryOpenInfo(self):
        print('获取开奖记录')
        issueNum = datetime.datetime.now().strftime('%Y-%m-%d')
        res = requests.post(self.api+'/api/HistoryOpenInfo', json={"lotteryId": 2032,'issueNum':issueNum}, headers={'content-type': 'application/json'})
        if (res.status_code == 200 ):
            resjson = json.loads(res.text)
            if resjson['code']==0:
                data = resjson['data']
                sql = "REPLACE INTO history ( `period` ,`content`,`t`,video) VALUES "
                for x in data:
                    # "+url+"
                    sql = sql + "("+x['issue']+",'"+x['openCode']+"','"+x['openTime']+"','"+x['videoUrl']+"'),"
                    # 文件写入 判断是否存在
                    mp4Download(x['videoUrl'])
                        
                sql = sql[:-1]
                cursor.execute(sql)
                db.commit()

def mp4Download(url):
    if os.path.exists('.'+url)==False:
        print('正在下载mp4',url)
        res = requests.get('https://video-qq.ziyouyizhi.com'+url, '', headers={'Referer':'https://www.macau-jc.com/','content-type': 'video/mp4'})
        if res.status_code==200:
            with open("."+url,'wb') as mp4:
                for chunk in res.iter_content(chunk_size=1024):
                    if chunk:
                        mp4.write(chunk)
    else:
        print('文件已存在无需下载',url)

def start(oneGet):
    xianZai = datetime.datetime.now().timestamp()
    xianZai = int(xianZai)
    #今晚21：15 时间戳
    openTime = ' 21:30'
    jinWan =  datetime.datetime.strptime(str(datetime.date.today())+openTime, '%Y-%m-%d %H:%M').timestamp()
    jinWan = int(jinWan)
    print(jinWan)
    # 明晚 21:15 时间戳
    today = datetime.datetime.strptime(  str( datetime.date.today()+datetime.timedelta(days=1) ) +openTime , '%Y-%m-%d %H:%M').timestamp()
    today = int(today)
    t1 = 0
    if xianZai < jinWan :
        # print('今天还没开奖',xianZai - jinWan)
        t1 = jinWan - xianZai
    else:
        # print('今天已过，等待明天',today - xianZai)
        t1 = today - xianZai
    
    # 一小时后检测一下防止时间偏差过大
    

    if t1<60 or t1> 60*60*23.5 or oneGet:
        # 防止阻塞
        new_get = allRecording()
        thread = threading.Thread(target=new_get.start)
        thread.start()
    return
    print('开始执行需要等待：',t1)
    if  t1> 60*60 * 1:
        print('一小时后检测一下防止时间偏差过大')
        time.sleep(60*60)
    else:
        print('正在等待',t1)
        time.sleep(t1)
    oneGet=False
    start(oneGet)


if __name__ == "__main__":
    # thread = threading.Thread(target=start)
    # thread.start()
    # start(oneGet)

    mp4Download('/lottery/video/2021/2032/2021124.mp4')
    









