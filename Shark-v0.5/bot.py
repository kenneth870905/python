from turtle import st
from telethon.sync import TelegramClient, events, types, Button
from telethon.sync import errors as t_errors
from pyfiglet import figlet_format
from random import randint
import re
import time
# games
from blackjack import BlackjackGame
from forestball import Animals, ForestBallGame
from lucky_airsihp import LuckyAirsihpGame, Place
from niuniu import NiuNiuGame, Selects
from roulette import Dice, MultiDice, RouletteGame
from speedha import SpeedHaGame
from kuisan import KuisanDice, KuisanGame
#
from config import *
from models import *
import texts
# ---varibales
bot = TelegramClient(session=bot_name, api_id=api_id, api_hash=api_hash)
bot.start(bot_token=token)
database = Database(db_file)
games : list[Game] = []
groups : list[Group] = []
top_ten = tuple()
last_update = time.time() - topten_time
envelopes : list[Envelope] = []
envelope_time = time.time()
# settings file
setting = Settings('settings.json')

signed_games = {
    "blackjack" : BlackjackGame,
    "niuniu" : NiuNiuGame,
    "forest":ForestBallGame,
    "roulette":RouletteGame,
    "speedha":SpeedHaGame,
    "kuisan":KuisanGame,
    "lucky":LuckyAirsihpGame,
}

# ---Queries
niuniu_queries = {
    "qinglong": Selects.QingLong,
    "white-tiger": Selects.WhiteTiger,
    "suzaku": Selects.Suzaku,
    "xuanwu": Selects.Xuanwu,
    }

forest_queries = {
    "panda": Animals.Panda,
    "lion": Animals.Lion,
    "tiger": Animals.Tiger,
    "cheetah": Animals.Cheetah,
    "brown-bear": Animals.BrownBear,
    "gray-wolf": Animals.GrayWolf,
    "giraffe": Animals.Giraffe,
    "wild-dog": Animals.WildDog,
    }

roulette_queries = {
    "large": MultiDice((4, 5, 6), "Large"),
    "small": MultiDice((1, 2, 3), "Small"),
    "single": MultiDice((1, 3, 5), "Single"),
    "double": MultiDice((2, 4, 6), "Double"),
    }

kuisan_queries = {
    "large": KuisanDice.Large(),
    "small": KuisanDice.Small(),
    "single": KuisanDice.Single(),
    "double": KuisanDice.Double(),
    "large_single": KuisanDice.LargeSingle(),
    "small_single": KuisanDice.SmallSingle(),
    "large_double": KuisanDice.LargeDouble(),
    "small_double": KuisanDice.SmallDouble(),
    "leopard": KuisanDice.Leopard(),
    "shunzi": KuisanDice.Shunzi(),
    "pair": KuisanDice.Pair(),
}
#-- functions

def refresh_rank():
    global top_ten, last_update
    # check 10 minutes
    if (time.time() - last_update < topten_time):
        return
    # refresh top ten
    # refresh users ranks
    last_update = time.time()
    top_ten = tuple(database.ranking())
    top_ten = tuple(
        map(lambda u: User(u[1], u[2], u[3], rank=u[0]), top_ten))
    


async def check_user(user_id: int, event) -> User:
    # get user name
    name = (await event.get_sender())
    full_name = name.first_name
    if name.last_name:
        full_name += f" {name.last_name}"
    # add to database
    user = database.get_user(user_id)
    if user:
        # check wins week
        if time.time() - user.week_time >= 7 * 24 * 60 * 60:
            user.week_time = time.time()
            user = database.add_win(user, zero=True)
        # update user name
        if user.name != full_name:
            user.name = full_name
            database.update_name(user)
    else:
        # add new user
        user = User(user_id, full_name, 0, 0,
                    sign_time=time.time() - sign_time)
        database.add_user(user)
    #
    return user


def get_group(group_id : int) -> Group:
    global groups
    #change groupd id format
    if str(group_id).startswith('-100'):
        group_id = int(str(group_id)[3:])
    # make group object
    if group_id in groups:
        group = groups[groups.index(group_id)]
    else:
        group = Group(group_id, time.time() - new_game_time)
        groups.append(group)
        
    return group

def check_group_game(group_id : int):
    group = get_group(group_id)
    # check time duriing
    if time.time() - group.last_game < new_game_time :
        return False
    else:
        return True

def reset_game_time(group_id : int, time_set : float = time.time() - new_game_time):
    global groups
    # reset time last game
    group = get_group(group_id)
    group.last_game = time_set
    return group

