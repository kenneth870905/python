from random import choice, shuffle
from models import *
import texts

class Animal:
    def __init__(self, odds : tuple, probability : int) -> None:
        self.normal_odd = odds[0]
        self.crit_odd = odds[1]
        self.probability = probability
    
    def __eq__(self, __o: object) -> bool:
        return type(self) == __o
    
    def __add__(self, other):
        return self.probability + other
    
    def __radd__(self, other):
        if other == 0:
            return self
        else:
            return self.__add__(other)
        
    def __str__(self) -> str:
        return self.symbol
    
class Animals:
    class Panda(Animal):
        def __str__(self) -> str:
            return texts.ForestBall.emojis['panda']
    class Lion(Animal):
        def __str__(self) -> str:
            return texts.ForestBall.emojis['lion']
    class Tiger(Animal):
        def __str__(self) -> str:
            return texts.ForestBall.emojis['tiger']
    class Cheetah(Animal):
        def __str__(self) -> str:
            return texts.ForestBall.emojis['cheetah']
    class BrownBear(Animal):
        def __str__(self) -> str:
            return texts.ForestBall.emojis['brown-bear']
    class GrayWolf(Animal):
        def __str__(self) -> str:
            return texts.ForestBall.emojis['gray-wolf']
    class Giraffe(Animal):
        def __str__(self) -> str:
            return texts.ForestBall.emojis['giraffe']
    class WildDog(Animal):
        def __str__(self) -> str:
            return texts.ForestBall.emojis['wild-dog']

class Player(Player):
    def __init__(self, user: User = None) -> None:
        super().__init__(user)
        self.select_times = 0
        self.selects : list[Animal] = []
        self.status = Status.Selecting()

class Dealer(Player):
    def __init__(self, user: User = None) -> None:
        super().__init__(user)
        self.select : Animal = None


class Odd:
    def __init__(self, times : int = 0) -> None:
        self.times = times
    def __eq__(self, __o: object) -> bool:
        return type(self) == __o

class Odds:
    class Normal(Odd):
        def __str__(self) -> str:
            return f"{self.times}"
    class Crit(Odd):
        def __str__(self) -> str:
            return f"(x2) {self.times}"

def odds_probability(prob : int):
    """ give a random item between Normal and Crit. probabilty of `Crit` is `prob` parameter (0, 100)"""
    if not (0 <= prob <= 100):
        raise KeyError("the probabilty must an number between 0 and 100")
    choices = []
    # add items to choices, count of al element is 100
    choices.extend(prob * [Odds.Crit()])
    choices.extend((100-prob) * [Odds.Normal()])
    # select an random item
    shuffle(choices)
    return choice(choices)

