import asyncio
import logging
import time
import datetime
import telethon
from telethon import TelegramClient , events, sync

# from telethon.tl.functions.contacts import ResolveUsernameRequest, GetContactsRequest, ImportContactsRequest
# from telethon.tl.types import InputChannelEmpty
# from telethon.tl.types.messages import Messages
# from telethon.tl.types.contacts import Contacts
from telethon.tl import functions
from telethon.tl.functions.contacts import GetContactsRequest, ResolveUsernameRequest
from telethon.tl.functions.messages import SendMessageRequest
import random

import ctypes
whnd = ctypes.windll.kernel32.GetConsoleWindow()
if whnd != 0:
    ctypes.windll.user32.ShowWindow(whnd, 0)
    ctypes.windll.kernel32.CloseHandle(whnd)

# 写入日志
def rizhi():
    #https://python3-cookbook.readthedocs.io/zh_CN/latest/c13/p11_add_logging_to_simple_scripts.html
    time_now = datetime.datetime.now()
    logging.basicConfig(
        filename='log/'+str(time_now.month)+'_'+str(time_now.day)+'.txt',
        level=logging.INFO
    )

api_id = 1368006
api_hash = '0c01e40681ffd65816bdb765a67ada94'
client  = TelegramClient('莞', api_id, api_hash)
client.start()
client.connect()


# 打印群信息
# dialogs = client.get_dialogs()
# my_channel = client.get_entity('https://t.me/FX2_usdt')
# print(my_channel,file=f)

def test():
    logging.info(time.time())
    time_now = datetime.datetime.now()
    logging.info( str(time_now.year)+'-'+str(time_now.now().month)+'-'+str(time_now.day)+" "+str(time_now.hour)+':'+str(time_now.minute))

# 博彩行业交流共享群 1457535120
# 菲律宾Makati pasay餐饮商家群🔥🔥(禁除餐饮广告链接)  1426325196

