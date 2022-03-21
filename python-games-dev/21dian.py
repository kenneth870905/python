# 21点扑克牌游戏python实现
# 游戏者的目标是使手中的牌的点数之和不超过21点且尽量大。
# 计算规则是：
# 2至9牌，按其原点数计算,A算作1点（在我这个程序里）
# 10、J、Q、K牌都算作10点（一般记作T，即Ten）
""" 21点扑克牌游戏设计思路
按下列规则模拟21点扑克牌游戏：
计算机人工智能AI作为庄家(House)，用户作为玩家(Player) 。
游戏开始时， 庄家从洗好的一副牌中发牌：第1张牌发给玩家， 第2张牌发给庄家，第3张牌发给玩家，第4张牌发给庄家。
然后，询问玩家是否需要继续“拿牌”，通过一次或多次“拿牌”，玩家尝试使手中扑克牌的点数和接近21。如果玩家手中扑克牌的点数之和超过21，则玩家输牌。
当玩家决定 “停牌”(即，不再“拿牌”)，则轮到庄家使用下列规则(“庄家规则”)“拿牌”：如果庄家手中的最佳点数之和小于17，则必须“拿牌”:，如果点数之和大于或等于17，则“停牌”。如果庄家的点数之和超过21,则玩家获胜。
最后， 比较玩家和庄家的点数。如果玩家的点数大，则获胜。如果玩家的点数小，则输牌。如果点数相同，则平局。但玩家和庄家的牌值都是21点，此时拥有blackjack (一张Ace 和一张点数为10的牌)方获胜。
"""
import random


def get_shuffled_deck():  # 初始化洗好的牌
    suits = {'♣', '♠', '♦', '♥'}
    ranks = {'2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A'}
    deck = []
    # 创建一副52张的扑克牌
    for suit in suits:
        for rank in ranks:
            deck.append(suit + ' ' + rank)
    random.shuffle(deck)
    return deck


# 发一张牌给参与者participant
def deal_card(deck, participant):
    card = deck.pop()  # 取一张牌赋值给card，一般是最后一张
    participant.append(card)
    return card


# 玩家拿牌： 询问玩家是否继续拿牌，如果是，继续给玩家发牌(调用函数deal_ card()) ，并计算玩家牌点compute_total()，如果大于21点，输出“玩家输牌!”信息，并返回。

# 计算并返回一手牌的点数和
def compute_total(hand):
    values = {'A': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 10, 'Q': 10,
              'K': 10}
    result = 0  # 初始化点数为0
    for card in hand:
        result += values[card[2:]]
    return result


def print_hand(hand):
    for card in hand:
        print(card, end=',')
    print()


def blackjack():
    deck = get_shuffled_deck()
    house = []  # 庄家的牌
    Player = []  # 玩家的牌

    # 依次给玩家和庄家各发两张牌
    for i in range(2):
        deal_card(deck, Player)
        deal_card(deck, house)
    # 打印一手牌
    print('庄家的牌：', end=' ');
    print_hand(house)
    print('玩家的牌：', end=' ');
    print_hand(Player)

    # 询问玩家是否继续拿牌，如果是，继续给玩家发牌
    answer = input('是否继续拿牌（y/n,缺省为y）:')
    while answer in ('', 'y', 'Y'):
        card = deal_card(deck, Player)
        print('玩家拿到的牌为：', end='');
        print_hand(Player);
        # 计算牌点
        if compute_total(Player) > 21:
            print('爆掉，玩家输了！')
            return
        answer = input('是否继续拿牌（y/n,缺省为y）:')

    # 庄家（计算人工智能）按“庄家规则”确定是否拿牌
    while compute_total(house) < 17:
        card = deal_card(deck, house)
        print('庄家拿到的牌为：', end='');
        print_hand(house)
        # 计算牌点
        if compute_total(house) > 21:
            print('爆掉，庄家输了！')
            return

    # 分别计算庄家和玩家的点数，比较点数大小，输出输赢结果信息
    houseTotal, playerTotal = compute_total(house), compute_total(Player)
    if houseTotal >= playerTotal:
        print('庄家赢！')
    else:
        print('玩家赢！')


if __name__ == '__main__':
    blackjack()