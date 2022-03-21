from config import ad
from telethon.sync import Button

# public messages

buttons_end_game = [
    [('Balance', 'balance'), ('Sign In', 'sign-in')],
]


buttons_ad_panel = [
    [('Add New Ad', 'add_ad'), ('Remove Ad', 'remove_ad')],
    [('Set Static Ad', 'set_static'), ('Refresh list', 'refresh')],
]

display_balance = """
{name}
Current balance: {balance}
Cumulative wins this week: {week_wins}
Fortune List: {fortune}
"""

sign_in_reward = "you get {reward} coins as reward"

sign_in_warning = "he rewatd in one in {sign_time} seconds!"

top_ten_rank = """**
{top_ten}

*The list is ranked by the wealth of all players
*The list is refreshed every ten minutes
*Your current ranking: {rank}
**
"""

not_in_list = "not in list"

not_enough_balance = "your coins isn't enough !"

user_bet_stat = "   {name} : {amount}"

adding_bet = """
Successful bet
Your current total bet: {amount}
Please click to start the game after 6 seconds after no one calls!
"""

not_game_warning = "There are currently no users betting, please wait for the user to bet and start the game"

start_6s_warning = "Plese start the game asfter 6s"

settle_game_warning = "There are currently no users betting, please wait for the user to bet and start the game"

make_game_flood_warning = """
Limited start
Each session window can create a game every {limit} seconds
A new game can be unlocked immediately after the previous game is settled
"""

transfer_wrong_format = """
wrong format
Please reply to the message that you need to transfer the object, and then enter the transfer instruction:
/zz transfer-amount
10% handling fee will be deducted for each transfer
"""

transfer_to_not_sign = "Can't transfer to not signed in users"

transfer_not_enough = "Insufficient balance, transfer amount: {amount}"

transfer_status = "Successful transfer, actul credit : {credit}, handling fee : {fee}"


add_money_wrong_format = """
Please enter the deposit like instruction:
/zengjia user_id amount
"""

add_to_not_sign = "Can't deposit money to not signed in users"

overflow_error = "Overflow error, the number is very large !"

raises_5time_warning = "If the number of raises exceeds 5 times per game, this raise fails !"


start_game =  """
{game_name} is betting

%s
""" % ad


bet_stats = """
**
{game_name} is betting

Player list:
{player_list}
**
%s
""" % ad


winner_prize_stats = "   {name} : win +${reward}"

winner_prize = """
**
🎉🎉🎉

{winners_list}
**
"""

sign_in_high_balance_warning = "You cannot sign in with a balance of more than {sign_limit_balance} . Reminder. Sufficient funds, this sign-in failed"

start_menu = "Hi !"


game_not_completed_warning = "the players are playing yet !"

wait_time_after_select = "please wait 6 seconds after the last select !"

del_money_wrong_format = """
Please enter the deposit like instruction:
/sl user_id amount
(for all users, replace user_id with `all`)
"""
add_money_status = "Successful added money, added amount : `{amount}`, target user : `{user}`"

delete_money_status = "Successful deleted money, deleted amount : `{amount}`, target user : `{user}`"

deposit_status = """
Your current deposit is: ${amount}
Deposit instruction: /ck amount
Deposit Amount >= $100,0000
"""

deposit_limit_warning = "A single deposit amount must be >= $100,0000"

deposit_success = """
Successful deposit, current deposit: {amount}
"""

deposit_not_enough = """
The deposit amount cannot be greater than the current balance, the current balance: ${balance}
"""

withdraw_status = """
Your current deposit is: {amount}
Withdrawal instruction: /qk amount
Amount >= $100,0000
"""

withdraw_warning = "Each withdrawal cannot be less than $100,0000. The withdrawal amount is: ${amount}"

withdraw_success = """
Withdrawal succeeded
This withdrawal: ${withdraw}
Current Deposit: ${deposit}
"""

