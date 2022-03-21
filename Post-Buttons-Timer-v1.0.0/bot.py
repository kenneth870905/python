# -*- coding: utf-8 -*-
# Programmer : t.me/Amir_720
# ---------------------Telethon--------------------
import re
from telethon.sync import TelegramClient, events, Button
from pyfiglet import figlet_format
import pyfiglet.fonts
from telethon.tl.types import MessageEntityUrl, Message
from telethon.errors import *
from EveryTime import EveryTime
from random import choice
from time import time
import os
import json
# ------------------------Values------------------------
from config import *
from texts import buttons_name
import texts

bot = TelegramClient(session_name, api_id, api_hash)

try:
    bot.start(bot_token=token)
except Exception as e:
    print(e)

print(bot_name)

buttons_coordinates = {}
buttons_coordinates_2 = {}
messages = []
data_flood = {}
# -------------------------butoons------------------
main_buttons = [
    [
        Button.text(buttons_name.display, resize=True),
    ],
    [
        Button.text(buttons_name.set_channel, resize=True),
        Button.text(buttons_name.set_time, resize=True),
    ],
    [
        Button.text(buttons_name.add_button, resize=True),
        Button.text(buttons_name.del_button, resize=True),
    ],
    [
        Button.text(buttons_name.start, resize=True),
    ],
]
# -----------------------files--------------------------
# fileds should be created
_files = [
    {
        "path": "buttons.json",
        "object": [],
    },
    {
        "path": "data.json",
        "object": {
            "channel": None,
            "time_loop": 1 * 60 * 60},
    }
]
# create files
for file in _files:
    if not os.path.exists(file["path"]):
        json.dump(file["object"], open(file["path"], 'w'))
# ------------------------functions-------------------------
# get data
def get_data():
    data = json.load(open("data.json", 'r'))
    return data

# save data
def save_data(data):
    json.dump(data, open("data.json", 'w'))

# get channel
def get_channel():
    return get_data()['channel']

# save channel
def save_channel(channel):
    data = get_data()
    data["channel"] = channel
    save_data(data)

# get time loop
def get_time_loop():
    return get_data()['time_loop']

#save time loop
def save_time_loop(time_loop):
    data = get_data()
    data["time_loop"] = time_loop
    save_data(data)


# check validition url
def Validition_Url(url):
    check = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https://
        # domain...
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    # out
    if check.match(url):
        return True
    else:
        return False


def numeric(num):
    if float(num) < 1000:
        return num
    num = str(int(float(num)))
    from re import findall
    price = ",".join(findall("[\d]{1,3}", num[::-1]))[::-1]
    return price


def event_values(event):
    text, sender_id, chat_id, msg_id = ('', None, None, None,)
    if event.raw_text:
        text = event.raw_text
    if event.sender_id:
        sender_id = event.sender_id
    if event.chat_id:
        chat_id = event.chat_id
    if event.message:
        msg_id = event.message.id
    return text, sender_id, chat_id, msg_id


def randstr(n):
    from string import ascii_letters
    from random import choice
    data = ascii_letters + "0123456789"
    stri = ""
    while len(stri) < n:
        stri += choice(data)
    return stri


def just_get_buttons():
    data = json.load(open("buttons.json"))

    return data


def get_list_buttons():
    get_buttons(with_number=True)

    data = just_get_buttons()

    if not data:
        return

    bts = []
    c = 0

    for row in data:
        for button in row:
            c += 1
            bts.append(
                (c, button['text'])
            )

    if not bts:
        return

    return bts


def get_buttons(with_number=False,display=False):
    global buttons_coordinates, buttons_coordinates_2

    if with_number:
        buttons_coordinates = {}

    data = just_get_buttons()

    if not data:
        if not with_number:
            return
        else:
            data.append([])

    buttons = []
    count = 0
    c_rows = 0

    for row in data:
        #
        if not row:
            continue
        row_2 = []
        #
        for button in row:
            # url butoons
            if("url" in button):
                b = Button.url(
                    text=button['text'],
                    url=button['url']
                )
            # inline butoons
            else:
                b = Button.inline(
                    text=button['text'],
                    data="display" if (display or with_number) else button['data'] 
                )
            row_2.append(b)
            count += 1
            # with_number
            n = count
            buttons_coordinates_2[n] = (c_rows, len(row_2)-1,)
        # with_number
        if with_number:
            n = count + 1
            buttons_coordinates[n] = (len(buttons), len(row_2),)

            row_2.append(Button.inline(f"{n}", data=f"button-{n}"))
            count += 1
        buttons.append(row_2)
        c_rows += 1
    # with_number
    if with_number:
        n = count + 1
        buttons_coordinates[n] = (len(buttons), 0,)

        buttons.append(
            [
                Button.inline(f"{n}", data=f"button-{n}")
            ]
        )
    ##
    if not buttons:
        return
    return buttons


