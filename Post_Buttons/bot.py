# -*- coding: utf-8 -*-
# Programmer : t.me/Amir_720
# ---------------------Telethon--------------------
import re
from telethon.sync import TelegramClient, events, Button
# from pyfiglet import figlet_format
from pyfiglet import figlet_format
from telethon.tl.types import MessageEntityUrl
import os
import json
# ------------------------Values------------------------
from config import *
from texts import buttons_name
import texts

bot = TelegramClient(session_name, api_id, api_hash)
bot.start(bot_token=token)
print('程序已经启动')
print(bot_name)
# print(figlet_format(bot_name))

buttons_coordinates = {}
buttons_coordinates_2 = {}
# -------------------------butoons------------------
main_buttons = [
    [
        Button.text(buttons_name.display, resize=True),
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
for file_name in ("buttons.json",):
    if not os.path.exists(file_name):
        json.dump([], open(file_name, 'w'))

# ------------------------functions-------------------------
####


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


def get_buttons(with_number=False):
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
            b = Button.url(
                text=button['text'],
                url=button['url']
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

# --------------------------NewMessage------------------------------------------


@bot.on(events.NewMessage(chats=admins, func=lambda e: e.is_private))
async def event_handler(event):
    text, sender_id, chat_id, msg_id = event_values(event)

    get_buttons(with_number=True)

    matchs = {
        'add': re.match("add (\d+)", text, re.I),
        'del': re.match("del (\d+)$", text, re.I),
    }
# ------------start------------------
    if text in ('/start', buttons_name.start, ):
        await event.reply("Hello Sir !", buttons=main_buttons)

# ----display buttons----
    elif text == buttons_name.display:
        try:
            buttons = get_buttons()
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

# ----add new button 2---
    elif matchs["add"]:
        try:
            position = int(matchs["add"].group(1))
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
            #
            entities = event.message.entities
            if not entities:
                t = texts.no_link
                await event.reply(t)
                return
            #
            url_entity = None
            for entity in entities:
                if type(entity) == MessageEntityUrl:
                    url_entity = entity
                    break
            if not url_entity:
                t = texts.no_link
                await event.reply(t)
                return
            ##
            url_entity = (url_entity.offset, url_entity.length)
            button = {
                'text': lines[1],
                'url': text[url_entity[0]: url_entity[0] + url_entity[1]]
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
            #
            a = buttons_coordinates_2[position][0]
            b = buttons_coordinates_2[position][1]

            buttons = just_get_buttons()
            del buttons[a][b]
            save_buttons(buttons)

            t = texts.del_succesfully
            await event.reply(t)
        except Exception as e:
            print(e)

# -----send to channel--------------
    else:
        message = event.message
        buttons = get_buttons()
        await bot.send_message(target_channel, message, buttons=buttons)
# ---------------------------------------------------------------------------------
# --------------------------------CallbackQuery--------------------------------------------------


@bot.on(events.CallbackQuery)
async def event_handler(event):
    data = event.data.decode()
    sender_id = event.sender_id
    #msg_id = event.original_update.msg_id
    #peer_chat = event.original_update.peer
# --------
    pass
# ----------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------

if __name__ == "__main__":
    bot.run_until_disconnected()

# Programmer : t.me/Amir_720