withdraw_not_enough = "The withdrawal amount cannot be greater than the current deposit amount, current deposit: ${deposit}"

private_commands_warnings = "this commands only works in private"

red_envelope_minimum_amount = "The red envelope amount cannot be less than $1000,0000"

red_envelope_minimum_count = "The number of red envelopes cannot be less than 3 and cannot exceed 100"

red_envelope_stats = """
English: {user}
Sent a #red envelope
Amount: {amount}
Number of red envelopes: {count}

%s
""" % ad


red_envelope_graber_stats = "   {name} : {reward}"

red_envelope_end_stats = """
English: {user}
Sent a #red envelope
Amount: {amount}
Number of red envelopes: {count}

Collection details :
{grabers_list}

🎉The luck king of this game is:
{lucky}
%s
""" % ad

red_envelope_button = "🧧 Grab red envelope"

red_envelope_grabed = "English: Congratulations, you got {amount} gold coins"

red_envelope_duplicate_warning = "You have already grabbed this red envelope and cannot receive it here"

red_envelope_not_exists = "the envelope doesn't exists any more"

red_envelope_give_back = "${amount} for unfinished envelope returned to your balance"

# /21 clackjack game
class Blackjack_21 :
    name = "21 BlackJack"
    
    buttons_game = [
        [('1%', '1:blackjack'), ('3%', '3:blackjack'), ('5%', '5:blackjack')],
        [('10%', '10:blackjack'), ('20%', '20:blackjack'), ('30%', '30:blackjack')],
        [('50%', '50:blackjack'), ('70%', '70:blackjack'), ('100%', '100:blackjack')],
        [('Start', 'start'), ('Balance', 'balance'), ('Sign In', 'sign-in')],
    ]

    buttons_control_game = [
        [('Hit me', 'hit'), ('Stand', 'stand')],
        [('Settle the game', 'settle')],
    ]

    start_game =  """
Betting the BlackJack :

%s
""" % ad
    
    bet_stats = """
**
21 Betting

Player list:
{player_list}
**
%s
""" % ad
    
    game_started_stats = """
**
21 Blackjack Selection (30)

dealer: {dealer}

Player list:
{player_list}
**
%s
""" % ad
    
    user_game_stats = "   {name} : {cards} , Total points : {score} ({status})"


    suspend_askcard_warning = "You have suspended trading and cannot continue to ask for cards" 


    stnad_warning = "you are not playing !" 

    user_settle_stats = "   {name} : {cards} , Total points : {score} ({status}) {amount}"

    dealer_settle_stats = "   {cards} , Total points : {score} ({status})"



class NiuNiu:
    name = "娱乐牛牛"
    
    buttons_game = [
        [('1%', '1:niuniu'), ('3%', '3:niuniu'), ('5%', '5:niuniu')],
        [('10%', '10:niuniu'), ('20%', '20:niuniu'), ('30%', '30:niuniu')],
        [('50%', '50:niuniu'), ('70%', '70:niuniu'), ('100%', '100:niuniu')],
        [('Start', 'start'), ('Balance', 'balance'), ('Sign In', 'sign-in')],
    ]

    buttons_control_game = [
        [('Qinglong', 'qinglong'), ('White Tiger', 'white-tiger'), ('Suzaku', 'suzaku'), ('Xuanwu', 'xuanwu')],
        [('Settle the game', 'settle')],
    ]
    
    game_started_stats = """
**
Entertainment Niu Niu is Selection (30)

Player list:
{player_list}

History of the last {len_his} games:
{history}
**
%s
""" % ad


    game_settle_stats = """
**
Entertainment Niu Niu Settlement

Banker ({0})
Qinglong ({1}), White Tiger ({2})
Suzaku ({3}) Xuanwu ({4})

Player list:
{player_list}

History of the last {len_his} games:
{history}
**
%s
""" % ad
    
    user_game_stats = "   {name} : {status} {choice}"
    
    user_settle_stats = "   {name} : {choice} {status} {amount}"
    
    flood_select_times = "in each game you can chnage your select only 3 times"