def save_buttons(buttons):
    json.dump(buttons, open("buttons.json", "w"))


target_channel = get_channel()
time_loop = get_time_loop()
# ----------------------------timer send------------------------------------


async def TimerSend():
    #global data
    global messages, target_channel

    # check messages not empty
    if not messages:
        return

    # get channel
    if not target_channel:
        await bot.send_message(admin, texts.channel_empty)
        return

    # choice message
    message = choice(messages)

    # send message
    try:
        buttons = get_buttons()
        await bot.send_message(target_channel, message, buttons=buttons)
    except (ChannelInvalidError, ChatInvalidError, PeerIdInvalidError, ChatForbiddenError):
        # notif to admin
        await bot.send_message(admin, texts.channel_error.format(channel=target_channel))
        # remove the channel id
        target_channel = None
        save_channel(target_channel)
        return
    except Exception as e:
        print(e)
        return

    # remove message from old data
    #messages.remove(message)


# start thread
main_thread = EveryTime(time_loop, TimerSend)
main_thread.start()
# --------------------------NewMessage------------------------------------------
@bot.on(events.NewMessage(chats=[admin]))
async def event_handler(event):
    text, sender_id, chat_id, msg_id = event_values(event)

    #global data
    global messages, target_channel, time_loop, main_thread

    # update buttons
    get_buttons(with_number=True)

    # regex matchs
    matchs = {
        'add_url': re.match(r"[/!]?add_url (\d+)", text, re.I),
        'add_inline': re.match(r"[/!]?add_inline (\d+)", text, re.I),
        'del': re.match(r"[/!]?del (\d+)$", text, re.I),
        'set_channel': re.match(r"[/!]?set_channel (?:(?:https?://)?t\.me|@)(.{5,})$", text, re.I),
        'set_time': re.match(r"[/!]?set_time (\d+)$", text, re.I),
    }
# ------------start------------------
    if text in ('/start', buttons_name.start, ):
        await event.reply("Hello Sir !", buttons=main_buttons)

# ----display buttons----
    elif text == buttons_name.display:
        try:
            buttons = get_buttons(display=True)
            if not buttons:
                await event.reply(texts.buttons_empty)
                return

            await event.reply(".", buttons=buttons)
        except Exception as e:
            print(e)

# ----add new button---
    elif text == buttons_name.add_button:
        try:
            buttons = get_buttons(with_number=True)

            t = texts.add_button
            await event.reply(t, buttons=buttons)
        except Exception as e:
            print(e)
# ----delete a button----
    elif text == buttons_name.del_button:
        try:
            buttons = get_list_buttons()

            if not buttons:
                await event.reply(texts.buttons_empty)
                return

            bts = map(lambda x: f"{x[0]} : {x[1]}", buttons)

            bts = "\n".join(bts)

            t = texts.delete_button.format(buttons_list=bts)
            await event.reply(t)
        except Exception as e:
            print(e)

# ----set channel 1----
    elif text == buttons_name.set_channel:
        try:
            t = texts.set_channel.format(channel=target_channel)
            await event.reply(t)
        except Exception as e:
            print(e)


