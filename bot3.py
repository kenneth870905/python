#encoding:utf-8
import threading
import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters
from telepot.loop import MessageLoop

TOKEN='1310502105:AAGxENCeAetw6EYj4yC04bWhnTiBT7luoc4'
# 这个是你的机器人的编码。
# TOKEN="1049741563:AAG7PCHkwthTOpL7gdJnCvoUEhvk9alhgcg"

def a(update,context):
    keyboard = [
        [InlineKeyboardButton('❤聊天交友❤', callback_data='help',url="https://t.me/bwg01"), InlineKeyboardButton('❤甩人 曝光❤', callback_data='help',url="https://t.me/bwg02")],
        [InlineKeyboardButton('❤点歌频道❤', callback_data='help', url="https://t.me/yabo0007"), InlineKeyboardButton('❤详情咨询❤', callback_data='help', url="https://t.me/YBHR_xiaoj")],
        #[InlineKeyboardButton('🥰点歌频道🥰', callback_data='help', url="https://t.me/yabo0007"),备用跳转
        # InlineKeyboardButton('🥰预留🥰', callback_data='help', url="https://t.me/yabo0007")],
        #[InlineKeyboardButton('🥰预留🥰', callback_data='help', url="https://t.me/yabo0007"),
         [InlineKeyboardButton('⭐⚡顶级企业最高待遇诚聘优才⭐⚡', callback_data='help', url="https://t.me/yabo0007")],
    ]
    str="""亚博集团总部直招！
不坑不黑不骗不压不扣！    
月薪1万RMB的人叫你不要去亚博，那是因为他们想象不到单单餐补房补就超过4000RMB是什么概念。
不是你想象中的亚博，亚博超乎你的想象！ 
菠菜行业👉🏻业内排名前3️⃣！享受年终13-16薪💰及年终奖🎉饮料槟榔无限提供！
-----------------------------
  🛑诚聘优才：
人事专员/人事主管、推广专员/推广主管 人事助理 、ios、安卓    seo团队 推广团队 电销团队  自媒体运营 电竞体育主播   

🈲限制地区：
福建全省  河南新乡 山东威海    

公司优势👇👇👇 
1️⃣公司规模10000+人，不会倒闭，稳定可靠。 
2️⃣管理规范，赔付透明，员工若罹患新冠，公司全资治疗，目前公司同事感染率为0 
3️⃣完善的晋升培训体系，亚博愿与你共同成长、携手共赢。远高于同行业的薪酬福利待遇，业绩岗、技术岗百万年薪等你来拿！ 🚫限制地区：福建全省  河南新乡 山东威海 以人为本，关心每位亚博人。
代理连接：http://www.baidu.com/
更多岗位请联系HR负责人： @YBHR_xiaoj
                """
    # r = update.message.reply_text(str, reply_markup=InlineKeyboardMarkup(keyboard))
    r = update.message.reply_photo("https://t.me/bottest1234561/1252",caption=str,reply_markup=InlineKeyboardMarkup(keyboard))
    # sleep(30)
    print(r.chat.id,r.message_id)
    # 这里是修改时间的地方（20）
    t = threading.Timer(30, deleteMsg, (r.chat.id,r.message_id))
    t.start()
    # bot.delete_message(chat_id=r.chat.id, message_id=r.message_id)
def deleteMsg(chat_id,message_id):
    print(chat_id,message_id)
    bot.delete_message(chat_id=chat_id, message_id=message_id)

def echo(update, context):
    # print(update)
    if update.message.new_chat_members:
        for new_member in update.message.new_chat_members:
            r = a(update,context)


def filterText(update, context):
    # print('收到消息')
    if update.message.text.startswith('欢迎：') or update.message.text.startswith('欢迎:'):
        r = bot.get_chat_member(user_id=update.message.from_user.id, chat_id=update.message.chat.id)
        if r.status== 'creator' or r.status =='administrator':
            a(update,context)
        else:
            update.message.reply_text('你不是管理员')

bot = telegram.Bot(TOKEN)
updater = Updater(TOKEN, use_context=True)
# updater = telegram.Bot('1310502105:AAGxENCeAetw6EYj4yC04bWhnTiBT7luoc4')
# updater.dispatcher.add_handler(CommandHandler("a",a))
# updater.dispatcher.add_handler(CallbackQueryHandler(help, pattern='help'))
# updater.dispatcher.add_handler(CallbackQueryHandler(go, pattern='go'))
updater.dispatcher.add_handler(MessageHandler(Filters.status_update,echo))
updater.dispatcher.add_handler(MessageHandler(Filters.text,filterText))

updater.start_polling()
# updater.idle()