class ForestBall:
    name = "Forest Ball Game"
    
    emojis = {
        "panda": "🐼",
        "lion": "🦁",
        "tiger": "🐯",
        "cheetah": "🐆",
        "brown-bear": "🐻",
        "gray-wolf": "🐺",
        "giraffe": "🦒",
        "wild-dog": "🐶",
        }
    
    buttons_game = [
        [('1%', '1:forest'), ('3%', '3:forest'), ('5%', '5:forest')],
        [('10%', '10:forest'), ('20%', '20:forest'), ('30%', '30:forest')],
        [('50%', '50:forest'), ('70%', '70:forest'), ('100%', '100:forest')],
        [('Start', 'start'), ('Balance', 'balance'), ('Sign In', 'sign-in')],
    ]

    buttons_control_game = [
        [(emojis['panda'], 'panda'), (emojis['lion'], 'lion'), (emojis['tiger'], 'tiger'), (emojis['cheetah'], 'cheetah')],
        [(emojis['brown-bear'], 'brown-bear'), (emojis['gray-wolf'], 'gray-wolf'), (emojis['giraffe'], 'giraffe'), (emojis['wild-dog'], 'wild-dog')],
        [('Settle the game', 'settle')],
    ]
    
    game_started_stats = """
**
Forest Ball Game is Selection (30)

After the game is settled, the unified betting record will be displayed

History of the last {len_his} games:
{history}
**
%s
""" % ad


    game_settle_stats = """
**
Forest Ball Game Settlement

prize result : {dealer} {odd} times

Player list:
{player_list}

History of the last {len_his} games:
{history}
**
%s
""" % ad
    
    user_settle_stats = "   {name} : {status} {reward}"
    
    flood_select_times = "in the game you can only select 8 elements"
    
    select_duplicate_warning = "you can not select an duplicate item"
    
    select_stats_answer = """
Your Selected items :

{selects_list}

At the time of settlement, the reward will be settled according to the proportion of the bet on the animal you pressed
"""    


class Roulette:
    name = "Roulette Wheel"
    
    buttons_game = [
        [('1%', '1:roulette'), ('3%', '3:roulette'), ('5%', '5:roulette')],
        [('10%', '10:roulette'), ('20%', '20:roulette'), ('30%', '30:roulette')],
        [('50%', '50:roulette'), ('70%', '70:roulette'), ('100%', '100:roulette')],
        [('Start', 'start'), ('Balance', 'balance'), ('Sign In', 'sign-in')],
    ]

    buttons_control_game = [
        [('1', 'roul:1'), ('2', 'roul:2'), ('3', 'roul:3'), ('4', 'roul:4'), ('5', 'roul:5'), ('6', 'roul:6')],
        [('Large', 'large'), ('Small', 'small'), ('Single', 'single'), ('Double', 'double')],
        [('Settle the game', 'settle')],
    ]
    
    user_game_stats = "   {name} : {status} {select}"
    
    user_settle_stats = "   {name} : {select} {status} {reward}"
    
    game_started_stats = """
**
Small Roulette Selection (30)

Player list:
{player_list}

History of the last {len_his} games:
{history}
**
%s
""" % ad


    game_settle_stats = """
**
Small Roulette Settlement

Dice : {dealer}

Player list:
{player_list}

History of the last {len_his} games:
{history}
**
%s
""" % ad
    
    flood_select_times = "in the game you can change your only select 3 times"