# ----set time 1----
    elif text == buttons_name.set_time:
        try:
            t = texts.set_time.format(time=time_loop // 60)
            await event.reply(t)
        except Exception as e:
            print(e)

# ----clear all messages----
    elif text == buttons_name.clear_messages:
        try:
            messages.clear()
            t = texts.clear_messages
            await event.reply(t)
        except Exception as e:
            print(e)

# ----add new button 2--url button-
    elif matchs["add_url"]:
        try:
            position = int(matchs["add_url"].group(1))
            #
            if not position in buttons_coordinates:
                t = texts.invalid_position.format(position=position)
                await event.reply(t)
                return
            #
            lines = text.split("\n")
            if len(lines) != 3:
                t = texts.invalid_input
                await event.reply(t)
                return

            # check url validition
            button_url = lines[2]

            if not Validition_Url(button_url):
                t = texts.channel_error
                await event.reply(t)
                return

            # add new button
            button = {
                'text': lines[1],
                'url': button_url,
            }

            a = buttons_coordinates[position][0]
            b = buttons_coordinates[position][1]
            ##
            buttons = just_get_buttons()
            if len(buttons)-1 < a:
                buttons.append([])
            #
            buttons[a].insert(b, button)
            save_buttons(buttons)

            t = texts.add_succesfully
            await event.reply(t)
        except Exception as e:
            print(e)

# ----add new button 2--inline button-
    elif matchs["add_inline"]:
        try:
            position = int(matchs["add_inline"].group(1))
            #
            if not position in buttons_coordinates:
                t = texts.invalid_position.format(position=position)
                await event.reply(t)
                return
            #
            lines = text.split("\n")
            if len(lines) != 2:
                t = texts.invalid_input
                await event.reply(t)
                return

            # add new button
            button = {
                'text': lines[1],
                'data': "update",
            }

            a = buttons_coordinates[position][0]
            b = buttons_coordinates[position][1]
            ##
            buttons = just_get_buttons()
            if len(buttons)-1 < a:
                buttons.append([])
            #
            buttons[a].insert(b, button)
            save_buttons(buttons)

            t = texts.add_succesfully
            await event.reply(t)
        except Exception as e:
            print(e)

# ----delete a button 2----
    elif matchs["del"]:
        try:
            position = int(matchs["del"].group(1))
            #
            if not position in buttons_coordinates_2:
                t = texts.invalid_position.format(position=position)
                await event.reply(t)
                return
            
            #get buttons
            buttons = just_get_buttons()

            #delete empty rows
            for row in buttons:
                if not row:
                    buttons.remove(row)
            #
            a = buttons_coordinates_2[position][0]
            b = buttons_coordinates_2[position][1]

            #delete position
            del buttons[a][b]


            #save
            save_buttons(buttons)

            t = texts.del_succesfully
            await event.reply(t)
        except Exception as e:
            print(e)

# ----set the channel 2----
    elif matchs["set_channel"]:
        channel = matchs["set_channel"].group(1)
        # check valid channel
        try:
            await bot.get_entity(channel)
        except:
            await event.reply(texts.channel_error.format(channel=channel))
            return
        # save channel
        target_channel = channel
        save_channel(channel)
        # send message added
        t = texts.channel_added.format(channel=channel)
        await event.reply(t)


# ----set the time loop 2----
    elif matchs["set_time"]:
        match = matchs["set_time"]
        time_loop = int(match.group(1)) #minute
        time_loop = time_loop * 60 # to second
        
        # save time loop
        save_time_loop(time_loop)
        
        #done the main thread
        main_thread.done()
        #start new thread
        main_thread = EveryTime(time_loop, TimerSend)
        main_thread.start()

        # send message added
        t = texts.time_loop_added.format(channel=time_loop // 60)
        await event.reply(t)

# -----send to channel--------------
    else:
        # check exists channel
        if not target_channel:
            await event.reply(texts.channel_empty)
            return
        # add post
        message = event.message
        messages.append(message)
        await event.reply(texts.added_post)
# -----------------------------Callback Query----------------------------------------


@bot.on(events.CallbackQuery)
async def event_handler(event):
    Data = event.data.decode()

    global messages, data_flood
    #----check data callback
    if Data != "update" :
        return
    #----check data callback
    '''
    sender_id = event.sender_id
    if sender_id in data_flood:
        #5 time in minute => every 12 sec
        if time() - data_flood[sender_id] < 12:
            return
    #update last click time
    data_flood[sender_id] = time()
    '''
    # --------------------------------
    try:
        #get chat id
        chat_id = event.chat_id
        
        #check messages empty
        if not messages:
            return

        #get message
        message = choice(messages)

        #get buttons
        buttons = get_buttons()

        #remove old message
        #await event.delete()

        #send new meesage
        await bot.send_message(chat_id, message, buttons=buttons)

        #remove message from messages
        #messages.remove(message)
    except Exception as e:
        print(e)
# ----------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------

if __name__ == "__main__":
    try:
        bot.run_until_disconnected()
    except Exception as e:
        print(e)

    input("Press Any Key To Quit !")

# Programmer : t.me/Amir_720
