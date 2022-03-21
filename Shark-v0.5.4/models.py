from random import randint
from sqlite3.dbapi2 import OperationalError
import time
import sqlite3
import re
import json

class User:
    def __init__(self, user_id: int, name: str, balance: int, week_wins: int = 0, week_time: float = time.time(), sign_time: float = time.time(), rank: int = None, title : str = None):
        self.id = user_id
        self.name = name
        self.balance = int(balance)
        self.week_wins = week_wins
        self.week_time = week_time
        self.sign_time = sign_time
        self.rank = rank
        self.title = title
        # define after initialize
        self.tuple = (self.id, self.name, self.balance,
                      self.week_wins, self.week_time, self.sign_time)
        self.fortune = None
        self.deposit = 0

    def __eq__(self, __o: object) -> bool:
        return self.id == __o

    def __str__(self) -> str:
        return " , ".join(map(str, self.tuple))


class Database:
    def __init__(self, db_file: str):
        self.connection = sqlite3.connect(db_file)
        # players table
        self.connection.execute('''
CREATE TABLE IF NOT EXISTS players(
id INTEGER PRIMARY KEY NOT NULL,
name TEXT NOT NULL,
balance TEXT NOT NULL,
wins INTEGER NULL,
week REAL NULL,
sign REAL NULL,
rank INTEGER NULL,
title TEXT NULL);
''')
        # investment and deposit table
        self.connection.execute("""
CREATE TABLE IF NOT EXISTS investors(
id INTEGER PRIMARY KEY NOT NULL,
amount str);
""")
        # alter tables
        try:
            self.connection.execute("ALTER TABLE players ADD COLUMN title TEXT NULL")
        except OperationalError:
            pass

        self.connection.commit()

    def get_user(self, user_id: int):
        for user in self.connection.execute("SELECT * FROM players WHERE id = ?", (user_id, )):
            user = User(*user)
            return user
        return False

    def add_user(self, user: User):
        parameters = (
                user.id, user.name,
                str(user.balance),
                user.week_wins,
                user.week_time,
                user.sign_time,
                user.rank,
                user.title,
                )
        self.connection.execute(
            'INSERT INTO players VALUES (?, ?, ?, ?, ?, ?, ?, ?)', parameters)
        self.connection.commit()


    def update_name(self, user: User):
        parameters = (user.name, user.id, )
        self.connection.execute('UPDATE players SET name = ? WHERE id = ?', parameters)
        self.connection.commit()
    
    def add_balance(self, user : User, amount : int):
        # syncwith database
        user = self.get_user(user.id)
        new_balance = user.balance + amount
        parameters = (str(new_balance), user.sign_time, user.id, )
        self.connection.execute("UPDATE players SET balance = ?, sign = ? WHERE id = ?;", parameters)
        # commmit
        self.connection.commit()
        # return user object
        user = self.get_user(user.id)
        # check nevigate balances
        if user.balance < 0:
            # make balance zero
            user = self.add_balance(user, -user.balance)
        return user
    
    def add_balance_all(self, amount : int):
        # inceease balance of all users
        # load all users
        users = self.connection.execute("SELECT balance, id FROM players;")
        # add balance to users
        add_money = lambda b : 0 if (b + amount < 0) else b + amount
        if amount < 0:
            # print('需要扣除存款')
            for u in users:
                if int(u[0]) + amount < 0:
                    old_deposit = self.get_deposit(u[1])
                    deposit_amount = int(old_deposit) + ( int(u[0]) + amount) if (int(old_deposit) + ( int(u[0]) + amount)) > 0  else 0
                    paramteres = (str(deposit_amount), u[1])
                    self.connection.execute("UPDATE investors SET amount = ? WHERE id = ?", paramteres)
                # print(u[0])

        users = map(lambda u : (str(add_money(int(u[0]))), u[1]), users)
        # add new data to database and commit
        self.connection.executemany("UPDATE players SET balance = ? WHERE id = ?", users)
        self.connection.commit()
    
    def add_win(self, user : User, zero = False):
        if zero:
            self.connection.execute("UPDATE players SET wins = 0, week = ? WHERE id = ?;", (user.week_time, user.id))
        else:
            self.connection.execute("UPDATE players SET wins = wins + 1, week = ? WHERE id = ?;", (user.week_time, user.id))
            
        # commmit
        self.connection.commit()
        # return user object
        return self.get_user(user.id)

    def ranking(self, count=10):
        # get all users
        users = tuple(self.connection.execute("SELECT id, name, balance from players;"))
        # sort by
        users = sorted(users, key=lambda user : int(user[2]), reverse=True)
        users = tuple(map(lambda user: (users.index(user)+1, *user), users))
        # update users rank column
        users_ranking = map(lambda user: (user[0], user[1], ), users)
        self.connection.executemany("UPDATE players SET rank = ? WHERE id = ?;", users_ranking)
        self.connection.commit()
        # return top users
        top_users = users[:count]
        return top_users
    
    def get_deposit(self, user_id : int) -> int:
        if type(user_id) == User:
            user_id = user_id.id
        # get deposit amount in investors table
        for record in self.connection.execute("SELECT amount FROM investors WHERE id = ?", (user_id, )):
            return record[0]
        # make new record for new user
        paramteres = (user_id, 0)
        self.connection.execute("INSERT INTO investors VALUES (?, ?)", paramteres)
        return 0
    
    def make_deposit(self, user : User, amount : int) -> int:
        # decrease the user balance
        user = self.add_balance(user, - amount)
        # increase old deposit amount
        old_deposit = self.get_deposit(user)
        deposit_amount = int(old_deposit) + amount
        paramteres = (str(deposit_amount), user.id)
        self.connection.execute("UPDATE investors SET amount = ? WHERE id = ?", paramteres)
        # commit and save
        self.connection.commit()
        return deposit_amount
    
    def change_title(self, user : User, title : str):
        # change user's title
        paramteres = (title, user.id)
        self.connection.execute('UPDATE players SET title = ? WHERE id = ?', paramteres)

    def add_investors_amount(self,user,amount):
        old_deposit = self.get_deposit(user)
        deposit_amount = int(old_deposit) + amount if (int(old_deposit) + amount) > 0  else 0

        paramteres = (str(deposit_amount), user.id)
        self.connection.execute("UPDATE investors SET amount = ? WHERE id = ?", paramteres)
        # commit and save
        self.connection.commit()


    # 删除金额多少组
    def dete_balance_all(self,n):
        users = self.connection.execute("SELECT balance, id FROM players;")
        # print(n)
        # print(users)
        newUsers = []
        user2 = []
        for x in users:
            if len(x[0]) < n*4:
                newUsers.append((0,x[1]))
                # 删除存款
                old_cunkuan = self.get_deposit(x[1])
                old_cunkuan = str(old_cunkuan)
                cunkuan = old_cunkuan[ 0: len(old_cunkuan) - (n*4 - len(x[0])) ]
                if not cunkuan:
                    cunkuan = 0
                user2.append( (cunkuan , x[1]) )
            else:
                qian = x[0][0: len(x[0]) - (n * 4) ]
                newUsers.append((qian,x[1]))
        self.connection.executemany("UPDATE players SET balance = ? WHERE id = ?", newUsers)
        self.connection.commit()

        if len(user2) > 0:
            self.connection.executemany("UPDATE investors SET amount = ? WHERE id = ?", user2)


