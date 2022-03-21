from config import ad
from telethon.sync import Button

# public messages

buttons_end_game = [
    [('查询余额', 'balance'), ('签到领钱', 'sign-in')],
]


buttons_ad_panel = [
    [('Add New Ad', 'add_ad'), ('Remove Ad', 'remove_ad')],
    [('Set Static Ad', 'set_static'), ('Refresh list', 'refresh')],
]

display_balance = """
{name}
余额: {balance}
本周累计胜: {week_wins}
财产清单: {fortune}
"""

sign_in_reward = """
签到成功 
    系统赠送了您：${reward}
    梭哈一时爽，请理性游戏~
    每秒可再次签到领取
"""

sign_in_warning = "{sign_time}秒内限定签到一次!"

top_ten_rank = """**
🏆财富富豪榜🏆
{top_ten}

*榜单由所有玩家财富进行排名
*榜单每十分钟更新一次
*您当前的排名： {rank}
**
"""

not_in_list = "not in list"

not_enough_balance = "你的硬币不够 !"

user_bet_stat = "【{title}】{name} : {amount}"

adding_bet = """
成功的选择
您当前的总赌注: {amount}
无人呼叫请在6秒后点击开始游戏!  
"""

not_game_warning = "目前没有用户投注，请等待用户投注后开始游戏 "

start_6s_warning = "请在6秒后开始游戏"

settle_game_warning = "目前没有用户投注，请等待用户投注后开始游戏"

make_game_flood_warning = """
有限的开始
每个会话窗口可以在{limit}秒内创建一个游戏  
新游戏可以在前一款游戏结束后立即解锁  
"""

transfer_wrong_format = """
错误的格式  
请回复需要转账的消息，然后输入转账指令:  
/zz 转帐金额  
每次转账将扣除10%的手续费 
"""

transfer_to_not_sign = "不能转移到未登录的用户"

transfer_not_enough = "余额不足，转账金额: {amount}"

transfer_status = "转账成功，实际学分:{credit}，手续费:{fee} "


add_money_wrong_format = """
请输入存款指示:  
/zengjia user_id 数量 
"""

add_to_not_sign = "不能向未登录的用户存钱吗"

overflow_error = "溢出错误，数量非常大"

raises_5time_warning = "如果每款游戏的提升次数超过5次，这个提升就失败了! "


start_game =  """
{game_name} 正在投注

%s
""" % ad


bet_stats = """
**
{game_name} 选择中

用户列表
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

sign_in_high_balance_warning = "您当前的资金（{sign_limit_balance}）充足，不可签到 "

start_menu = "Hi !"


game_not_completed_warning = "球员们还在比赛呢!"

wait_time_after_select = "请在上次选择后等待6秒!"


del_money_wrong_format = """
请输入存款指示:
/sl user_id amount
(对于所有用户，将用户id替换为' all ')
"""
add_money_status = "成功添加金钱，添加金额:' {amount} '，目标用户:' {user} '  "

delete_money_status = "成功删除金额，删除金额:' {amount} '，目标用户:' {user} '  "


deposit_status = """
您的活期存款是: ${amount}
存款指令: /ck amount
存入金额 >= $100,0000
"""

deposit_limit_warning = "一次存款金额必须是>= $100,0000"

deposit_success = """
成功存款，活期存款:{amount}
"""


deposit_not_enough = """
存款金额不能大于当前余额，当前余额:${balance}  
"""

withdraw_status = """
您的活期存款为:{amount}  
提现说明:/qk 金额  
数量> = $100,0000
"""

withdraw_warning = "每次提款金额不得少于$100,000。 提现金额为:   ${amount}"


withdraw_success = """
退出成功  
这个撤军:${withdraw}  
活期存款:${deposit}  
"""

withdraw_not_enough = "支取金额不得大于活期存款金额，活期存款:   ${deposit}"

private_commands_warnings = "此命令仅在私有情况下有效"

red_envelope_minimum_amount = "红包金额不能少于 $1000,0000"

red_envelope_minimum_count = "红包数量不能少于3个，也不能超过100个  "

red_envelope_stats = """
中文: {user}
发了个红包  
数量: {amount}
红包数量: {count}

