#Programmer : t.me/Amir_720

from requests.api import get
from telethon.sync import TelegramClient,events,Button
from telethon.tl.custom import Button
from telethon.errors import *
from time import sleep
from pyfiglet import figlet_format
from os import path
import requests,json,os

from telethon.tl.types import Channel, PeerChannel, PeerChat
#------------------Config-------------------
from config import *
import texts
bot = TelegramClient(session_name,api_id, api_hash).start(bot_token=token)
bot.start()
print('程序已启动：',name_bot)
# print(figlet_format(name_bot))

#----------------functions-----------------
def get_chat_member(chat_id,user_id):
	try:
		chat_id = str(chat_id)
		chat_id = chat_id if chat_id.startswith('-100') else f'-100{chat_id}'
		data = {
			'chat_id':chat_id,
			'user_id':user_id,
		}
		result = requests.post(f"https://api.telegram.org/bot{token}/GetChatMember",data=data)
		result = result.json()
		if (not result['ok']) or (not 'result' in result):
			return False
		return result['result']['status']
	except Exception as e:
		print(e)
		return False


def event_values(event):
	if event.raw_text != None : text = str(event.raw_text)
	if event.sender_id != None : sender_id = event.sender_id
	if event.chat_id != None : chat_id = event.chat_id
	if event.message != None : msg_id = event.message.id
	#text,sender_id,chat_id,msg_id = event_values(event)
	return text,sender_id,chat_id,msg_id


def sec_to_time(sec):
	hours = sec//3600
	sec -= hours *3600
	
	minutes = sec//60
	sec -= minutes *60
	
	return f"{hours} Hours and {minutes} Minutes and {sec} Seconds"

async def send_to_users(bot,users,message):
	b = 0
	flood = False
	for user in users[:] :
		try:
			m = await bot.send_message(user,message)
		except FloodWaitError as e:
			sec = e.seconds
			flood = sec
			break
		except (MessageEmptyError,MessageTooLongError,TimedOutError) :
			break
		except Exception as e :
			pass
		else:
			b+=1
			sleep(0.034)
			users.remove(user)
	return (b,users,flood)
	

async def forward_to_users(bot,users,message):
	b = 0
	flood = False
	for user in users[:] :
		try:
			m = await bot.forward_messages(entity=user,messages=message)
		except FloodWaitError as e:
			sec = e.seconds
			flood = sec
			break
		except (MessageEmptyError,MessageTooLongError,TimedOutError) :
			break
		except Exception as e :
			pass
		else:
			b+=1
			sleep(0.034)
			users.remove(user)
	return (b,users,flood)

async def entity_to_id(bot,entity,is_channel=False):
	ch = entity
	if str(ch).isdigit() or "-100" in ch :
		ch = int(ch)
	try :
		res = await bot.get_entity(ch)
		if is_channel and type(res) != Channel :
			return
		return res.id
	except :
		return

def get_channels():
	return json.load(open('channels.json'))

def save_channels(channels):
	return json.dump(channels,open('channels.json','w'))

def get_channels_source():
	f2 = lambda x:int(f"-100{x['from']}")
	return list(map(f2,channels))

#----------------DataBase------------------

if not os.path.exists('channels.json'):
	save_channels([])

	
channels = get_channels()
#----------------buttons-------------------
buttons_main = [
	[Button.text('channels', resize= True)],
	[Button.text('/help', resize= True),Button.text('/start', resize= True)],
]

#--------------------------NewMessage admin-------------------------------
@bot.on(events.NewMessage(chats=[admin],func=lambda e:e.is_private))
async def my_event_handler(event):
	text,sender_id,chat_id,msg_id = event_values(event)
	global channels
#---------start-------
	if text.lower() == '/start':
		await event.reply(texts.start,buttons=buttons_main)
#---------help-------
	if text.lower() == '/help':
		t = texts.help
		await event.reply(t,buttons=buttons_main)
#---------get list channels-------
	if text.lower() == 'channels':
		#channels = get_channels()
		if not channels:
			await event.reply(texts.channels_empty)
			return
		t = []
		b = 1
		for x in channels:
			a = f"(`{b}`)\nFrom : `{x['from']}`\nTo : `{x['to']}`\ntext : {x['text']}"
			t.append(a)
			b+=1
		await event.reply("\n---------\n".join(t),buttons=buttons_main)
#--------remove forward channel --------
	match = re.match('[\/\!]?remove (\d{,2})$',text,re.I)
	if match:
		try:
			index = int(match.group(1))

			#channels = get_channels()
			if not channels or len(channels) < index or index <= 0:
				await event.reply(texts.index_does_exists)
				return
			del channels[index-1]
			save_channels(channels)
			await event.reply(f'index {index} succesfully removed !')
		except Exception as e:
			print(e)
#--------add forward channel --------
	match = re.match('[\/\!]?forward (\S+) to (\S+)$',text,re.I)
	if match:
		try:
			ch_1,ch_2 = match.group(1),match.group(2)
			channels2 = []
			me = await bot.get_me()

			for ch in (ch_1,ch_2,):
				ch = await entity_to_id(bot,ch,True)
				if not ch:
					await event.reply(texts.invalid_channel)
					return
				result = get_chat_member(ch,me.id)
				skip = (
					not result,
					result != 'administrator',
				)
				if any(skip):
					await event.reply(texts.not_admin_bot)
					return
				if ch in channels2:
					await event.reply(texts.ch_must_diff)
					return
				channels2.append(ch)
			channel = {
				'from':channels2[0],
				'to':channels2[1],
				'text':text,
			}
			if channel in channels:
				await event.reply(texts.ch_exists)
				return
			channels.append(channel)
			save_channels(channels)
			
			await event.reply(texts.ch_set)
		except Exception as e:
			print(e)
#--------------------------NewMessage channel-------------------------------
async def forward_process_handler(event):
#---------------
	try:
		channel = event.sender_id
		
		channel = str(channel)
		channel = channel[4:] if channel.startswith('-100') else channel
		channel = int(channel)
		
		toos = []
		for item in channels:
			if item['from'] == channel:
				toos.append(item['to'])
		
		if not toos:
			return

		mesage = event.messages if hasattr(event,'messages') else event.message

		a = await forward_to_users(bot,toos,mesage)
		if a[2]:
			print('Flood for :',sec_to_time(a[2]))
		
	except Exception as e:
		print(e)
#--------------------------
if __name__ == "__main__":
	f1 = lambda e:e.sender_id in get_channels_source() and (not e.message.grouped_id)
	f2 = lambda e:e.sender_id in get_channels_source()
	bot.add_event_handler(forward_process_handler,events.NewMessage(func=f1))
	bot.add_event_handler(forward_process_handler,events.Album(func=f2))
	bot.run_until_disconnected()

#Programmer : t.me/Amir_720