def add_game_history(group_id : int, history):
    global groups
    group = get_group(group_id)
    group.history.append(history)
    # only save 10 game history for each game
    for hist in group.history:
        while group.history.count(hist) > 10:
            del group.history[group.history.index(hist)]


async def check_envelopes():
    global envelopes
    for envelope in envelopes:
        # every 12 hours
        if time.time() - envelope.created >= 12 * 60 * 60 :
            # give back left over money to creator
            left_over = sum(envelope.distro)
            database.add_balance(envelope.user, left_over)
            envelopes.remove(envelope)
            try:
                await bot.send_message(envelope.user.id, texts.red_envelope_give_back.format(amount=separator(left_over)))
            except :
                pass
            
            
# ---Messages


async def messages_handler(event: events.newmessage.NewMessage.Event):
    sender_id = event.sender_id
    text = str(event.raw_text)
    chat_id = event.chat_id
    global envelopes
    # check chat type
    if type(event.message.peer_id) == types.PeerUser:
        return
    # check user
    user = await check_user(sender_id, event)
    refresh_rank()
    await check_envelopes()
    
    # game tables
    game_pattern = re.match(r"[/!](?P<game>21|pj|sl|lp|suoha|ks|feiting)", text, re.I)
    if game_pattern:
        # check flood
        if not check_group_game(chat_id):
            return await event.reply(texts.make_game_flood_warning.format(limit=new_game_time))
        # new game created time
        reset_game_time(chat_id, time.time())
        # detect game type
        command = game_pattern.group("game")
        if command == '21':
            # blackjack 21
            texts_source = signed_games["blackjack"].texts_source
        elif command == 'pj':
            # niuniu
            texts_source = signed_games["niuniu"].texts_source
        elif command == 'sl':
            # forest
            texts_source = signed_games["forest"].texts_source
        elif command == 'lp':
            # roulette
            texts_source = signed_games["roulette"].texts_source
        elif command == 'suoha':
            # speed haha
            texts_source = signed_games["speedha"].texts_source
        elif command == 'ks':
            # speed haha
            texts_source = signed_games["kuisan"].texts_source
        elif command == 'feiting':
            # lucky airship
            texts_source = signed_games["lucky"].texts_source
        # send game table
        await event.reply(texts.start_game.format(game_name=texts_source.name), buttons=texts_source.buttons_game, link_preview=False)
            
    
    # /rank top fortuners list
    elif text.startswith('/rank'):
        # fomratting top list
        user = await check_user(sender_id, event)
        _top_ten = list(
            map(lambda u: f"{u.rank}. {u.name} : ${separator(u.balance)}", top_ten))
        _t = '\n'.join(list(_top_ten))
        await event.reply(texts.top_ten_rank.format(top_ten=_t, rank=user.rank))
        
    # transfer balance betwenn users
    elif text.startswith('/zz'):
        # check command's format
        user = await check_user(sender_id, event)
        pattern = re.match(r'\/zz (?P<amount>\d+)', text,re.I)
        # get replied message
        reply_user = await event.get_reply_message()
        if (not pattern) or (not reply_user):
            await event.reply(texts.transfer_wrong_format)
            return
        # check user replied
        reply_user = reply_user.from_id
        if (type(reply_user) != types.PeerUser):
            await event.reply(texts.transfer_to_not_sign)
            return
        reply_user = database.get_user(reply_user.user_id)
        if (not reply_user):
            await event.reply(texts.transfer_to_not_sign)
            return
        # check user balance
        transfer_amount = int(pattern.group('amount'))
        if user.balance < transfer_amount:
            await event.reply(texts.transfer_not_enough.format(amount=separator(transfer_amount)))
            return
        # calculate amounts
        fee = int(transfer_amount * 0.10)
        credit = transfer_amount - fee
        # transfer crdeit and receive fee
        try:
            database.add_balance(reply_user, credit)
            user = database.add_balance(user, - fee)
        except OverflowError:
            await event.reply(texts.overflow_error)
            return
        # successful
        await event.reply(texts.transfer_status.format(credit=separator(credit), fee=separator(fee)))
    
    # /hb red envelope
    elif text.startswith('/hb'):
        # check command's format
        pattern = re.match(r'\/hb (?P<amount>\d+) (?P<count>\d+)$', text,re.I)
        if not pattern:
            return
        # make an envelope 
        user = await check_user(sender_id, event)
        amount = int(pattern.group('amount'))
        count = int(pattern.group('count'))
        # check minimum amount
        if amount < 10000000:
            return await event.reply(texts.red_envelope_minimum_amount)
        # check count
        if not (3 <= count <= 100):
            return await event.reply(texts.red_envelope_minimum_count)
        # check user balance
        if user.balance < amount:
            return await event.reply(texts.red_envelope_not_enough_balance)
        # make a uniqe id
        try:
            _id = max(envelopes, key=lambda e:e.id) + 1
        except ValueError:
            # list is empty
            _id = 1
        print(_id)
        # add new envelope
        envelope = Envelope(_id, user, amount, count)
        envelopes.append(envelope)
        # decrease amount from creator user
        database.add_balance(user, - amount)
        # send an red envelope
        buttons = [
            [Button.inline(texts.red_envelope_button, f'envelope:{envelope.id}')]
        ]
        await event.reply(texts.red_envelope_stats.format(user=user.name, amount=amount, count=count), buttons=buttons, link_preview=False)


