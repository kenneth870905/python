from random import shuffle
from models import *
import texts
from roulette import Dice, Player

class Place(Dice):
    def __str__(self) -> str:
        s = str(self.value)
        if self.value == 1:
            s = "first place"
        elif self.value == 2:
            s = "2nd place"
        elif self.value == 3:
            s = "3nd place"
        elif self.value == 4:
            s = "fourth place"
        elif self.value == 5:
            s = "fifth place"
        elif self.value == 6:
            s = "six place"
        elif self.value == 7:
            s = "seven place"
        elif self.value == 8:
            s = "eight place"
        elif self.value == 9:
            s = "nine place"
        elif self.value == 10:
            s = "ten place"
        return s

class Player(Player):
    def __init__(self, user: User = None) -> None:
        super().__init__(user)
        self.place : Place = None
        self.selects : list[Dice] = []
        self.select_times = 0

class Dealer(Player):
    pass

class LuckyHistory(History):
    def __init__(self, dealer_select : list[Dice]) -> None:
        self.select = dealer_select
    
    def __str__(self) -> str:
        return " ".join(map(str, self.select))

class LuckyAirsihpGame(Game):
    texts_source = texts.LuckyAirship
    name = texts_source.name
    history_object = LuckyHistory
    
    def __init__(self, game_id: int, database: Database) -> None:
        super().__init__(game_id, database)
        self.players : list[Player] = []
        self.dealer = Dealer()
        
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
        # dealer selects 10 shuffeled numbers 
        self.dealer.selects = [Dice(i) for i in range(1, 10+1)]
        shuffle(self.dealer.selects)
    
    def make_select(self, player : Player, user_select : Dice) :
        if type(player) == int:
            player = self.get_player(player)
        # check the type of user's select
        if type(user_select) == Place:
            # check select times
            if player.select_times >= 3:
                raise errors.PlaceLimit()
            # make a place
            player.place = user_select
            player.select_times += 1
        # select is a dice
        elif type(user_select) == Dice:
            # check place required
            if not player.place:
                raise errors.PlaceRequired()
            # check selects limit
            if len(player.selects) >= 7:
                raise errors.SelectLimit()
            # check duplicate item
            if user_select in player.selects:
                raise errors.SelectDuplicate()
            player.selects.append(user_select)
        # add new select
        self.last_update = time.time()
        if player.place and player.selects:
            player.status = Status.Selected()
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
        self.history = self.history_object(self.dealer.selects)
        # find winners
        for player in self.players:
            # return the timeout players
            if type(player.status) == Status.Selecting:
                player.status = Status.TimeOut()
                continue
            # who player will wins that he detect correctly numbrt in correct place
            # index
            if self.dealer.selects[player.place.value - 1] in player.selects:
                player.status = Status.Win()
                self.winners.append(player)
            else :
                player.status = Status.Lose()
            
        # settle the moneys
        for player in self.players :
            # winner player profit
            if type(player.status) == Status.Win:
                player.profit = player.bet_amount / len(player.selects) * 10
                player.profit = int(player.profit)
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
        history = list(filter(lambda x: type(x) == self.history_object, history))
        history_records = "\n".join(map(str, history))
    
        # displaying game data stats
        def user_stats_settle(player : Player):
             return self.texts_source.user_settle_stats.format(
                 name=player.user.name,
                 status=player.status,
                 place=player.place,
                 selects=" ".join(map(str, player.selects)),
                 reward=format_amount(player),
                 )
             
        def user_stats(player : Player):
             return self.texts_source.user_game_stats.format(
                 name=player.user.name,
                 status=player.status,
                 place=player.place,
                 selects=" ".join(map(str, player.selects)),
                 )
        
        if settle:
            # settle game
            buttons = texts.buttons_end_game
            player_list = "\n".join(map(user_stats_settle, self.players))
            t = self.texts_source.game_settle_stats.format(
                dealer=" ".join(map(str, self.dealer.selects)),
                player_list=player_list,
                len_his=len(history),
                history=history_records,
                )
        else:
            # playing game
            buttons = self.texts_source.buttons_control_game
            player_list = "\n".join(map(user_stats, self.players))
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
        