class Card:
    def __init__(self, value: int, symbol: str = '') -> None:
        self.value = value
        # the symbol is same value between 2 and 9 cards
        if (not symbol) and (2 <= self.value <= 10):
            self.symbol = str(self.value)
        else:
            self.symbol = symbol
            
    def __eq__(self, __o: object) -> bool:
        return self.value == __o
    
    def __lt__(self, other_card):
        return self.value < other_card.value


class Deck:
    # a deck for playing blackjack
    def __init__(self, duplicate : bool = False):
        self.cards : Card = 4 * [
            Card(1, 'A'), Card(2), Card(3), Card(4), Card(5),
            Card(6), Card(7), Card(8), Card(9), Card(10),
            Card(10, 'J'), Card(10, 'Q'), Card(10, 'K'),
        ]
        self.duplicate = duplicate

    def choose_random_card(self, ):
        # select a random card and remove it
        position = randint(0, len(self.cards)-1)
        selected_card = self.cards[position]
        if not self.duplicate:
            del self.cards[position]
        return selected_card


class Status:
    class Lose:
        def __str__(self) -> str:
            return "输"
    class Win:
        def __str__(self) -> str:
            return "赢"
    class Playing:
        def __str__(self) -> str:
            return "选择中"
    class Stand:
        def __str__(self) -> str:
            return "停牌🔔"
    class Draw:
        def __str__(self) -> str:
            return "退回"
    class Blackjack:
        def __str__(self) -> str:
            return "黑杰克🤡"
    class Selecting:
        def __str__(self) -> str:
            return "🕔"
    class Selected:
        def __str__(self) -> str:
            return "✅"
    class TimeOut:
        def __str__(self) -> str:
            return "退回"
    
class GameStatus:
    class Clsoed:
        pass
    class Open:
        pass

class Player:
    def __init__(self, user: User = None) -> None:
        if user:
            self.user = user
            self.id = user.id
        # after initialize
        self.bet_amount = 0
        self.profit = 0
        self.bet_times = 0
        self.score = 0
        self.status : Status = Status.Playing()
        self.cards: list[Card] = []

    def calculate_score(self):
        # clear cards snd score
        self.score = 0
        #calclulate
        for card in sorted(self.cards, reverse=True):
            if (card.value == 1) and (self.score <= 10):
                self.score += 11
            else:
                self.score += card.value
        return self.score
    
    def __eq__(self, __o: object) -> bool:
        return self.id == __o
    

