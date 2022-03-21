from models import *
import time
import texts

class Player(Player):
    def is_blackjack(self):
        if self.score == 21 and len(self.cards) == 2 :
            return True

class Dealer(Player):
    pass

class BlackjackGame(Game):
    name = texts.Blackjack_21.name
    texts_source = texts.Blackjack_21
    
    def __init__(self, game_id: int, database: Database, setting : Settings) -> None:
        super().__init__(game_id, database, setting)
        self.id = game_id
        self.last_update = time.time()
        self.database = database
        # define affter initialize
        self.total = 0
        self.players: list[Player] = []
        self.deck = Deck()
        self.dealer = Dealer()
        self.winners : list[Player] = []

    def __eq__(self, __o: object) -> bool:
        return self.id == __o
    
    def play(self):
        # dealer bet amount
        self.dealer.bet_amount = self.total
        # dealer hit
        self.dealer_play()
        # get two cards each player
        for player in self.players:
            self.hit_me(player)
            self.hit_me(player)
    
    
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
    
    def hit_me(self, player : Player) -> Player:
        if type(player) == int:
            player = self.get_player(player)
        # check status
        if type(player.status) != Status.Playing :
            return False
        # choose cards
        card = self.deck.choose_random_card()
        player.cards.append(card)
        player.calculate_score()
        # make status
        if player.score > 21 :
            player.status = Status.Lose()
        elif player.score == 21:
            player.status = Status.Win()
        
        if player.is_blackjack():
            player.status = Status.Blackjack()
        
        # save
        self.last_update = time.time()
        return player
    
    def dealer_play(self):
        while self.dealer.score < 17:
            self.hit_me(self.dealer)

    def get_player(self, user_id: int):
        if user_id in self.players:
            return self.players[self.players.index(user_id)]
        else:
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
        # settle the game
        for player in self.players:
            # return the timeout players
            if type(player.status) == Status.Playing:
                player.status = Status.TimeOut()
                continue
            # skip losers
            if type(player.status) == Status.Lose:
                continue
            # compare with dealer
            if (type(self.dealer.status) == Status.Lose) or (player.score > self.dealer.score):
                # player wins
                player.status = Status.Win()
            elif (player.score < self.dealer.score):
                # player loses
                player.status = Status.Lose()
            else :
                # player draws
                player.status = Status.Draw()
        
        
        # settle the bet amounts
        for player in self.players + [self.dealer]:
            # set blackjacks
            if player.is_blackjack():
                player.status = Status.Blackjack()
            
            # skip delaer
            if type(player) == Dealer:
                continue
                        
            #calculate rewards
            player.user = self.database.get_user(player.id)
            if type(player.status) in (Status.Win, Status.Blackjack):
                self.winners.append(player)
                #blackjac has 2 times profit
                if type(player.status) == Status.Blackjack:
                    player.profit = (player.bet_amount) * 2
                else:
                    # winner has 1 times profit
                    player.profit = player.bet_amount
                # add wins
                player.user = self.database.add_win(player.user)
            # draw doesn't have profit
            elif type(player.status) in (Status.Draw, Status.TimeOut):
                player.profit = 0
            # loser has neviagte profit
            elif type(player.status) == Status.Lose:
                player.profit = - player.bet_amount
                
            # commit
            player.user = self.database.add_balance(player.user, player.profit + player.bet_amount)
    
    async def update_stats(self, event, history, settle=False):
    
        def user_stats_settle(player : Player):
            return self.texts_source.user_settle_stats.format(
                title=make_hyper_title(player, self.setting),
                name=player.user.name,
                cards=cards_format(player.cards),
                score=player.score,
                status=player.status,
                amount=format_amount(player)
                )
        def user_stats(player : Player):
            return self.texts_source.user_game_stats.format(
                title=make_hyper_title(player, self.setting),
                name=player.user.name,
                cards=cards_format(player.cards),
                score=player.score,
                status=player.status,
                )
        
        # hidden the cards of dealer
        if settle:
            _dealer = self.texts_source.dealer_settle_stats.format(cards=cards_format(self.dealer.cards), score=self.dealer.score )
            user_stats_func = user_stats_settle
            buttons = texts.buttons_end_game
        else:
            _dealer = cards_format(self.dealer.cards[:1])
            user_stats_func = user_stats
            buttons = self.texts_source.buttons_control_game
        
        player_list = "\n".join(map(user_stats_func, self.players))
        t = self.texts_source.game_started_stats.format(
            dealer=_dealer, player_list=player_list)

        game_m = await event.edit(t, link_preview=False, buttons=buttons)
        
        # send message notif to winners
        if settle and self.winners:
            # clear winners list
            winners_list = self.winners.copy()
            self.winners.clear()
            # send the congrage message to winners
            winners_list = map(lambda player: texts.winner_prize_stats.format(
                name=player.user.name,
                reward=separator(player.profit + player.bet_amount)
                ), winners_list)
            winners_list = "\n".join(winners_list)
            # winners
            await game_m.reply(texts.winner_prize.format(winners_list=winners_list), link_preview=False)