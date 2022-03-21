
from models import *
import texts
from random import choice, choices
from roulette import Dealer, Dice, Player, RouletteGame, RouletteHistory


class ListcDice:
    selection_list = []
    name = ''
        
    def __str__(self) -> str:
        return self.name

class KuisanDice:
    # layer one
    class Large(ListcDice):
        selection_list = list(range(11, 18+1))
        name = "Large"
        
    class Small(ListcDice):
        selection_list = list(range(3, 10+1))
        name = "Small"
        
    class Single(ListcDice):
        selection_list= list(range(3, 18+1, 2))
        name = "Single"
        
    class Double(ListcDice):
        selection_list = list(range(4, 18+1, 2))
        name = "Double"
        
    # layer two
    class LargeSingle(ListcDice):
        selection_list = list(range(11, 18+1, 2))
        name = "Large Single"
        
    class SmallSingle(ListcDice):
        selection_list = list(range(3, 10+1, 2))
        name = "Small Single"
        
    class LargeDouble(ListcDice):
        selection_list = list(range(12, 18+1, 2))
        name = "Large Double"
            
    class SmallDouble(ListcDice):
        selection_list = list(range(4, 10+1, 2))
        name = "Small Double"

    
    # specially layer
    class Leopard(ListcDice):
        selection_list = [111, 222, 333, 444, 555, 666]
        name = "Leopard"
        
    class Shunzi(ListcDice):
        name = "Shunzi"
        selection_list = []
        # make three digits numbers
        for i in range(1, 5):
                selection_list.append(int(f"{i}{i+1}{i+2}"))
                selection_list.append(int(f"{i}{i+2}{i+1}"))
                selection_list.append(int(f"{i+1}{i}{i+2}"))
                selection_list.append(int(f"{i+1}{i+2}{i}"))
                selection_list.append(int(f"{i+2}{i}{i+1}"))
                selection_list.append(int(f"{i+2}{i+1}{i}"))
        selection_list = list(set(selection_list))
        
    class Pair(ListcDice):
        name = "Pair"
        selection_list = []
        # make three digits numbers
        for i in range(1, 6+1):
            for j in range(1, 6+1):
                selection_list.append(int(f"{i}{j}{j}"))
                selection_list.append(int(f"{j}{i}{j}"))
        selection_list = list(set(selection_list))
            
class KuisanHistory(RouletteHistory):
    pass

class Dealer(Dealer):
    def __init__(self, user: User = None) -> None:
        super().__init__(user)
        self.select_number : int = 0
        self.selects_list : list[int] = []

class KuisanGame(RouletteGame):
    texts_source = texts.Kuisan
    name = texts_source.name
    history_object = KuisanHistory
    
    def __init__(self, game_id: int, database: Database, setting : Settings) -> None:
        super().__init__(game_id, database, setting)
        self.players : list[Player] = []
        self.dealer : Dealer = Dealer()
    
    def play(self):
        # give 3 dice to dealer
        selects = choices(list(range(1, 6+1)), k=3)
        self.dealer.selects_list = selects.copy()
        self.dealer.select_number = int(''.join(map(str, selects)))
        self.dealer.select = Dice(sum(selects))
    
    
    def dice_reward(self, dice : Dice) -> int:
        reward = 0
        # find reward by value
        if dice.value in (4, 17):
            reward = 50
        elif dice.value in (5, 16):
            reward = 30
        elif dice.value in (6, 15):
            reward = 25
        elif dice.value in (7, 14):
            reward = 20
        elif dice.value in (8, 13):
            reward = 15
        elif dice.value in (9, 12):
            reward = 10
        elif dice.value in (10, 11):
            reward = 5
        #
        return reward
    
    def settle(self):
        #check players status and game time
        if time.time() - self.last_update < 30:
            if self.game_playing():
                raise errors.PlayersArePlaying()
            elif (time.time() - self.last_update < 6) :
                raise errors.WaitTimeSelect()
        self.last_update = time.time()
        #check game status
        if type(self.status) == GameStatus.Clsoed:
            return
        # make game close 
        self.status = GameStatus.Clsoed()
        # save the history
        self.history = self.history_object(self.dealer.select)
        # # find winners
        for player in self.players:
            # return the timeout players
            if type(player.status) == Status.Selecting:
                player.status = Status.TimeOut()
                continue
            # who player will wins that he has the dealer's selected 
            if (self.dealer.select == player.select):
                player.status = Status.Win()
                self.winners.append(player)
            # list items
            elif (type(player.select) != Dice and self.dealer.select in player.select.selection_list):
                player.status = Status.Win()
                self.winners.append(player)
            # check specially list
            elif (type(player.select) != Dice and self.dealer.select_number in player.select.selection_list):
                player.status = Status.Win()
                self.winners.append(player)
            else :
                player.status = Status.Lose()
            
        # settle the moneys
        for player in self.players :
            # winner player profit
            if type(player.status) == Status.Win:
                #  NUmbers -> Variable times
                if type(player.select) == Dice:
                    # get reward times by dice value (decrease for adding bet amount)
                    reward_times = self.dice_reward(player.select) - 1
                    player.profit = reward_times * player.bet_amount
                #  leopard -> 200
                elif type(player.select) == KuisanDice.Leopard:
                    player.profit = 199 * player.bet_amount
                # shunzi -> 30
                elif type(player.select) == KuisanDice.Shunzi:
                    player.profit = 29 * player.bet_amount
                # two Pair -> 10
                elif type(player.select) == KuisanDice.Pair:
                    player.profit = 9 * player.bet_amount
                # small multi items (large_single, etc) -> 4
                elif type(player.select) in (KuisanDice.LargeSingle, KuisanDice.SmallSingle, KuisanDice.LargeDouble, KuisanDice.SmallDouble):
                    player.profit = 3 * player.bet_amount
                # big multi items (large, etc) -> 2
                elif type(player.select) in (KuisanDice.Large, KuisanDice.Small, KuisanDice.Single, KuisanDice.Double):
                    player.profit = 1 * player.bet_amount
            # loser player loses one times bet amount
            elif type(player.status) == Status.Lose:
                player.profit = - player.bet_amount
            # user that timeout must get back her money
            elif type(player.status) in (Status.Draw, Status.TimeOut):
                player.profit = 0
            # commit and change user balance
            player.user = self.database.add_balance(player.user, player.bet_amount + player.profit)
        
    async def update_stats(self, event, history, settle=False):
        # make the dealer select custom format 
        if type(self.status) == GameStatus.Clsoed:
            self.dealer.select = "+".join(map(str, self.dealer.selects_list)) + f"={self.dealer.select}"
        # inheritance the update_stat from roulette game
        return await super().update_stats(event, history, settle)