massage = [
            "大家好啊",
            "好无聊啊",
            "哀家来打个招呼",
            "(#^.^#)",
            "我来报个到",
            '烦呀烦。。。',
            '都在上班吗？',
            "睡觉了",
            "同志们好",
            '和一MM争论鲸鱼是不是鱼，最后我说“日本人也带个人字”，她这才同意鲸鱼不是鱼。',
            '有一句话憋在我心里已经有很久了，一直没机会说，一直在你家门口徘徊，远远的眺望着你，关注你，在此期间，我痛苦过，挣扎过，我决定在今天向你说出我内心的煎熬：领导，上次吃饭的发票你给报销了吧!要不今晚你请客。',
            ' 哥们，还没打着工作吧!正好我最近发现一职位很适合你，简直是为你量身定做的，我已经帮你报名了，就是去项羽军营里当伙夫，职责就是提桶，打饭，简称饭桶夫!记得去面试啊。看到这短信后，大声对天空喊三声：我是饭桶!你就穿越到项羽军营区了，祝你好运',
            '我最喜欢你的大眼睛，是那么机灵可爱，我最喜欢你的柔软发，是那么光滑莹亮，我最喜欢你的好嗓音，是那么清脆悦耳：喵喵喵...如果你开心了，记得用你柔软的小手转发一下我的信息哦...',
            '正月吃得美，2月不减肥，3月肉成堆，4月少人追，5月情人吹，6月坐家内，7月更加肥，8月会自卑，9月无三围，10月剩悲催。还在看短信呢?快快去减肥!',
            '记得我们上学的时候，大家都叫你“猪才怪”，叫的次数多了，你感觉无法忍受，终于有一天，当一个同学再次叫你外号的时候，你爆发了：我不是猪才怪!',
            ' 如果有一天我们一起乘船远航，忽然遭遇狂风暴浪，你被卷入海中，我一定会奋不顾身地下去救你，不然你身上揣的那些现金可就浪费了...祝你开怀一笑!',
            '领导为单位选对联。上联：白加黑星期六保证不休息;下联：五加二星期天休息不保证;横批：拼命实干!祝愿看到短信的人自我加压，钞票多拿。',
            '某新兵营，班长：华军，为什么你的棉被总叠得比窦兵差?华军：报告，窦兵入伍前是做豆腐的，而我参军前是做花卷馒头的。',
            '小伴侣嗓门特别大，主人叮嘱，今晚来的都是有身份的人，说话务必小声一点。吃完饭，主人客人玩牌，小伴侣收拾完想早点休息，于是凑近男主人耳边轻声道：”那我先睡了哈',
            '我在办公室边上猫扑大杂烩边擦唇膏，不小心没拿住，正好今天穿的是很宽松的背带裤，于是它掉进裤子里了，然后突然推门进来的老板很惊诧地看见我从裤裆部位拿出一支长度和粗细都很值得怀疑的小棒子',
            '唐僧西行遇一女妖，观其乳丰臀肥，故欲行房事，女妖见状惊呼：长老！小女月经在身恐有行房不便！唐僧听罢双手合一道：阿弥陀佛，贫僧正为取经而来！',
            '丈夫回家看到妻子与医生正躺在床上。医生：别误会，我在给她量体温。丈夫：若你插入我老婆身体的那东西没有刻度的话，你就死定了',
            '夫妻与幼儿同住，夜半****，突然发现儿子不见，忙寻之，原来抱膝蹲在门后。夫曰：“快回来，门后风大。”儿愤曰：“少骗人，被窝里风更大',
            '傻子娶妻半年无子,公爹问儿办事没有,儿不懂,父说用你身体最硬的地方撞你媳妇撒尿的地方.次日儿媳夫对公说:你儿子疯了,他用脑袋撞了一晚上尿盆子',
            '人生啊、总是要有些哲理的……生活就象被强暴：要么反抗要么就去享受；工作就像嫖妓:你不行就让别人上；社会就像****:所有的都要靠自己的双手解决',
            '两个历史系老师结婚,且都是二婚;入洞房后,女出上联求下联:夜袭珍珠港,美人受惊(精);男巧对:两颗原子弹,日德(得)投降;横批:二次大战!',
            '公鸡出差一个月,回来后听说鹌鹑没事老来,公鸡怀疑.过两天母鸡生了个鹌鹑蛋,公鸡大怒,母鸡慌忙解释:是早产啦!',
            '一光棍洞房花烛夜后，新娘艰难地扶着墙出来，骂到：“骗子，他说他有三十年的积蓄，我还以为是钱呢！！',
            '一留美学生探亲回家吹牛:美国工厂技术先进,活猪送进去,推出来的是香肠！其父见其崇洋媚外很生气,曰:我跟你妈更厉害,我香肠推进去,出来的是活猪！',
            "有次爸爸出差,小宝贝就只好跟妈妈一起洗澡! 洗完之后,小宝贝严肃的和妈妈说:'妈妈,以后帮我洗澡的时候,不要再碰我的小JJ了!' 妈妈一脸疑惑的问:'为什么?' 小宝贝说:'你把自己的都玩没了,又来玩我的!～",
            "女秘书因工作出色，在老板的撮合下，她和一名能干的职员结了婚。初夜：新郎：小声点儿，别人听到了多难为情！新娘：你说话怎么和老板一样呀",
            "医生：布朗太太，我要告诉你一个好消息。 布朗：好消息？那太好了！但是您应该说“布朗小姐”，不是“布朗太太”。医生：布朗小姐，我要告诉你一个坏消息。",
            "我：“卧槽！你拉的屎形状和我拉得一样，咱们两个撞屎了！”室在：“你能别这么恶心吗？”我：“那你TM以后能记得冲厕所么。。。",
            "单位来了一清纯小女生，为了欢迎，组织去ktv happy。一哥们点了一首颇有难度的歌，飙完高音后，对小女生说：“你看我屌不？”这女孩脸一红：“不看”",
            "正方形和长方形逛街，迎面走来三角形，正方形小声地说：“你看，前面那个肯定是小姐。”长方形纳闷：“你怎么知道的？” 正方形得意地说：“因为他是等鞭三角形啊！”",
            "我问单身哥们：什么事情让你觉得自己越来越老了。哥们：发现一卷纸越来越耐用了。",
            "今天跟两个女MM一起去玩，我说我跟后面跟着，免得给你们丢脸。然后她说跟着好啊，可以做护花使者。我当时就在想“你们后面能有什么花呢？”。。。",
            "“你有病啊！”“你有药啊！”“你有什么病我就有什么药！”“你有什么药我就有什么病！”“我有伟哥。”",
            "昨晚和男友吵架了一架，今天早上大夷妈来了，男友哄我说：咋了还能气吐血了呀。",
            "结婚多年，睡到半夜，老公突然转过身紧紧抱住老婆说，老婆：这辈子太短了，老婆醒了过来，听到老公这句话，感动的掉下了泪水，老公接着说：我都他妈盖不到脚。",
            "记得高中时候老师正在上课，突然手机想了，老师很犹豫要不要接，同学们就说“老师，出去接吧！”但老师仍旧犹豫，这时候二货同桌来了句话，让全班沸腾了:“怎么的，要不我们出去您在屋里接？”",
            "上午上一老师的课，老师很严很八婆，同桌大姨妈漏了，从桌洞里掏出一包卫生巾，新的一包，“喳”的一撕，没想到老师一个健步过来夺了过去，阴阳怪气道：“吃的啥好吃的，给老师一点啊？”，于是。。",
    ]