class DefaultSettings(object):
    def __init__(self, title : str = 'Default', link : str = 't.me/telegram') -> None:
        self.title = title
        self.link = link


class Settings:
    def __init__(self, path : str):
        self.path = path
        self.data = DefaultSettings()
        
        try:
            # read the data
            data = json.load(open(self.path, 'r'))
            self.data = DefaultSettings(**data)
        except (FileNotFoundError, FileExistsError):
            # write new empty file to save data
            self.update()


    def update(self):
        # update json file
        json.dump(vars(self.data), open(self.path, 'w'))



class Game:
    name = "game"
    
    def __init__(self, game_id: int, database : Database, setting : Settings) -> None:
        self.id = game_id
        self.last_update = time.time()
        self.database = database
        # define affter initialize
        self.total = 0
        #self.players: list[Player] = []
        #self.deck = Deck()
        self.winners : list[Player] = []
        self.history = None
        self.status  = GameStatus.Open()
        self.stable_statuses = (Status.Lose, Status.Win, Status.Blackjack, Status.Draw, Status.Selected, Status.TimeOut)
        self.setting = setting

    def __eq__(self, __o: object) -> bool:
        return self.id == __o
    
    def play(self):
        pass
    
    def game_playing(self):
        for player in self.players:
            if (type(player.status) in (Status.Playing, Status.Selecting)):
                return True
        return False
    
    def add_bet(self, user: User, rate : int):
        pass

    def get_player(self, user_id: int):
        if user_id in self.players:
            return self.players[self.players.index(user_id)]
        else:
            return False
    
    def settle(self):
        #check players status
        if time.time() - self.last_update < 30:
            if self.game_playing() == True:
                return False
    
    async def update_stats(self, event, history, settle : bool = False):
        """ a method to update game status in telegram message """


class History:
    def __eq__(self, __o: object) -> bool:
        return type(self) == __o
    
class Group:
    def __init__(self, group_id : int, last_game= time.time()) :
        self.id = group_id
        self.last_game = last_game
        self.history : list[History] = []
        
    def __str__(self) -> str:
        return str(self.id)
    
    def __eq__(self, __o: object) -> bool:
        return self.id == __o


class errors:
    class AddBetLimit(Exception):
        """ an error when the bet times be more than 5 """
        pass
    class BalanceNotEnough(Exception):
        """ this happens when the user balance not enough to bet """
    class SelectLimit(Exception):
        """ an exception to limit the user selects times"""
    class SelectDuplicate(Exception):
        """ an exception when user want to select an duplicate element"""
    class PlayersArePlaying(Exception):
        """ an exception when a user want to settle the game but not all players are ready to it """
    class WaitTimeSelect(Exception):
        """ an exception when you want make settle and all users have a select but no much time passed from their selects """
    class GameIsClosed(Exception):
        """ an exception when user want to settle the game and game is closed """
    class PlaceLimit(Exception):
        """ an exception to limit the user's place selects times"""
    class PlaceRequired(Exception):
        """ an axception when user want toselecr a dice and doesn't select a place yet ! """

def separator(num: str):
    #sep_num = f"{num:,}"
    sep_num = ",".join(re.findall("\d{1,4}", str(num)[::-1]))[::-1]
    return sep_num

def cards_format(cards: list[Card]):
    return "".join(
        map(lambda x: f"🃏{x.symbol}", cards))

def format_amount(player : Player):
    if type(player.status) == Status.Lose:
        a = f"~~ -${separator(player.profit)} ~~"
    elif type(player.status) in (Status.Win, Status.Blackjack):
        a = f"+${separator(player.profit + player.bet_amount)}"
    elif type(player.status) in (Status.Draw, Status.TimeOut):
        a = f"+${separator(player.profit)}"
    return a

class Graber:
    def __init__(self, user : User, reward : int) -> None:
        self.user = user
        self.reward = reward
    
    def __eq__(self, __o: object) -> bool:
        return self.user.id == __o

class Envelope:
    """ ENvelope object to manage red envelope and distibuting the amount to users """
    def __init__(self, id : int,  user : User, amount : int, count : int) -> None:
        self.id = id
        self.user = user
        self.amount = amount
        self.count = count
        #
        self.created = time.time()
        self.distro = []
        self.grabers : list[Graber] = []
        self.distribute()
    
    def __eq__(self, __o: object) -> bool:
        return self.id == __o
    
    def distribute(self):
        # distribute the all amount randomly to count of users
        for i in range(self.count):
            # the last per gets all the leftover
            if i == self.count - 1 :
                n = self.amount - sum(self.distro)
            else:
                # a random number
                n = randint(1, self.amount - sum(self.distro))
            # add to list
            self.distro.append(n)

def make_hyper_title(player : Player, setting : Settings):
    # the user's title if exists or default title
    if player.user.title:
        title = player.user.title
    else:
        title = setting.data.title
    # make hyper link
    hyper = f"[{title}]({setting.data.link})"
    return hyper
