from random import choice
from models import *
import texts

class Dice:
    pass

class Player(Player):
    def __init__(self, user: User = None) -> None:
        super().__init__(user)
        self.select_times = 0
        self.select : Dice = None
        self.status = Status.Selecting()

class Dealer(Player):
    pass

class Dice:
    def __init__(self, value : int) -> None:
        self.value = value
    
    def __eq__(self, __o: object) -> bool:
        return self.value == __o
    
    def __str__(self) -> str:
        return str(self.value)

class MultiDice:
    def __init__(self, value: tuple, name : str) -> None:
        self.value = value
        self.name = name
    
    def __str__(self) -> str:
        return self.name

class DiceRandom:
    class Large(MultiDice):
        def __init__(self) -> None:
            super().__init__((4, 5, 6), "Large")
        
    class Small(MultiDice):
        def __init__(self) -> None:
            super().__init__((1, 2, 3), "Small")
            
    class Single(MultiDice):
        def __init__(self) -> None:
            super().__init__((1, 3, 5), "Single")
            
    class Double(MultiDice):
        def __init__(self) -> None:
            super().__init__((2, 4, 6), "Double")


class RouletteHistory(History):
    def __init__(self, dealer_select : Dice) -> None:
        self.select = dealer_select
    
    def __str__(self) -> str:
        return str(self.select)

class RouletteGame(Game):
    name = texts.Roulette.name
    texts_source = texts.Roulette
    history_object = RouletteHistory
    
    def __init__(self, game_id: int, database: Database) -> None:
        super().__init__(game_id, database)
        self.players : list[Player] = []
        self.dealer : Dealer = Dealer()
        self.selects : list[Dice] = (
            Dice(1),
            Dice(2),
            Dice(3),
            Dice(4),
            Dice(5),
            Dice(6),
        )
        
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
        # select dealer
        self.dealer.select = choice(self.selects)
    
    def make_select(self, player : Player, user_select : Dice) :
        if type(player) == int:
            player = self.get_player(player)
        # check select times
        if player.select_times >= 3:
            raise errors.SelectLimit()
        # add new select
        player.select = user_select
        player.select_times += 1
        player.status = Status.Selected()
        self.last_update = time.time()
        #
        return player
    
    
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
        # save the history
        self.history = self.history_object(self.dealer.select)
        # find winners
        for player in self.players:
            # return the timeout players
            if type(player.status) == Status.Selecting:
                player.status = Status.TimeOut()
                continue
            # who player will wins that he has the dealer's selected 
            if (self.dealer.select == player.select) or (type(player.select) != Dice and self.dealer.select in player.select.value):
                player.status = Status.Win()
                self.winners.append(player)
            else :
                player.status = Status.Lose()
            
        # settle the moneys
        for player in self.players :
            # winner player profit
            if type(player.status) == Status.Win:
                # if selects selects a number object gets 6 times reward
                if type(player.select) == Dice:
                    player.profit = 5 * player.bet_amount
                else:
                    # selects an item between large, small, ... 
                    player.profit = player.bet_amount
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
        history = list(filter(lambda x: type(x) == self.history_object, history))
        history_records = " ".join(map(str, history))
    
        # displaying game data stats
        def user_stats_settle(player : Player):
             return self.texts_source.user_settle_stats.format(
                 name=player.user.name,
                 status=player.status,
                 select=player.select,
                 reward=format_amount(player),
                 )
             
        def user_stats(player : Player):
            return self.texts_source.user_game_stats.format(
                 name=player.user.name,
                 status=player.status,
                 select=player.select,
                 )
        
        if settle:
            print(4)
            # settle game
            buttons = texts.buttons_end_game
            player_list = "\n".join(map(user_stats_settle, self.players))
            t = self.texts_source.game_settle_stats.format(
                dealer=self.dealer.select,
                player_list=player_list,
                len_his=len(history),
                history=history_records,
                )
        else:
            print(5)
            # playing game
            buttons = self.texts_source.buttons_control_game
            player_list = "\n".join(map(user_stats, self.players))
            print(player_list)
            t = self.texts_source.game_started_stats.format(
                player_list=player_list,
                len_his=len(history),
                history=history_records,
                )
        
        # send game stats
        game_m = await event.edit(t, link_preview=False, buttons=buttons)
        
        # send message notif to winners
        if settle and self.winners:
            # clear winners list
            winners_list = self.winners.copy()
            self.winners.clear()
            # send the congrage message to winners
            winners_list = map(lambda p: texts.winner_prize_stats.format(
                name=p.user.name,
                reward=separator(p.profit + p.bet_amount)
                ), winners_list)
            winners_list = "\n".join(winners_list)
            # winners
            await game_m.reply(texts.winner_prize.format(winners_list=winners_list), link_preview=False)