async def admin_message_handler(event):
    sender_id = event.sender_id
    text = str(event.raw_text)
    chat = event.message.peer_id
    # check user
    user = await check_user(sender_id, event)
    # only works in private
    if type(chat) != types.PeerUser:
        return

    # start menu
    if text.lower() == "/start" :
        await event.reply(texts.start_menu)#, buttons=texts.buttons_ad_panel)
        
    # /zengjia add money to users by admin
    elif text.startswith('/zengjia'):
        # check command's format
        pattern = re.match(r'\/zengjia (?P<target>(?:all|\d+)) (?P<amount>\d+)$', text,re.I)
        # get replied message
        if (not pattern):
            return await event.reply(texts.add_money_wrong_format)
        # calculate amounts (increase)
        amount = int(pattern.group('amount'))
        # check target user
        target = pattern.group('target')
        if target == "all":
            # add money to all users
            database.add_balance_all(amount)
        else:
            target_user = database.get_user(int(target))
            if (not target_user):
                return await event.reply(texts.transfer_to_not_sign)
            # add money to user
            database.add_balance(target_user, amount)
            
        # result
        await event.reply(texts.add_money_status.format(amount=separator(amount), user=target) )
        
    
    # /sf command to decrease money of all users  
    elif text.startswith("/sf"):
        # check command's format
        pattern = re.match(r'\/sf (?P<target>(?:all|\d+)) (?P<amount>\d+)$', text,re.I)
        # get replied message
        if (not pattern):
            return await event.reply(texts.del_money_wrong_format)
        # calculate amounts (decrease)
        amount = - int(pattern.group('amount'))
        # check target user
        target = pattern.group('target')
        if target == "all":
            # delete money from all users
            database.add_balance_all(amount)
        else:
            target_user = database.get_user(int(target))
            if (not target_user):
                await event.reply(texts.transfer_to_not_sign)
                return
            # delete money
            database.add_balance(target_user, amount)
        
        # result
        await event.reply(texts.delete_money_status.format(amount=separator(amount), user=target) )

    # /settings change setting
    elif text.startswith('/settings'):
        # check command's format
        pattern = re.match(r'\/settings (?P<key>.+) (?P<value>.+)$', text,re.I)
        # send command's description and list of currnt settings
        _settings_list = map(lambda key:f"`{key}` : {vars(setting.data)[key]}", vars(setting.data))
        _settings_list = "\n".join(_settings_list)
        if (not pattern):
            return await event.reply(texts.settings_description.format(settings=_settings_list), link_preview=False)
        # get key and value
        key = pattern.group('key')
        value = pattern.group('value')
        # check exists key in settings items
        if not key in vars(setting.data):
            return await event.reply(texts.settings_invalid_key.format(key=key))
        # change value
        old_value = setting.data.__dict__[key]
        setting.data.__dict__[key] = value
        setting.update()
        # result
        await event.reply(texts.settings_changed.format(key=key, old=old_value, value=value), link_preview=False)
    

    elif text.startswith("/scz"):
        # print('/scz')
        pattern = re.match(r'\/scz (?P<target>(?:all|\d+)) (?P<amount>\d+)$', text,re.I)

        if (not pattern):
            return await event.reply(texts.del_money_wrong_format)

        zu = int(pattern.group('amount'))
        # check target user
        target = pattern.group('target')
        
        if target == "all":
            # delete money from all users
            database.dete_balance_all(zu)
        else:
            return await event.reply("输入命令错误，请重新输入")
        
        # /scz 738714863 2  1080622

