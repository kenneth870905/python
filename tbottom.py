#encoding:utf-8
from asyncore import dispatcher

import telegram
from telegram import  InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackQueryHandler

update_id = None

def main():
    global update_id
    print(update_id)
    bot = telegram.Bot('1310502105:AAGxENCeAetw6EYj4yC04bWhnTiBT7luoc4')
    echo(bot)
    while True:
        echo(bot)


def echo(bot):
    global update_id
    for update in bot.get_updates(offset=update_id, timeout=10):
        update_id = update.update_id + 1
        print(update)
        if  update.message == '' or not update.message:
            print('meiyou')
            # print(update.callback_query)
            # print(update.callback_query.data)
            if update.callback_query.data=='help':
                print('meiyou132')
                help(bot,update)
                # update.message.reply_text('Welcome1234:')
        else:
            print(update.message.text)
        # update.message.reply_text(update.message.text)
        # return
        if update.message:
            if update.message.text ==1:
                print('1')
                update.message.reply_text('haha')
            else:
                print(2)
                keyboard = [
                            [InlineKeyboardButton('Help', callback_data='help')]
                        ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                update.message.reply_text('欢迎:'+update.message.chat.first_name, reply_markup=reply_markup)

def help(bot, update):
    print('help',update)
    # keyboard = [
    #              [InlineKeyboardButton('Leave', callback_data='cancel')]
    #            ]
    # print(1,update)
    # update.message.reply_text('Welcome123:')
    keyboard = [
        [InlineKeyboardButton('Leave', callback_data='cancel')]
    ]

    # update.callback_query.message('Help ... help..', reply_markup=InlineKeyboardMarkup(keyboard))
    # if update.message:
    # update.callback_query.edit_message_reply_markup('Help ... help..', reply_markup=InlineKeyboardMarkup(keyboard))
if __name__ == '__main__':
    main()
    # dispatcher.add_handler(CallbackQueryHandler(help, pattern='help'))
    # dispatcher.add_handler(CallbackQueryHandler(help, pattern='help'))