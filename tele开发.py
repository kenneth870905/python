# 第一个注释
import time

from telethon import TelegramClient, events, sync
from telethon import utils
from telethon import functions

from telethon.tl.functions.channels import GetParticipantsRequest, InviteToChannelRequest
from telethon.tl.functions.messages import AddChatUserRequest
from telethon.tl.types import ChannelParticipantsSearch
from time import sleep

# These example values won't work. You must get your own api_id and
# api_hash from https://my.telegram.org, under API Development.

api_id = 1254346
api_hash = '6cbc41174ef6cd0c44af16d6117fc49c'

f = open("./tele.txt", 'w+',encoding="utf-8")

client = TelegramClient('session_name', api_id, api_hash)
client.start()
me = client.get_me()
# 打印群信息
dialogs = client.get_dialogs()
# print(client.get_entity("@guanshifuwu"))
# my_channel = client.get_entity('扇贝吐水夫妻互换鉴黄交流群')   1389763687
my_channel = client.get_entity('博彩行业交流共享群')
# 1457535120
print(my_channel,file=f)
exit()
# =============
offset = 0
limit = 100
all_participants = []
# client(InviteToChannelRequest(
#                 channel=1327483562,
#                 users =['Dicky_M']
#             ))
# xiao_xiong  Dicky_M
# exit()
# 1327483562 我的频道
list = [0,100,200,300,400,500,600,700,800,900,1000,1100,1200,1300,1400,1500,1600,1700,1800,1900,2000,2100,2200,2300,2400,2500,2600,2700,2800,2900,3000,
        3100,3200,3300,3400,3500,3600,3700,3800
        ]
username = []
for num in list:
    # print('---------------',file=f)
    participants = client(GetParticipantsRequest( 1457535120, ChannelParticipantsSearch(''), num, 100, hash=0))
    # if not participants.users:
        # break
    all_participants.extend(participants.users)
    print(len(all_participants))
    username = []
    for par in all_participants:
        if par.username:
            username.append(par.username)
        elif par.phone:
            username.append(par.phone)
        # elif par.first_name:
        #     username.append(par.first_name)
print(username, file=f)
print(len(username))
lst2 = sorted(set(username), key=username.index)
print(lst2,file=f)
print(len(lst2))

for name in lst2:
    try:
        client(InviteToChannelRequest(
                channel=1327483562,
                users =[name]
            ))
        print(name)
    except:
        print('------------',name)
    time.sleep(10)

# xiao_xiong
# FengDoorBot
# client(InviteToChannelRequest(
#         channel=1327483562,
#         users =["639275211821"]
#     ))


# for iterating_var in lst2:
    # client(InviteToChannelRequest(
    #     channel=1327483562, #频道id
    #     users = [iterating_var],  #列表格式的username
    # ))



# User(id=738714863, is_self=True, contact=True, mutual_contact=True, deleted=False, bot=False, bot_chat_history=False, bot_nochats=False, verified=False, restricted=False, min=False, bot_inline_geo=False, support=False, scam=False, access_hash=-1560304935798578627, first_name='小孟', last_name='Kenneth', username='phxiaoM', phone='639270325065', photo=UserProfilePhoto(photo_id=3172756178110359471, photo_small=FileLocationToBeDeprecated(volume_id=855225813, local_id=277588), photo_big=FileLocationToBeDeprecated(volume_id=855225813, local_id=277590), dc_id=5), status=UserStatusOffline(was_online=datetime.datetime(2020, 5, 4, 9, 30, 5, tzinfo=datetime.timezone.utc)), bot_info_version=None, restriction_reason=[], bot_inline_placeholder=None, lang_code=None)
# User(id=1019758607, is_self=False, contact=True, mutual_contact=True, deleted=False, bot=False, bot_chat_history=False, bot_nochats=False, verified=False, restricted=False, min=False, bot_inline_geo=False, support=False, scam=False, access_hash=408260543666490158, first_name='锅倩', last_name=None, username=None, phone='639294142403', photo=None, status=UserStatusOffline(was_online=datetime.datetime(2020, 5, 4, 4, 50, 38, tzinfo=datetime.timezone.utc)), bot_info_version=None, restriction_reason=[], bot_inline_placeholder=None, lang_code=None)

# User(id=907156279, is_self=False, contact=False, mutual_contact=False, deleted=False, bot=False, bot_chat_history=False, bot_nochats=False, verified=False, restricted=False, min=False, bot_inline_geo=False, support=False, scam=False, access_hash=-192162674015849252, first_name='小妞别走 44852', last_name=None, username='xiaoniu44852', phone='639957656427', photo=UserProfilePhoto(photo_id=3896206551122290606, photo_small=FileLocationToBeDeprecated(volume_id=500001700814, local_id=130085), photo_big=FileLocationToBeDeprecated(volume_id=500001700814, local_id=130087), dc_id=5), status=UserStatusOnline(expires=datetime.datetime(2020, 5, 4, 9, 54, 40, tzinfo=datetime.timezone.utc)), bot_info_version=None, restriction_reason=[], bot_inline_placeholder=None, lang_code=None)

# client(InviteToChannelRequest(
#     channel=1327483562, #频道id
#     users = ['8613638499663'],#列表格式的username
# ))
# 发送消息
# destination_user_username='8613638499663'
# entity=client.get_entity(destination_user_username)
# client.send_message(entity=entity,message="Hello python")
# ---------------------


# =================
# async def main():
#     # Getting information about yourself
#     me = await client.get_me()
#
#     # "me" is an User object. You can pretty-print
#     # any Telegram object with the "stringify" method:
#     print(me.stringify(),file=f)
#     print(123)
#     print(client)
#     client.send_message('639275211821', 'Hello! Talking to you from Telethon')
#
# with client:
#     client.loop.run_until_complete(main())