class SpeedHa:
    name = "Speed HaHa"
    
    buttons_game = [
        [('50%', '50:speedha'), ('100%', '100:speedha')],
        [('Start', 'start'), ('Balance', 'balance'), ('Sign In', 'sign-in')],
    ]

    buttons_control_game = [
        [('Large', 'speedha:large'), ('Small', 'speedha:small')],
        [('Settle the game', 'settle')],
    ]
    
    user_game_stats = "   {name} : {status} {select}"
    
    user_settle_stats = "   {name} : {select} {status} {reward}"
    
    game_started_stats = """
**
Speed haha Selection (30)

Player list:
{player_list}

History of the last {len_his} games:
{history}
**
%s
""" % ad


    game_settle_stats = """
**
Speed haha Settlement

Dice : {dealer}

Player list:
{player_list}

History of the last {len_his} games:
{history}
**
%s
""" % ad
    
    flood_select_times = "in the game you can change your only select 3 times"


class Kuisan:
    name = "Kuisan"
    
    buttons_game = [
        [('1%', '1:kuisan'), ('3%', '3:kuisan'), ('5%', '5:kuisan')],
        [('10%', '10:kuisan'), ('20%', '20:kuisan'), ('30%', '30:kuisan')],
        [('50%', '50:kuisan'), ('70%', '70:kuisan'), ('100%', '100:kuisan')],
        [('Start', 'start'), ('Balance', 'balance'), ('Sign In', 'sign-in')],
    ]

    buttons_control_game = [
        [('3', 'kuisan:3'), ('4', 'kuisan:4'), ('5', 'kuisan:5'), ('6', 'kuisan:6'),('7', 'kuisan:7'), ('8', 'kuisan:8'),],
        [('9', 'kuisan:9'), ('10', 'kuisan:10'), ('11', 'kuisan:11'), ('12', 'kuisan:12'), ('13', 'kuisan:13'), ('14', 'kuisan:14'), ],
        [('15', 'kuisan:15'), ('16', 'kuisan:16'), ('17', 'kuisan:17'), ('18', 'kuisan:18'),],
        [('Large', 'kuisan:large'), ('Small', 'kuisan:small'), ('Single', 'kuisan:single'), ('Double', 'kuisan:double')],
        [('Large Single', 'kuisan:large_single'), ('Small Single', 'kuisan:small_single'), ('Large Double', 'kuisan:large_double'), ('Small Double', 'kuisan:small_double')],
        [('Leopard', 'kuisan:leopard'), ('Shunzi', 'kuisan:shunzi'), ('Pair', 'kuisan:pair')],
        [('Settle the game', 'settle')],
    ]
    
    user_game_stats = "   {name} : {status} {select}"
    
    user_settle_stats = "   {name} : {select} {status} {reward}"
    
    game_started_stats = """
**
Kuisan Selection (30)

Player list:
{player_list}

History of the last {len_his} games:
{history}
**
%s
""" % ad


    game_settle_stats = """
**
Kuisan Settlement

{dealer}

Player list:
{player_list}

History of the last {len_his} games:
{history}
**
%s
""" % ad
    
    flood_select_times = "in the game you can only select 3 times"