%s
""" % ad



red_envelope_graber_stats = "   {name} : {reward}"

red_envelope_end_stats = """
中文: {user}
发了个红包  
数量: {amount}
红包数量: {count}

收集细节 :
{grabers_list}

🎉这个游戏的幸运之王是:
{lucky}
%s
""" % ad

red_envelope_button = "🧧 拿红包"

red_envelope_grabed = " 恭喜你，你得到了{amount}金币"

red_envelope_duplicate_warning = "这个红包你已经抢过了，不能在这里收  "

red_envelope_not_exists = "这个信封已经不存在了"

red_envelope_give_back = "${amount} 因为未完成的信封被退回到你的余额中  "

red_envelope_not_enough_balance = "你的余额不够!"

set_title_description = """
使用自定义标题函数的说明  
私人聊天机器人使用以下命令格式  
/settitle 定义标题  
例如  
/settitle 最好  
使用的限制  
标题字符长度大于0且小于或等于4  
不能自定义为系统默认名称  
当前设置自定义标题功能费用:$500  
"""

set_title_wrong_length = "标题长度不能超过4，当前长度: {length}"

set_title_succes = """
题目设置完成  
当前标题:{title}  
"""

set_title_money_not_enough = """
余额不足  
创建一款游戏需要花费$500 
"""

settings_description = """
当前设置:  
{settings}  
 
更改设置的命令格式:  
`/settings key value`
"""

settings_invalid_key = "无效\"{key}\" !"

settings_changed = """
{key}的值更改成功  
旧值:{Old}  
新值:{value}  
"""

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
21点黑杰克 正在游戏中 :

%s
""" % ad
    
    bet_stats = """
**
21点 黑杰克 选择中

玩家列表:
{player_list}
**
%s
""" % ad
    
    
    game_started_stats = """
**
21点 黑杰克 选择中 (30)

庄家: {dealer}

玩家列表:
{player_list}
**
%s
""" % ad
    
    user_game_stats = "【{title}】{name} : {cards} , 总分 : {score} ({status})"


    suspend_askcard_warning = "你已经暂停交易，不能继续要求牌" 


    stnad_warning = "你不是在玩 !" 

    user_settle_stats = "【{title}】{name} : {cards} , 总分 : {score} ({status}) {amount}"

    dealer_settle_stats = "【{title}】{cards} , 总分 : {score} ({status})"



class NiuNiu:
    name = "娱乐牛牛"
    
    buttons_game = [
        [('1%', '1:niuniu'), ('3%', '3:niuniu'), ('5%', '5:niuniu')],
        [('10%', '10:niuniu'), ('20%', '20:niuniu'), ('30%', '30:niuniu')],
        [('50%', '50:niuniu'), ('70%', '70:niuniu'), ('100%', '100:niuniu')],
        [('开始游戏', 'start'), ('查询余额', 'balance'), ('签到', 'sign-in')],
    ]

    buttons_control_game = [
        [('青龙', 'qinglong'), ('白虎', 'white-tiger'), ('朱雀', 'suzaku'), ('玄武', 'xuanwu')],
        [('结算游戏', 'settle')],
    ]
    
    game_started_stats = """
**
娱乐牛牛 选择中 (30)

玩家列表:
{player_list}

最近{len_his}场历史记录:
{history}
**
%s
""" % ad


    game_settle_stats = """
**
娱乐牛牛 选择中

庄家 ({0})
青龙 ({1}), 白虎 ({2})
朱雀 ({3}), 玄武 ({4})

玩家列表:
{player_list}

最近{len_his}场历史记录:
{history}
**
%s
""" % ad
    
    user_game_stats = "【{title}】{name} : {status} {choice}"
    
    user_settle_stats = "【{title}】{name} : {choice} {status} {amount}"
    
    flood_select_times = "在每个游戏中，你只能改变3次选择  "