urllist = [
    # {'url': "https://t.me/TG128", 'msg': "😝😝😝😝"},
    {'url': "https://t.me/TG7788", 'msg': "😝😝😝😝"},
    {'url': "https://t.me/susu622",'msg':'有没有想找美女的啊？需要的密我\nhttps://t.me/GuanShiFuWu','name':"菲律宾★招嫖鉴黄总站"},
    {'url': "https://t.me/hhdd58", 'msg':"有没有想找美女的啊？有的密我",'name':"菲律宾Makati pasay餐饮商家群🔥🔥"},
    # {'url': "https://t.me/bodu365bocai", 'msg': "有没有想找美女的啊？有的密我", 'name':"博度365博彩行业交流（禁黄 禁硬广"},
    {'url': "https://t.me/SYH6969", 'msg': "有没有想找美女的啊？有的密我", 'name': "菲律宾★华人联盟"},
    {'url': "https://t.me/TG188188", 'msg': "有没有想找美女的啊？有的密我", 'name': "菲凡社区🌸菲律宾华人/狗推交流互助"},
    {'url': "https://t.me/bodu123456", 'msg': "有没有想找美女的啊？有的密我", 'name': "扇贝吐水夫妻互换鉴黄交流群"},
    {'url': "https://t.me/FX2_usdt", 'msg': "有没有想找美女的啊？有的密我", 'name': "风行OTC/usd/btc资金漂白"},
    {'url': "https://t.me/waimaimeishimanila", 'msg': "有没有想找美女的啊？有的密我", 'name': "外卖 美食 换汇 马尼拉"},
    # {'url': "https://t.me/ResourcesInPH", 'msg': "有没有想找美女的啊？需要的密我\nhttps://t.me/GuanShiFuWu", 'name': "在菲：資源交換（廣告群）"},  这个要等
    {'url': "https://t.me/SYH669", 'msg': "有没有想找美女的啊\nhttps://t.me/GuanShiFuWu", 'name': "菲律宾★菲嫖不可娱乐群"},
    {'url': "https://t.me/dd322", 'msg': "有没有想找美女的啊？有的密我", 'name': "香烟槟榔面膜美食/手机/卡/笔记本/电脑"},
    {'url': "https://t.me/PPGOO", 'msg': "有没有人想我啊", 'name': "狗推客服人事★交流群【禁广告】"},
    {'url': "https://t.me/bwg01", 'msg': "需要安排的密我", 'name': "🏛 “博”物管 🔍/聊天吹水/生活互助/外卖"},
    {'url': "https://t.me/susu521", 'msg': "😝😝😝😝", 'name': "狗推🔥全网娱乐中心"},
    {'url': "https://t.me/Liugezhashuai", 'msg': "😝😝😝需要安排的密我", 'name': "菲律宾美食外卖交流"},
    {'url': "https://t.me/wmmsq", 'msg': "😝😝😝需要安排的密我", 'name': "Pasay Makati 外卖美食群(🈲外卖以"},
    {'url': "https://t.me/bmhhq3", 'msg': "😝😝😝需要安排的密我", 'name': "便民群-换汇群（🈲广告）"},
    {'url': "https://t.me/dou1687", 'msg': "😝😝😝需要安排的密我", 'name': "全菲能力甩人交流群（禁止打 广告发链"},
    {'url': "https://t.me/SU9899", 'msg': "😝😝😝大家好啊", 'name': "菲律宾★狗推人事联盟💋匆匆那年【禁广告】"},
    {'url': "https://t.me/HWC689", 'msg': "😝😝😝", 'name': "菲律宾💋青春年华🌹交友闲聊💖【禁"},
    {'url': "https://t.me/TG550", 'msg': "😝😝😝需要安排的密我", 'name': "狗推俱乐部"},
    {'url': "https://t.me/sdynews", 'msg': "😝😝😝需要安排的密我", 'name': "昇得源-菜农特工讨论群"},
    {'url': "https://t.me/TG222", 'msg': "😝😝😝需要安排的密我", 'name': ""},
    {'url': "https://t.me/TGhr88", 'msg': "😝😝😝需要安排的密我", 'name': ""},
    {'url': "https://t.me/aabbccmmm", 'msg': "需要小妹的密我", 'name': ""},
    {'url': "https://t.me/chwlmm", 'msg': "需要小妹的密我", 'name': ""},
    {'url': "https://t.me/bwjl51", 'msg': "需要小妹的密我", 'name': ""},
    {'url': "https://t.me/DongDTB", 'msg': "😝😝😝", 'name': ""},
    # {'url': "https://t.me/TG928", 'msg': "需要小妹的密我", 'name': ""},
    {'url': "https://t.me/piseo2rmb", 'msg': "需要小妹的密我", 'name': ""},
    {'url': "phxiaoM",'msg':"定时消息测试，不用管"},
    # {'url': "", 'msg': "", 'name': ""},
    # {'url': "", 'msg': "", 'name': ""},
]
# https://t.me/GuanShiFuWu


def startAll():
    for obj in urllist:
        try:
            client(SendMessageRequest(obj['url'], obj['msg'] ))
        except Exception as e:
            logging.error(obj['url'])
            logging.error(e)
        time.sleep(10)

def 打招呼():
    for obj in urllist:
        try:
            client(SendMessageRequest(obj['url'], massage[random.randint(0, len(massage))-1] ))
        except Exception as e:
            logging.error(obj['url'])
            logging.error(e)
        time.sleep(10)
    # # client(SendMessageRequest('', '有没有需要小妹的啊？需要的密我'))

if __name__ == "__main__":
    rizhi()
    logging.info(datetime.datetime.now().hour)
    # 打招呼()
    # time.sleep(60* 10 * 1)
    # while True:
    hour_now = datetime.datetime.now().hour
    if (hour_now > 12 and hour_now<24) or hour_now < 3 :
        if hour_now % 2 == 0:
            startAll()
        else:
            打招呼()
        # time.sleep(60 * 60 * 1)
    # else:
        # time.sleep(60* 10 * 1)