class LuckyAirship:
    name = "Lucky Airship"
    
    buttons_game = [
        [('1%', '1:lucky'), ('3%', '3:lucky'), ('5%', '5:lucky')],
        [('10%', '10:lucky'), ('20%', '20:lucky'), ('30%', '30:lucky')],
        [('50%', '50:lucky'), ('70%', '70:lucky'), ('100%', '100:lucky')],
        [('Start', 'start'), ('Balance', 'balance'), ('Sign In', 'sign-in')],
    ]

    buttons_control_game = [
        [('first place', 'lucky:place:1'), ('2nd place', 'lucky:place:2'), ('3nd place', 'lucky:place:3'), ('fourth place', 'lucky:place:4'), ('the fifth place', 'lucky:place:5'), ],
        [('six place', 'lucky:place:6'), ('seven place', 'lucky:place:7'), ('eight place', 'lucky:place:8'), ('nine place', 'lucky:place:9'), ('ten place', 'lucky:place:10'), ],
        [('1', 'lucky:1'), ('2', 'lucky:2'), ('3', 'lucky:3'), ('4', 'lucky:4'), ('5', 'lucky:5'), ],
        [('6', 'lucky:6'), ('7', 'lucky:7'), ('8', 'lucky:8'), ('9', 'lucky:9'), ('10', 'lucky:10'), ],
        [('Settle the game', 'settle')],
    ]
    
    user_game_stats = "   {name} : {status} {place} {selects}"
    
    user_settle_stats = "   {name} : {place} {selects} {status} {reward}"
    
    game_started_stats = """
**
Lucky Airship Selection (30)

Player List :
{player_list}

History of the last {len_his} games:
{history}
**
%s
""" % ad


    game_settle_stats = """
**
Lucky Airship Settlement

{dealer}

Player List :
{player_list}

History of the last {len_his} games:
{history}
**
%s
""" % ad
    
    flood_select_times = "in the game you can only select 7 items"
    flood_place_times = "in the game you can only change your place 3 times"
    place_required_warning = "you must select an place firstly"
    select_duplicate_warning = "you can not select an duplicate item"
    


# convert tuples to Button object 
Blackjack_21.buttons_game = list(map(lambda y: list(
    map(lambda x: Button.inline(text=x[0], data=x[1]), y)), Blackjack_21.buttons_game))

Blackjack_21.buttons_control_game = list(map(lambda y: list(
    map(lambda x: Button.inline(text=x[0], data=x[1]), y)), Blackjack_21.buttons_control_game))

NiuNiu.buttons_game = list(map(lambda y: list(
    map(lambda x: Button.inline(text=x[0], data=x[1]), y)), NiuNiu.buttons_game))

NiuNiu.buttons_control_game = list(map(lambda y: list(
    map(lambda x: Button.inline(text=x[0], data=x[1]), y)), NiuNiu.buttons_control_game))

ForestBall.buttons_game = list(map(lambda y: list(
    map(lambda x: Button.inline(text=x[0], data=x[1]), y)), ForestBall.buttons_game))

ForestBall.buttons_control_game = list(map(lambda y: list(
    map(lambda x: Button.inline(text=x[0], data=x[1]), y)), ForestBall.buttons_control_game))

Roulette.buttons_game = list(map(lambda y: list(
    map(lambda x: Button.inline(text=x[0], data=x[1]), y)), Roulette.buttons_game))

Roulette.buttons_control_game = list(map(lambda y: list(
    map(lambda x: Button.inline(text=x[0], data=x[1]), y)), Roulette.buttons_control_game))

SpeedHa.buttons_game = list(map(lambda y: list(
    map(lambda x: Button.inline(text=x[0], data=x[1]), y)), SpeedHa.buttons_game))

SpeedHa.buttons_control_game = list(map(lambda y: list(
    map(lambda x: Button.inline(text=x[0], data=x[1]), y)), SpeedHa.buttons_control_game))

Kuisan.buttons_game = list(map(lambda y: list(
    map(lambda x: Button.inline(text=x[0], data=x[1]), y)), Kuisan.buttons_game))

Kuisan.buttons_control_game = list(map(lambda y: list(
    map(lambda x: Button.inline(text=x[0], data=x[1]), y)), Kuisan.buttons_control_game))

LuckyAirship.buttons_game = list(map(lambda y: list(
    map(lambda x: Button.inline(text=x[0], data=x[1]), y)), LuckyAirship.buttons_game))

LuckyAirship.buttons_control_game = list(map(lambda y: list(
    map(lambda x: Button.inline(text=x[0], data=x[1]), y)), LuckyAirship.buttons_control_game))

buttons_end_game = list(map(lambda y: list(
    map(lambda x: Button.inline(text=x[0], data=x[1]), y)), buttons_end_game))

buttons_ad_panel = list(map(lambda y: list(
    map(lambda x: Button.inline(text=x[0], data=x[1]), y)), buttons_ad_panel)) 