class ForestBallGame(Game):
    name = texts.ForestBall.name
    texts_source = texts.ForestBall
    
    def __init__(self, game_id: int, database: Database) -> None:
        super().__init__(game_id, database)
        self.players : list[Player] = []
        self.dealer = Dealer()
        self.elements : list[Animal] = [
            Animals.Panda(odds=(50, 100), probability=3),
            Animals.Lion(odds=(25, 50), probability=5),
            Animals.Tiger(odds=(20, 40), probability=8),
            Animals.Cheetah(odds=(15, 30), probability=10),
            Animals.BrownBear(odds=(10, 20), probability=12),
            Animals.GrayWolf(odds=(5, 10), probability=15),
            Animals.Giraffe(odds=(3, 6), probability=20),
            Animals.WildDog(odds=(2, 5), probability=27),
        ]
        self.odd : Odd = odds_probability(15)
    
    def add_bet(self, user: User, rate: int):
        self.last_update = time.time()
        # make player object
        if user.id in self.players:
            player = self.get_player(user.id)
            # check bet times
            if player.bet_times >= 5 :
                raise errors.AddBetLimit()
        else:
            player = Player(user)
        # add new bet amount
        player.user = self.database.get_user(player.user.id)
        new_bet = int(player.user.balance * (rate / 100))
        if new_bet < 1:
            raise errors.BalanceNotEnough()
        # add new user if not exists 
        if not player.id in self.players:
            self.players.append(player)
        # add new bet amount 
        player.bet_amount += new_bet
        player.bet_times += 1
        self.total += new_bet
        # commit in database
        player.user = self.database.add_balance(player.user, - new_bet)
        return player.bet_amount
    
    def play(self):
        # dealer playing
        self.dealer.select = choice(self.elements)
        # check odd type
        if type(self.odd) == Odds.Normal:
            self.odd.times = self.dealer.select.normal_odd
        elif type(self.odd) == Odds.Crit:
            self.odd.times = self.dealer.select.crit_odd
    
    
    def make_select(self, player : Player, user_select : Animal) :
        if type(player) == int:
            player = self.get_player(player)
        # check select times
        if player.select_times >= 8:
            raise errors.SelectLimit()
        # make select
        for element in self.elements:
            # select from selects
            if type(element) == user_select:
                # can't select duplicate element
                if element in player.selects:
                    raise errors.SelectDuplicate()
                # new select
                player.selects.append(element)
            
        # add new select
        player.select_times += 1
        player.status = Status.Selected()
        self.last_update = time.time()
        #
        return player
    
    
    def game_selecting(self):
        for player in self.players:
            if type(player.status) == Status.Selecting:
                return True
        return False
    
    def settle(self):
        #check players status and game time
        if time.time() - self.last_update < 30:
            if self.game_playing():
                raise errors.PlayersArePlaying()
            elif (time.time() - self.last_update < 6) :
                raise errors.WaitTimeSelect()
        #check game status
        if type(self.status) == GameStatus.Clsoed:
            raise errors.GameIsClosed()
        # make game close 
        self.status = GameStatus.Clsoed()
        # find winners
        for player in self.players:
            # return the timeout players
            if not player.selects:
                player.status = Status.TimeOut()
                continue
            # who player will wins that he has the dealer's selected element 
            if self.dealer.select in player.selects:
                player.status = Status.Win()
                self.winners.append(player)
            else :
                player.status = Status.Lose()
        
        # save the history
        self.history = ForestHistory(self.dealer.select)
            
        # settle the moneys
        for player in self.players :
            # winner player profit
            if type(player.status) == Status.Win:
                # calculate profit by selected cards
                # profir formula : bet amount / player selects count * element odd
                # calculate profit
                profit = player.bet_amount / len(player.selects) * self.odd.times
                player.profit = int(profit)
                # when user is a winner, just get profit without bet amount
                player.bet_amount = 0
                # commit and change user balance
                player.user = self.database.add_balance(player.user, player.profit)
                return
            # loser player loses one times bet amount
            elif type(player.status) == Status.Lose:
                player.profit = - player.bet_amount
            # user that timeout must get back her money
            elif type(player.status) in (Status.Draw, Status.TimeOut):
                player.profit = 0
            # commit and change user balance
            player.user = self.database.add_balance(player.user, player.bet_amount + player.profit)
        
    
    async def update_stats(self, event, history, settle=False):
        # formatting history
        history = list(filter(lambda x: type(x) == ForestHistory, history))
        history_records = " ".join(map(str, history))
    
        # displaying game data stats
        def user_stats_settle(player : Player):
             return self.texts_source.user_settle_stats.format(
                 name=player.user.name,
                 status=player.status,
                 reward=format_amount(player),
                 )
        
        if settle:
            # settle game
            player_list = "\n".join(map(user_stats_settle, self.players))
            buttons = texts.buttons_end_game
            t = self.texts_source.game_settle_stats.format(
                dealer=self.dealer.select,
                odd=self.odd,
                player_list=player_list,
                len_his=len(history),
                history=history_records,
                )
        else:
            # when game is playing, players list won't display
            buttons = self.texts_source.buttons_control_game
            t = self.texts_source.game_started_stats.format(
                len_his=len(history),
                history=history_records,
                )
        
            # send game stats
        game_m = await event.edit(t, link_preview=False, buttons=buttons)
        
        # send message notif to winners
        if settle and self.winners:
            winners_list = map(lambda p: texts.winner_prize_stats.format(
                name=p.user.name,
                reward=separator(p.profit + p.bet_amount)
                ), self.winners)
            winners_list = "\n".join(winners_list)
            # winners
            await game_m.reply(texts.winner_prize.format(winners_list=winners_list), link_preview=False)



class ForestHistory(History):
    def __init__(self, dealer_select : Animal) -> None:
        self.select = dealer_select
        
    def __str__(self) -> str:
        return str(self.select)