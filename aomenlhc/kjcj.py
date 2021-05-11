import requests
import json
import time
import hashlib
import os


def md5(str):
    return hashlib.md5(str.encode(encoding='UTF-8')).hexdigest()


def collect(url, LotteryCode, lastIssueCode, IssueCodePrefix):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
    }
    apiheaders = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
    }
    try:
        html = requests.get(url, headers=headers)
        data = json.loads(html.text)
        IssueCode = data['result']['data'][0]['preDrawIssue']
        Result = data['result']['data'][0]['preDrawCode']
        Result = Result.replace(',', '|')
        if (lastIssueCode != IssueCode):
            lastIssueCode = IssueCode
            try:
                if (IssueCodePrefix != ""):
                    IssueCode = IssueCodePrefix+str(IssueCode)
                elif (LotteryCode == '60001'):
                    IssueCode = str(IssueCode)[0:8]+'0'+str(IssueCode)[8:11]
            except:
                print('类型转换错误')
            t = time.strftime("%Y%m%d%H%M", time.localtime())
            param = {
                'lotterycode': LotteryCode,
                'issuecode': IssueCode,
                'content': Result,
                'source': 'api68',
                'machineid': 'ming',
                'user': md5(md5(md5('ctcaitou123!@#')+md5(t))),
                'date': t
            }
            try:
                html = requests.post(
                    "http://103.249.104.33/api_kj/", param, headers=apiheaders)
                print('103.249.104.33')
                print(html.text)
            except:
                lastIssueCode = 0
                print('连接异常')
            try:
                html = requests.post(
                    "http://103.233.82.50/api_kj/", param, headers=apiheaders)
                print('103.223.82.50')
                print(html.text)
            except:
                lastIssueCode = 0
                print('连接异常')
        # print(IssueCode)
        # print(Result)
        print('等待下一次采集中 '+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    except:
        print('采集出错 稍后继续尝试')
    time.sleep(5)
    return lastIssueCode


CollectList = [
    {
        'url': "http://api.api68.com/pks/getPksHistoryList.do?lotCode=10057",
        'LotteryCode': '20005',
        'lastIssueCode': '0',
        'IssueCodePrefix': ''
    },
    {
        'url': "http://api.apiose122.com/lotteryJSFastThree/getJSFastThreeList.do?lotCode=10007",
        'LotteryCode': '40003',
        'lastIssueCode': '0',
        'IssueCodePrefix': '20'
    },
    {
        'url': "http://api.api68.com/ElevenFive/getElevenFiveList.do?&lotCode=10006",
        'LotteryCode': '60001',
        'lastIssueCode': '0',
        'IssueCodePrefix': ''
    }
]

index = 0
while (1 == 1):
    index += 1
    if (index % 180 == 0):
        os.system('pppoe-stop')
        print('断网等待中')
        time.sleep(30)
        os.system('pppoe-start')
        time.sleep(30)
    for i, v in enumerate(CollectList):
        print('['+CollectList[i]['LotteryCode']+']')
        CollectList[i]['lastIssueCode'] = collect(CollectList[i]['url'], CollectList[i]['LotteryCode'], CollectList[i]['lastIssueCode'], CollectList[i]['IssueCodePrefix'])
    time.sleep(20)
    os.system('clear')