async def users_private_handler(event):
    sender_id = event.sender_id
    text = str(event.raw_text)
    chat = event.message.peer_id
    # only works in private
    if type(chat) != types.PeerUser:
        return await event.reply(texts.private_commands_warnings)
    # check user
    user = await check_user(sender_id, event)
    
    # /ck deposit money
    if text.startswith("/ck"):
        deposit_amount = database.get_deposit(sender_id)
        pattern = re.match(r'/ck (?P<amount>\d+)$', text, re.I)
        # check command's format
        if not pattern:
            return await event.reply(texts.deposit_status.format(amount=separator(deposit_amount)))
        # check deposit amount
        new_deposit = int(pattern.group("amount"))
        if new_deposit < 1000000:
            return await event.reply(texts.deposit_limit_warning)
        # check user balance
        if user.balance < new_deposit:
            return await event.reply(texts.deposit_not_enough.format(balance=separator(user.balance)))
        # make an deposit
        deposit_amount = database.make_deposit(user, new_deposit)
        await event.reply(texts.deposit_success.format(amount=separator(deposit_amount)))
    
    # /qk qithdraw the money
    elif text.startswith("/qk"):
        deposit_amount = database.get_deposit(sender_id)
        pattern = re.match(r'/qk (?P<amount>\d+)$', text, re.I)
        # check command's format
        if not pattern:
            return await event.reply(texts.withdraw_status.format(amount=separator(deposit_amount)))
        # check withdraw amount
        withdraw_amount = int(pattern.group("amount"))
        if withdraw_amount < 1000000:
            return await event.reply(texts.withdraw_warning.format(amount=separator(withdraw_amount)))
        # check deposit amount and withdraw
        if deposit_amount < withdraw_amount:
            return await event.reply(texts.withdraw_not_enough.format(deposit=separator(deposit_amount)))
        # make withdraw with nevigate amount
        deposit_amount = database.make_deposit(user, - withdraw_amount)
        await event.reply(texts.withdraw_success.format(withdraw=separator(withdraw_amount), deposit=separator(deposit_amount)))
    
    # /settitle to make custom titles
    elif text.startswith('/settitle'):
        # check command's format
        pattern = re.match(r"/settitle (?P<title>\w+)$", text, re.I)
        if not pattern:
            return await event.reply(texts.set_title_description)
        # check title name
        title = pattern.group('title')
        if len(title) > 4:
            return await event.reply(texts.set_title_wrong_length.format(length=len(title)))
        # check user money
        if user.balance < 500:
            return await event.reply(texts.set_title_money_not_enough)
        # change title
        database.add_balance(user, - 500)
        database.change_title(user, title)
        await event.reply(texts.set_title_succes.format(title=title))

            
    

# --CallbackQuery-------------------------------------------------------------

