#!/usr/bin/python3
# import pymysql
import datetime
import time
# import asyncio
# 定时器 避免阻塞
import threading
# 调用接口
import requests
import json
import hashlib

# 日志
from log import make_print_to_file


def setToken():
    t = datetime.datetime.now().strftime('%Y%m%d%H%M')
    # 创建md5对象
    hl = hashlib.md5()
    hl.update(t.encode(encoding='utf-8'))
    str1 = hl.hexdigest()+'abcdefg1234567'
    # 创建md5对象  一定要分开创建2次，，不然会出错
    h2 = hashlib.md5()
    h2.update( str1.encode(encoding='utf-8') )
    str2 = h2.hexdigest()
    return str2

class allRecording():
    def __init__(self):
        self.api = 'https://his.duomaids.com'
        # self.api_2 = 'http://127.0.0.1/php/aomenlhc'
        self.api_2 = 'http://kj00853.app/'
        
        # 数据库已保存参数
        self.CurrentInfo =  {
            # "issue":'当前',
            # 'lastIssue':'上期'
        }

        # 获取最新
        # 已获取次数
        self.n1 = 0
        # 失败或没有结果间隔时间 秒
        self.t1 = 30
        # 最多调用次数 
        self.max1 = 5
        
        #指定期数开奖
        self.n2 = 0
        self.t2 = 60
        self.max2 = 50

        # 获取我们数据库次数
        self.n3 = 0
    
    # 获取数据库现有配置
    def getWeCurrentInfo(self):
        requests.get(self.api_2 + '/api.php?Update=resetNew&token='+setToken(), '', headers={'content-type': 'application/json'})
        res =  requests.get(self.api_2 + '/api.php?action=CurrentInfo', '', headers={'content-type': 'application/json'})
        if res.status_code == 200 :
            self.CurrentInfo = json.loads(res.text)
            print('数据库现有结果',self.CurrentInfo)
            self.n3 = 0
            # self.CurrentInfo = {'id': '1', 'issue': '2021125', 'lastIssue': '2021124'}
        else:
            print('获取数据库CurrentInfo返回值错误')
            if self.n3 < 10:
                time.sleep(10)
                self.n3 = self.n3+1
                self.getWeCurrentInfo()
    # 更新数据库配置
    def updateCurrentInfo(self):
        res =  requests.post( self.api_2 + '/api.php?Update=CurrentInfo&token='+setToken(), json=self.CurrentInfo ,headers={'content-type': 'application/json'})
        if res.status_code == 200:
            resJson = json.loads(res.text)
            print(resJson)
            self.n3 = 0
        else:
            print('更新数据库CurrentInfo返回值错误')
            if self.n3 < 10:
                time.sleep(10)
                self.n3 = self.n3+1
                self.updateCurrentInfo()

    # 更新开奖结果
    def updateHistory(self,data):
        print('更新开奖结果',data)
        res =  requests.post(self.api_2 + '/api.php?Update=IssueOpenInfo&token='+setToken(), json=data ,headers={'content-type': 'application/json'})
        if res.status_code==200:
            self.n3 = 0
            resJson = json.loads(res.text)
            print(resJson)
        else:
            print('更新开奖结果失败')
            if self.n3 < 10:
                time.sleep(10)
                self.n3 = self.n3+1
                self.updateHistory(data)


    def start(self):
        # 获取数据库现有数据
        self.getWeCurrentInfo()
            
        # 获取开奖配置
        self.getCurrentInfo()
        
        # 获取指定期数开奖信息
        self.IssueOpenInfo()

    # 获取开奖配置
    def getCurrentInfo(self):
        print('获取开奖配置')
        # 查询已保存结果
        res = requests.post(self.api+'/api/CurrentInfo', json={"lotteryId": 2032}, headers={'content-type': 'application/json'})
        if (res.status_code == 200 ):
            resjson = json.loads(res.text)
            # print('接口返回值',resjson)
            if resjson['code'] == 0:
                data = resjson['data']
                
                if  str(self.CurrentInfo['issue']) != data['issue']:
                    sql = "UPDATE `CurrentInfo` SET `issue`='"+data['issue']+"',`lastIssue`='"+data['lastIssue']+"' WHERE 1"
                    self.CurrentInfo = {'issue':data['issue'],'lastIssue':data['lastIssue']} 
                    print('拿到最新获取开奖配置',self.CurrentInfo)
                    # 更新 CurrentInfo 添加到数据库
                    self.updateCurrentInfo()
                else:
                    print('没有拿到最新获取开奖配置')
                    if self.n1 < self.max1:
                        time.sleep(self.t1)
                        self.n1 = self.n1+1
                        self.getCurrentInfo()
        else:
            print('获取获取开奖配置返回值错误')
            if self.n1 < self.max1:
                time.sleep(self.t1)
                self.n1 = self.n1+1
                self.getCurrentInfo()
    
    # 获取指定期数开奖信息
    def IssueOpenInfo(self):
        print('获取最新开奖信息')
        res =  requests.post(self.api+'/api/IssueOpenInfo', json={'lotteryId': 2032, 'issue': self.CurrentInfo['lastIssue']},headers={'content-type': 'application/json'})
        if (res.status_code == 200 ):
            resjson = json.loads(res.text)
            if resjson['code']==0:
                x = resjson['data']
                t = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                data = {'period':x['issue'],'content':x['openCode'],'period':x['issue'],'t':t,'video':'/lottery/video/2021/2032/'+self.CurrentInfo['lastIssue']+'.mp4'}
                # 更新最新开奖结果
                self.updateHistory(data)
                if x['openCode']:
                    print('执行完毕等待明天继续执行')
                else:
                    print('开奖结果为空需要再次获取')
                    if self.n2 < self.max2:
                        time.sleep(self.t2)
                        self.n2 = self.n2+1
                        self.IssueOpenInfo()
            else:
                if self.n2 < self.max2:
                    time.sleep(self.t2)
                    self.n2 = self.n2+1
                    self.IssueOpenInfo()
        else:
            print('获取IssueOpenInfof返回值错误')
            if self.n2 < self.max2:
                time.sleep(self.t2)
                self.n2 = self.n2+1
                self.IssueOpenInfo()


def start():
    xianZai = datetime.datetime.now().timestamp()
    xianZai = int(xianZai)
    #今晚21：30 时间戳
    openTime = ' 21:16'
    # openTime = ' 08:53'
    jinWan =  datetime.datetime.strptime(str(datetime.date.today())+openTime, '%Y-%m-%d %H:%M').timestamp()
    jinWan = int(jinWan)
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
    

   
    # new_get = allRecording()
    # thread = threading.Thread(target=new_get.start)
    # thread.start()
    # return
    
    print('开始123')
    if t1<60 or t1> 60*60*23.5:
        # 防止阻塞
        new_get = allRecording()
        thread = threading.Thread(target=new_get.start)
        thread.start()

    print('开始执行需要等待：',t1)
    if  t1> 60*60 * 1:
        print('一小时后检测一下防止时间偏差过大')
        time.sleep(60*60)
    else:
        print('正在等待',t1)
        time.sleep(t1)
    start()


if __name__ == "__main__":
    make_print_to_file(path='./log')
    # thread = threading.Thread(target=start)
    # thread.start()
    start()



# 安装依赖  python -m pip install b包名
# 运行
# python /root/aomenlhc/start.py >> /root/aomenlhc/my.log 2>&1 &
# nohup python start.py >> my.log 2>&1 &
# nohup python start.py 2>&1 &
# nohup python start.py 2
# nohup python start.py &
# 查看
# ps -aux | grep "start.py"
# 结束
# kill 查询出来的id






