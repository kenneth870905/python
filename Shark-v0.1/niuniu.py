from models import *
import texts

class Select:
    def __init__(self, card : Card = None, status : Status = None) -> None:
        self.card = card
        self.status = status

class Selects:
    class QingLong(Select):
        def __str__(self) -> str:
            return "QingLong"
    class WhiteTiger(Select):
        def __str__(self) -> str:
            return "White Tiger"
    class Suzaku(Select):
        def __str__(self) -> str:
            return "Suzaku"
    class Xuanwu(Select):
        def __str__(self) -> str:
            return "Xuanwu"
    
class Player(Player):
    def __init__(self, user: User = None) -> None:
        super().__init__(user)
        self.select : Select = None
        self.card : Card = None
        self.select_times = 0
        self.status = Status.Selecting()

class Dealer(Player):
    pass


class NiuNiuGame(Game):
    name = texts.NiuNiu.name
    texts_source = texts.NiuNiu
    
    def __init__(self, game_id: int, database: Database) -> None:
        super().__init__(game_id, database)
        self.deck = Deck(True)
        self.deck.cards = [
            Card(0, 'No Cow'),
            Card(1, 'Niu Yi'),
            Card(2, 'Niu Er'),
            Card(3, 'Niu San'),
            Card(4, 'Niu Si'),
            Card(5, 'Niu Wu'),
            Card(6, 'Niu Liu'),
            Card(7, 'Niu Qi'),
            Card(8, 'Niu Ba'),
            Card(9, 'Niu Jiu'),
            Card(10, 'Niu Niu'),
        ]
        self.history : NiuNIuHistory = None
        self.dealer = Dealer()
        self.players : list[Player] = []
        self.selects : list[Select] = [
            Selects.QingLong(self.deck.choose_random_card()),
            Selects.WhiteTiger(self.deck.choose_random_card()),
            Selects.Suzaku(self.deck.choose_random_card()),
            Selects.Xuanwu(self.deck.choose_random_card()),
            ]
    
    def play(self):
        # play dealer
        self.dealer.card = self.deck.choose_random_card()
        self.last_update = time.time()
    
    def make_select(self, player : Player, user_select : Select) :
        if type(player) == int:
            player = self.get_player(player)
        # check select times
        if player.select_times >= 3:
            raise errors.SelectLimit()
        # make select
        for select in self.selects:
            # select from selects
            if type(select) == user_select:
                player.select = select
                player.card = player.select.card
            
        # add new select
        player.select_times += 1
        player.status = Status.Selected()
        self.last_update = time.time()
        #
        return True
            
    
    def game_selecting(self):
        for player in self.players:
            if type(player.status) == Status.Selecting:
                return True
        return False
    
    
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
        # settle the game
        for player in self.players:
            # return the timeout players
            if not player.card:
                player.status = Status.TimeOut()
                continue
            # player wins
            if player.card.value > self.dealer.card.value:
                self.winners.append(player)
                player.status = Status.Win()
                self.dealer.status = Status.Lose()
            # player lose
            elif player.card.value < self.dealer.card.value:
                player.status = Status.Lose()
                self.dealer.status = Status.Win()
            # player draw
            else :
                player.status = Status.Draw()
                self.dealer.status = Status.Draw()
        
        # settle the selects (for history)
        for select in self.selects:
            # select loses
            if select.card.value < self.dealer.card.value :
                select.status = Status.Lose()
            # select wins
            elif select.card.value > self.dealer.card.value :
                select.status = Status.Win()
            # select draws
            else :
                select.status = Status.Draw()
            
        # add history
        self.history = NiuNIuHistory(*self.selects)
        
        # settle the moneys
        for player in self.players :
            # winnerplayer gets one times bet amount as profit
            if type(player.status) == Status.Win:
                # the profit is different with each card
                if player.card.value in (7, 8, 9):
                    profit_times = 2
                elif player.card.value == 10:
                    profit_times = 3
                else :
                    profit_times = 1
                player.profit = profit_times * player.bet_amount
            # loser player loses one times bet amount as profit
            elif type(player.status) == Status.Lose:
                player.profit = - player.bet_amount
            # drawerr player don't gets anythings as profit
            elif type(player.status) in (Status.Draw, Status.TimeOut):
                player.profit = 0
            # commit and change user balance
            player.user = self.database.add_balance(player.user, player.bet_amount + player.profit)
    
            
    async def update_stats(self, event, history, settle=False, buttons=texts_source.buttons_control_game):
        # formatting history
        def format_history_status(status):
            if type(status) == Status.Win:
                a = "●"
            elif type(status) == Status.Lose:
                a = "○"
            elif type(status) == Status.Draw:
                a = "◎"
            return a
                
        history = list(filter(lambda x: type(x) == NiuNIuHistory, history))
        
        history_records = ""
        _history = {
            Selects.QingLong() : map(lambda select : format_history_status(select.qinglong.status),  history),
            Selects.WhiteTiger() : map(lambda select : format_history_status(select.white_tiger.status),  history),
            Selects.Suzaku() : map(lambda select : format_history_status(select.suzaku.status),  history),
            Selects.Xuanwu() : map(lambda select : format_history_status(select.xuanwu.status),  history),
        }
        for record in _history:
            history_records += f"{record} : {' '.join(_history[record])}\n"
        
        
    
        def user_stats_settle(player : Player):
             return texts.NiuNiu.user_settle_stats.format(name=player.user.name, choice=player.select, status=player.status, amount=format_amount(player))
        
        def user_stats(p : Player):
            return texts.NiuNiu.user_game_stats.format(name=p.user.name, status=p.status, choice=p.select)
        
        # settle status or normal
        if settle:
            choices = []
            choices.append(self.dealer.card.symbol)
            choices.extend((select.card.symbol for select in self.selects))
            player_list = "\n".join(map(user_stats_settle, self.players))
            t = texts.NiuNiu.game_settle_stats.format(*choices, player_list=player_list, history=history_records, len_his=len(history))
            buttons = texts.buttons_end_game
        else:
            player_list = "\n".join(map(user_stats, self.players))
            t = texts.NiuNiu.game_started_stats.format(player_list=player_list, history=history_records, len_his=len(history))

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


class NiuNIuHistory(History):
    def __init__(self, qinglong : Selects.QingLong, white_tiger : Selects.WhiteTiger, suzaku : Selects.Suzaku, xuanwu : Selects.Xuanwu) -> None:
        self.qinglong = qinglong
        self.white_tiger = white_tiger
        self.suzaku = suzaku
        self.xuanwu = xuanwu
        