async def callback_handler(event: events.callbackquery.CallbackQuery.Event):
    query : str = event.data.decode()
    sender_id = event.sender_id
    game_id = event.original_update.msg_id
    chat_id = event.chat_id
    global envelopes
    # check chat type
    if type(event.original_update.peer) == types.PeerUser:
        return
    group = get_group(chat_id)
    # check user exists
    user = await check_user(sender_id, event)
    # check queries
    if query == 'balance':
        # display user info (balance, name, fortune list)
        user.fortune = top_ten.index(
            user.id)+1 if user.id in top_ten else texts.not_in_list

        ans_meessage = texts.display_balance.format(
            name=user.name, balance=separator(user.balance), week_wins=user.week_wins, fortune=user.fortune
        )
        await event.answer(ans_meessage, alert=True)
    elif query == 'sign-in':
        # check SIGN_TIME
        if time.time() - user.sign_time < sign_time:
            return await event.answer(texts.sign_in_warning.format(sign_time=sign_time), alert=True)
        # check user balance
        if user.balance >= sign_limit_balance :
            return await event.answer(texts.sign_in_high_balance_warning.format(sign_limit_balance=separator(sign_limit_balance)), alert=True)
        
        # update balance
        reward = randint(reward_range[0], reward_range[1])
        user.sign_time = time.time()
        # commit
        user = database.add_balance(user, reward)
        await event.answer(texts.sign_in_reward.format(reward=separator(reward)), alert=True)

            
    elif re.search("\d+:.*", query, re.I):
        # split query data
        query = query.split(':')
        rate = float(query[0])
        game_type = query[1]
        # join the game
        if game_id in games:
            indx = games.index(game_id)
            game = games[indx]
        else:
            # make new game
            if game_type in signed_games:
                game = signed_games[game_type](game_id, database, setting)
            else :
                raise Exception("can't detect game type !")
            games.append(game)
            indx = games.index(game_id)
        # make a bet
        try:
            add_bet = game.add_bet(user, rate)
        except errors.AddBetLimit :
            await event.answer(texts.raises_5time_warning, alert=True)
            return
        except errors.BalanceNotEnough:
            await event.answer(texts.not_enough_balance, alert=True)
            return
        # get game controls buttons
        buttons = signed_games[game_type].texts_source.buttons_game
        
        _player_list = list(
            map(lambda p: texts.user_bet_stat.format(
                title=make_hyper_title(p, setting), name=p.user.name, amount=separator(p.bet_amount)), game.players))
        _player_list = "\n".join(_player_list)
        
        await event.answer(texts.adding_bet.format(amount=separator(add_bet)), alert=True)
        try:
            await event.edit(texts.bet_stats.format(game_name=game.name, player_list=_player_list), link_preview=False, buttons=buttons)
        except t_errors.rpcerrorlist.MessageNotModifiedError :
            pass
        
    # starting the games
    elif query == 'start':
        # check game exists
        if not game_id in games:
            await event.answer(texts.not_game_warning, alert=True)
            return
        # starting the game
        indx = games.index(game_id)
        game = games[indx]
        # check user particpante
        if not user.id in game.players:
            return
        # check timer
        if (time.time() - game.last_update) < 6:
            await event.answer(texts.start_6s_warning, alert=True)
            return
        # chnage game table
        game.play()
        try:
            await game.update_stats(event, group.history)
        except t_errors.rpcerrorlist.MessageNotModifiedError :
            pass
    
    # grab envevlope
    elif query.startswith("envelope"):
        # get envelope
        envelope_id = int(query.split(':')[1])
        # check exists envelope
        if not envelope_id in envelopes:
            await event.answer(texts.red_envelope_not_exists, alert=True)
            return await event.delete()
        
        envelope = envelopes[envelopes.index(envelope_id)]
        # check graber duplicated
        if user.id in envelope.grabers:
            return await event.answer(texts.red_envelope_duplicate_warning, alert=True)
        # give reward
        reward = envelope.distro.pop(0)
        database.add_balance(user, reward)
        # add graber
        graber = Graber(user, reward)
        envelope.grabers.append(graber)
        # result
        await event.answer(texts.red_envelope_grabed.format(amount=separator(reward)), alert=True)
        # check completed envelope
        if not envelope.distro:
            envelopes.remove(envelope)
            # display collection details
            grabers_list = map(lambda g:texts.red_envelope_graber_stats.format(name=g.user.name, reward=separator(g.reward)), envelope.grabers)
            grabers_list = "\n".join(grabers_list)
            lucky = max(envelope.grabers, key=lambda g:g.reward)
            lucky = texts.red_envelope_graber_stats.format(name=lucky.user.name, reward=lucky.reward)
            _t = texts.red_envelope_end_stats.format(user=envelope.user.name, amount=envelope.amount, count=envelope.count, grabers_list = grabers_list, lucky=lucky)
            await event.edit(_t, link_preview=False)
        
        


