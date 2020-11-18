#encoding:utf-8
import json
import threading
import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters
from telepot.loop import MessageLoop

config = {}
with open("config.json", 'r') as f:
    config = json.loads(f.read())
str = config['text']
image = config['image']
TOKEN = config['TOKEN']

# str = """🏆⚽️亚博集团总部直招！🥇🥇🥇
#
# 💰丰厚年终奖🍹饮料🍬槟榔无限提供！仅餐补房补即超4000RMB！
# -----------------------------
# ❤️诚聘优才（远超同行的薪酬‼️）
# 1）推广➕电销专员/组长/主管；
# 2）淘宝运营、自媒体运营等；
# 3）ios、Android、前端、PHP、技术总监、渗透、劫持等技术岗；
# 4）seo、sem不限量；
# 5）人事专员/组长/主管。
# 🈲限制：福建省 河南新乡 山东威海
#
# 🏅🏅🏅公司优势👇👇👇
# 1️⃣人员规模10000+人，管理规范赔付透明！年净利超百亿！实力雄厚！
# 2⃣️远超同行的薪酬福利待遇！业绩岗、技术岗百万年薪等你来拿！💸
# 3⃣️至今全集团新冠0感染！若员工罹患，集团将全资治疗到底！🏥🏥🏥
#
# 开户网址： www.1319yb.com
# 更多详情请联系： @YBHR_xiaoj
#                 """


# TOKEN='1310502105:AAGxENCeAetw6EYj4yC04bWhnTiBT7luoc4'我选中那里 点开就又运行一个了 是吧
# 这个是你的机器人的编码。
# TOKEN="1049741563:AAG7PCHkwthTOpL7gdJnCvoUEhvk9alhgcg"

def a(update,context):
    keyboard = [
        [InlineKeyboardButton('❤聊天交友❤', callback_data='help',url="https://t.me/bwg01"),
         InlineKeyboardButton('❤甩人曝光❤', callback_data='help',url="https://t.me/bwg02")],
        [InlineKeyboardButton('❤点歌频道❤', callback_data='help', url="https://t.me/yabo0007"),
         InlineKeyboardButton('❤鉴黄开车❤', callback_data='help', url="https://t.me/kaichezhongxin")],
        #[InlineKeyboardButton('🥰点歌频道🥰', callback_data='help', url="https://t.me/yabo0007"),备用跳转
        # [InlineKeyboardButton('🥰预留🥰', callback_data='help', url="https://t.me/yabo0007")],
        #[InlineKeyboardButton('🥰预留🥰', callback_data='help', url="https://t.me/yabo0007"),
         [InlineKeyboardButton('⭐⚡顶级企业最高待遇诚聘优才⭐⚡', callback_data='help', url="https://t.me/yabo0007")],
    ]

    # r = update.message.reply_text(str, reply_markup=InlineKeyboardMarkup(keyboard))
    r = update.message.reply_photo(image,caption=str,reply_markup=InlineKeyboardMarkup(keyboard))
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