class ForestBall:
    name = "森林舞会"
    
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
        [('开始游戏', 'start'), ('查询余额', 'balance'), ('签到', 'sign-in')],
    ]

    buttons_control_game = [
        [(emojis['panda'], 'panda'), (emojis['lion'], 'lion'), (emojis['tiger'], 'tiger'), (emojis['cheetah'], 'cheetah')],
        [(emojis['brown-bear'], 'brown-bear'), (emojis['gray-wolf'], 'gray-wolf'), (emojis['giraffe'], 'giraffe'), (emojis['wild-dog'], 'wild-dog')],
        [('结算游戏', 'settle')],
    ]
    
    game_started_stats = """
**
森林舞会 正在进行中 (30)

比赛结束后统一显示结果

最近{len_his}场历史记录:
{history}
**
%s
""" % ad


    game_settle_stats = """
**
森林舞会 正在选择中

庄家 : {dealer} {odd} times

玩家列表:
{player_list}

最近{len_his}场历史记录:
{history}
**
%s
""" % ad
    
    user_settle_stats = "【{title}】{name} : {status} {reward}"
    
    flood_select_times = "在游戏中你只能选择8个元素"
    
    select_duplicate_warning = "您不能选择重复的项目"
    
    select_stats_answer = """
您所选择的项目:

{selects_list}

结算时，将根据您所压动物的投注比例来结算奖励  
"""  


class Roulette:
    name = "轮盘"
    
    buttons_game = [
        [('1%', '1:roulette'), ('3%', '3:roulette'), ('5%', '5:roulette')],
        [('10%', '10:roulette'), ('20%', '20:roulette'), ('30%', '30:roulette')],
        [('50%', '50:roulette'), ('70%', '70:roulette'), ('100%', '100:roulette')],
        [('开始游戏', 'start'), ('查询余额', 'balance'), ('签到', 'sign-in')],
    ]

    buttons_control_game = [
        [('1', 'roul:1'), ('2', 'roul:2'), ('3', 'roul:3'), ('4', 'roul:4'), ('5', 'roul:5'), ('6', 'roul:6')],
        [('Large', 'large'), ('Small', 'small'), ('Single', 'single'), ('Double', 'double')],
        [('结算游戏', 'settle')],
    ]
    
    user_game_stats = "【{title}】{name} : {status} {select}"
    
    user_settle_stats = "【{title}】{name} : {select} {status} {reward}"
    
    game_started_stats = """
**
轮盘游戏 正在进行中 (30)

玩家列表:
{player_list}

最近{len_his}场历史记录:
{history}
**
%s
""" % ad


    game_settle_stats = """
**
轮盘游戏正在选择中

庄家 : {dealer}

玩家列表:
{player_list}

最近{len_his}场历史记录:
{history}
**
%s
""" % ad
    
    flood_select_times = "在游戏中，你可以改变你唯一的选择3次  "


class SpeedHa:
    name = "快三"
    
    buttons_game = [
        [('50%', '50:speedha'), ('100%', '100:speedha')],
        [('开始游戏', 'start'), ('查询余额', 'balance'), ('签到', 'sign-in')],
    ]

    buttons_control_game = [
        [('大', 'speedha:large'), ('小', 'speedha:small')],
        [('结算游戏', 'settle')],
    ]
    
    user_game_stats = "【{title}】{name} : {status} {select}"
    
    user_settle_stats = "【{title}】{name} : {select} {status} {reward}"
    
    game_started_stats = """
**
急速梭哈正在进行中 (30)

玩家列表:
{player_list}

最近{len_his}场历史记录:
{history}
**
%s
""" % ad


    game_settle_stats = """
**
急速梭哈正在选择中

庄家 : {dealer}

玩家列表:
{player_list}

最近{len_his}场历史记录:
{history}
**
%s
""" % ad
    
    flood_select_times = "在游戏中，你可以改变你唯一的选择3次  "