async def game_controls_handler(event: events.callbackquery.CallbackQuery.Event):
    query = event.data.decode()
    sender_id = event.sender_id
    game_id = event.original_update.msg_id
    chat_id = event.chat_id
    # check chat type
    if type(event.original_update.peer) == types.PeerUser:
        return
    group = get_group(chat_id)
    # check user exists
    user = await check_user(sender_id, event)
    # load game
    if not game_id in games:
        return
    indx = games.index(game_id)
    game = games[indx]
    # check user in game
    if not user.id in game.players:
        return
    # Blackjack /21 controls
    if query == 'hit':
        # hit user
        player = game.hit_me(user.id)
        if player == False:
            # suspend to ask card
            await event.answer(texts.Blackjack_21.suspend_askcard_warning, alert=True)
            return
        else:
            # update stats
            #game.players[game.players.index(player.id)] = player
            try:
                await game.update_stats(event, group.history)
            except t_errors.rpcerrorlist.MessageNotModifiedError :
                pass
    elif query == 'stand':
        # change status to stand
        player = game.get_player(user.id)
        if type(player.status) != Status.Playing:
            await event.answer(texts.Blackjack_21.stnad_warning, alert=True)
            return
        player.status = Status.Stand()
        try:
            await game.update_stats(event, group.history)
        except t_errors.rpcerrorlist.MessageNotModifiedError :
            pass
    elif query == 'settle':
        # check game status
        try:
            settle = game.settle()
        except errors.PlayersArePlaying:
            return await event.answer(texts.game_not_completed_warning, alert=True)
        except errors.WaitTimeSelect:
            return await event.answer(texts.wait_time_after_select, alert=True)
        except errors.GameIsClosed:
            return
            
        # settle the game
        reset_game_time(chat_id)
        # add game history
        add_game_history(chat_id, game.history)
        try:
            await game.update_stats(event, group.history, True)
        except t_errors.rpcerrorlist.MessageNotModifiedError :
            pass
        return
        
    
    # Niu Niu game Controls
    if query in niuniu_queries:
        # make a select for user
        select = niuniu_queries[query]
        try:
            stats = game.make_select(user.id, select)
        # selects limit
        except errors.SelectLimit:
            return await event.answer(game.texts_source.flood_select_times, alert=True)
        
        # update game table
        await game.update_stats(event, group.history)
        return
         
    # Forest game Controls
    if query in forest_queries:
        # make a select for user
        select = forest_queries[query]
        
        try:
            player = game.make_select(user.id, select)
        # selects limit
        except errors.SelectLimit:
            return await event.answer(game.texts_source.flood_select_times, alert=True)
        # selects duplicate
        except errors.SelectDuplicate:
            return await event.answer(game.texts_source.select_duplicate_warning, alert=True)
        
        # send user selects status
        selects_list = "\n".join(map(str, player.selects))
        await event.answer(game.texts_source.select_stats_answer.format(selects_list=selects_list), alert=True)
        
    
    # Roulette game Controls
    if (query.startswith("roul:")) or (query in roulette_queries):
        # make a select for user
        if query in roulette_queries:
            select = roulette_queries[query]
        else:
            value = int(query.split(':')[1])
            select = Dice(value)
        
        try:
            player = game.make_select(user.id, select)
        # selects limit
        except errors.SelectLimit:
            return await event.answer(game.texts_source.flood_select_times, alert=True)
        await game.update_stats(event, group.history)
        return
        

    # speed haha game Controls
    if (query.startswith("speedha:")):
        # make a select for user
        item = query.split(':')[1]
        # using the roulette queries
        select = roulette_queries[item]
        try:
            player = game.make_select(user.id, select)
        # selects limit
        except errors.SelectLimit:
            return await event.answer(game.texts_source.flood_select_times, alert=True)
        await game.update_stats(event, group.history)
        return
    
    
    
    # Kuisan game Controls
    if (query.startswith("kuisan:")):
        # make a select for user
        item = query.split(':')[1]
        if item in kuisan_queries:
            # multi item
            select = kuisan_queries[item]
        else:
            # numerice item
            select = Dice(int(item))
        try:
            player = game.make_select(user.id, select)
        # selects limit
        except errors.SelectLimit:
            return await event.answer(game.texts_source.flood_select_times, alert=True)
        await game.update_stats(event, group.history)
        return
    
    
    # Lucky airhisp game Controls
    if (query.startswith("lucky:")):
        # check the type of select
        query_items = query.split(':')
        if query_items[1] == 'place' :
            # select a place
            select = Place(int(query_items[2]))
        else:
            # select an number
            select = Dice(int(query_items[1]))
        # make select
        try:
            player = game.make_select(user.id, select)
        # selects limit
        except errors.SelectLimit:
            return await event.answer(game.texts_source.flood_select_times, alert=True)
        except errors.PlaceLimit:
            return await event.answer(game.texts_source.flood_place_times, alert=True)
        except errors.SelectDuplicate:
            return await event.answer(game.texts_source.select_duplicate_warning, alert=True)
        except errors.PlaceRequired:
            return await event.answer(game.texts_source.place_required_warning, alert=True)
        
        # update
        await game.update_stats(event, group.history)
        return
        


# ---footer
if __name__ == "__main__":
    # add event handlers to bot
    bot.add_event_handler(messages_handler, events.NewMessage())
    bot.add_event_handler(admin_message_handler, events.NewMessage(from_users=admins + [admin]))
    bot.add_event_handler(users_private_handler, events.NewMessage(pattern=r'^[/!](ck|qk|settitle)'))
    
    bot.add_event_handler(callback_handler, events.CallbackQuery())
    bot.add_event_handler(game_controls_handler, events.CallbackQuery())
    # run
    print(figlet_format(bot_name))
    bot.run_until_disconnected()