class Kuisan:
    name = "快三"
    
    buttons_game = [
        [('1%', '1:kuisan'), ('3%', '3:kuisan'), ('5%', '5:kuisan')],
        [('10%', '10:kuisan'), ('20%', '20:kuisan'), ('30%', '30:kuisan')],
        [('50%', '50:kuisan'), ('70%', '70:kuisan'), ('100%', '100:kuisan')],
        [('▶️开始游戏', 'start'), ('💰查询余额', 'balance'), ('✅签到领钱', 'sign-in')],
    ]

    buttons_control_game = [
        [('3', 'kuisan:3'), ('4', 'kuisan:4'), ('5', 'kuisan:5'), ('6', 'kuisan:6'),('7', 'kuisan:7'), ('8', 'kuisan:8'),],
        [('9', 'kuisan:9'), ('10', 'kuisan:10'), ('11', 'kuisan:11'), ('12', 'kuisan:12'), ('13', 'kuisan:13'), ('14', 'kuisan:14'), ],
        [('15', 'kuisan:15'), ('16', 'kuisan:16'), ('17', 'kuisan:17'), ('18', 'kuisan:18'),],
        [('大', 'kuisan:large'), ('小', 'kuisan:small'), ('单', 'kuisan:single'), ('双', 'kuisan:double')],
        [('大单', 'kuisan:large_single'), ('小单', 'kuisan:small_single'), ('大双', 'kuisan:large_double'), ('小双', 'kuisan:small_double')],
        [('豹子', 'kuisan:leopard'), ('顺子', 'kuisan:shunzi'), ('对子', 'kuisan:pair')],
        [('🀄️结算游戏🀄️', 'settle')],
    ]
    
    user_game_stats = "【{title}】{name} : {status} {select}"
    
    user_settle_stats = "【{title}】{name} : {select} {status} {reward}"
    
    game_started_stats = """
**
快三 正在进行中 (30)

玩家列表:
{player_list}

最近{len_his}场历史记录:
{history}
**
%s
""" % ad


    game_settle_stats = """
**
快三 正在选择中

庄家 : {dealer}

玩家列表:
{player_list}

最近{len_his}场历史记录:
{history}
**
%s
""" % ad
    
    flood_select_times = "在游戏中你只能选择3次"



class LuckyAirship:
    name = "幸运飞艇"
    
    buttons_game = [
        [('1%', '1:lucky'), ('3%', '3:lucky'), ('5%', '5:lucky')],
        [('10%', '10:lucky'), ('20%', '20:lucky'), ('30%', '30:lucky')],
        [('50%', '50:lucky'), ('70%', '70:lucky'), ('100%', '100:lucky')],
        [('开始游戏', 'start'), ('查询余额', 'balance'), ('签到', 'sign-in')],
    ]

    buttons_control_game = [
        [('冠军', 'lucky:place:1'), ('亚军', 'lucky:place:2'), ('季军', 'lucky:place:3'), ('第四名', 'lucky:place:4'), ('第五名', 'lucky:place:5'), ],
        [('第六名', 'lucky:place:6'), ('第七名', 'lucky:place:7'), ('第八名', 'lucky:place:8'), ('第九名', 'lucky:place:9'), ('第十名', 'lucky:place:10'), ],
        [('1', 'lucky:1'), ('2', 'lucky:2'), ('3', 'lucky:3'), ('4', 'lucky:4'), ('5', 'lucky:5'), ],
        [('6', 'lucky:6'), ('7', 'lucky:7'), ('8', 'lucky:8'), ('9', 'lucky:9'), ('10', 'lucky:10'), ],
        [('结算游戏', 'settle')],
    ]
    
    user_game_stats = "【{title}】{name} : {status} {place} {selects}"
    
    user_settle_stats = "【{title}】{name} : {place} {selects} {status} {reward}"
    
    game_started_stats = """
**
幸运飞艇 正在进行中 (30)

玩家列表 :
{player_list}

最近{len_his}场历史记录:
{history}
**
%s
""" % ad


    game_settle_stats = """
**
幸运飞艇 正在选择中

庄家 : {dealer}

玩家列表 :
{player_list}

最近{len_his}场历史记录:
{history}
**
%s
""" % ad
    
    flood_select_times = "在游戏中你只能选择7个项目"
    flood_place_times = "在游戏中，你只能改变3次位置  "
    place_required_warning = "你必须先选择一个地方"
    select_duplicate_warning = "您不能选择重复的项目"
    


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