



from .Dealer import Dealer
from .Referee import Referee
from .Error import PokerError




class GameMaster(Dealer):


    allowed_betting_actions = ['pre-flop', 'flop', 'turn', 'river']

    def __init__(self, players_list):
        Dealer.__init__(self, players_list)

        self.__low_stake = 1.
        self.__high_stake = 2 * self.__low_stake
        self.__small_blind = 0.5 * self.__low_stake
        self.__big_blind = self.__low_stake
        self.__target_bet = 0.
        self.__pot = 0.

        # Might ba a good idea in the future to draw the first player randomly
        self.__small_blind_player_id = players_list[0].id
        self.__big_blind_player_id = self.get_player_from_id(self.__small_blind_player_id).next_player.id
        self.__first_player_id = self.get_player_from_id(self.__big_blind_player_id).next_player.id

        # Controlling player id is fully defined in bet_round
        self.__controlling_player_id = None

        self.__nb_players_in = self.get_nb_players()

        self.__referee = Referee()


    @property
    def nb_players_in(self):
        return self.__nb_players_in

    @property
    def pot(self):
        return self.__pot

    @property
    def target_bet(self):
        return self.__target_bet

    @property
    def small_blind(self):
        return self.__small_blind

    @property
    def big_blind(self):
        return self.__big_blind

    @property
    def last_winner_ids(self):
        return self.__last_winner_ids

    @property
    def target_bet(self):
        return self.__target_bet






    def bet_round(self):
        if self.state == "finished":
            return
        if self.bet_round_done is True:
            raise PokerError("Triggering a bet round at an unproper state")

        # nb_rounds is incremented by one each time the first_player plays
        first_round = True

        # If in pre-flop the player controlling the game is the big blind.
        # Otherwise it is the first_player
        if self.state == "pre-flop":
            self.__controlling_player_id = self.__big_blind_player_id
        else:
            # Looking for the first playing player starting from first_player to
            # give it the title of controlling_player
            controlling_player = self.get_player_from_id(self.__first_player_id)
            while controlling_player.playing_flag == False:
                controlling_player = controlling_player.next_player
            self.__controlling_player_id = controlling_player.id


        first_player = self.get_player_from_id(self.__first_player_id)
        while first_player.playing_flag == False:
            first_player = first_player.next_player

        self.__treat_player_action(first_player)
        if self.state == "finished":
            return

        # If the next players are not playing anymore then go to next Player
        current_player = first_player.next_player
        while current_player.playing_flag == False:
            current_player = current_player.next_player

        # A player can speak while it is not the controlling Player
        # or if it is the big blind, in the first round, in pre-flop and the big blind
        # is still controlling
        # Be careful to stop the game in the later case if the big blind is checking
        # or calling on 0
        while ((current_player.id != self.__controlling_player_id)
                or (self.state == "pre-flop"
                    and current_player.id == self.__big_blind_player_id
                    and current_player.id == self.__controlling_player_id
                    and first_round == True)):

            self.__treat_player_action(current_player)

            # Checking that the game hasn't finished while treating a Player's action
            # Indeed if the current Player is folding and there is only one Player
            # left on the board then the game stops
            if self.state == "finished":
                return

            # If we are in the situation where the big bind is controlling the game
            # at the pre-flop and we are in the very first round of play.
            # Then if the big blind calls or check it has to end the betting round.
            if (self.state == "pre-flop"
                and current_player.id == self.__big_blind_player_id
                and current_player.id == self.__controlling_player_id
                and first_round == True
                and (current_player.played_action == "check"
                    or current_player.played_action == "call")):
                break


            # If the next players are not playing anymore then go to next Player
            current_player = current_player.next_player
            if current_player.id == self.__first_player_id:
                first_round = False
            while current_player.playing_flag == False:
                current_player = current_player.next_player
                if current_player.id == self.__first_player_id:
                    first_round = False

        if self.state == "river":
            compet_hands = []
            compet_player_ids = []
            for id_, player in self._Dealer__players_dict.items():
                if player.playing_flag == True:
                    compet_hands += [player.hand]
                    compet_player_ids += [id_]

            winner_keys = self.__referee.arbitrate(compet_hands, self._Dealer__board)

            winner_ids = [compet_player_ids[i] for i in winner_keys]

            self.__last_winner_ids = winner_ids
            self.__terminate_game(winner_ids)
        else:
            # Finish betting round normally
            self.__transfer_bet_to_pot()
            self._Dealer__bet_round_done = True
            #self._Dealer__state += "-collected"



    def __treat_player_action(self, current_player):
        next_action = current_player.ask_action(self)
        if next_action == "check":
            if abs(self.__target_bet - current_player.current_bet) > 1e-3:
                raise UnauthorizedPlayerAction("Player is checking but its current\
                                                bet is not equal to target bet.")

        elif next_action == "fold":

            current_player.playing_flag = False
            self.__nb_players_in -= 1
            if self.__nb_players_in < 2:
                self.__last_winner_ids = self.__controlling_player_id
                self.__terminate_game([self.__last_winner_ids])
                return

            # If first player is folding, a special cas is occuring
            if current_player.id == self.__controlling_player_id:

                # If the controlling player is folding: go backwards in the playing order
                # to choose the first playing player whose gonna receive the title of controller
                new_controller = current_player.prev_player
                while new_controller.playing_flag == False:
                    new_controller = new_controller.prev_player
                self.__controlling_player_id = new_controller.id


        elif next_action == "call":
            # update player's wallet
            current_player.wallet -= (self.__target_bet - current_player.current_bet)
            current_player.current_bet = self.__target_bet


        elif next_action == "raise":
            self.__target_bet += self.__low_stake

            # update player's wallet
            current_player.wallet -= (self.__target_bet - current_player.current_bet)

            current_player.current_bet = self.__target_bet

            # Current player is taking control if raising
            self.__controlling_player_id = current_player.id
        else:
            raise UnauthorizedPlayerAction("None of the allowed actions has been\
                                            identified for a Player object in a bet round.")






    def collect_blinds(self):
        if (self.state != "start" or
            self.state == "start" and self.bet_round_done is True):
            raise PokerError("Unallowed to get blinds at that game stage")

        small_blind_player = self.get_player_from_id(self.__small_blind_player_id)
        big_blind_player = self.get_player_from_id(self.__big_blind_player_id)

        small_blind_player.wallet -= self.__small_blind
        small_blind_player.current_bet += self.__small_blind

        big_blind_player.wallet -= self.__big_blind
        big_blind_player.current_bet += self.__big_blind

        self.__target_bet = self.__big_blind

        #self.__pot += (self.__small_blind + self.__big_blind)

        self._Dealer__bet_round_done = True
        #self._Dealer__state = "blinds-collected"






    def __transfer_bet_to_pot(self):
        """
        Finishing the betting round by transferring player's bets to the pot.
        """
        bet_sum = 0
        for _, player in self._Dealer__players_dict.items():
            bet_sum += player.current_bet
            player.current_bet = 0
        self.__pot += bet_sum
        self.__target_bet = 0




    def __terminate_game(self, winner_ids):
        """
        Distribute the pot to the winners and put GameMaster's state to "finished".

        Returns
        -------
        None
        """
        self.__transfer_bet_to_pot()

        # Distribute pot to winners
        award = self.__pot / len(winner_ids)
        for winner_id in winner_ids:
            player = self.get_player_from_id(winner_id)
            player.wallet += award
        self.__pot = 0.
        self._Dealer__state = "finished"



    def reset(self):
        Dealer.reset(self)

        for _, player in self._Dealer__players_dict.items():
            player.playing_flag = True

        self.__nb_players_in = self.get_nb_players()

        # update blinds position
        self.__small_blind_player_id = self.get_player_from_id(self.__small_blind_player_id).next_player.id
        self.__big_blind_player_id = self.get_player_from_id(self.__small_blind_player_id).next_player.id
        self.__first_player_id = self.get_player_from_id(self.__big_blind_player_id).next_player.id




    def __repr__(self):
        to_print = "=" * 30 + "\n"
        to_print += "state: " + str(self._Dealer__state) + "\n"
        to_print += "current pot: " + str(self.__pot) + "\n"
        to_print += "current target bet: " + str(self.__target_bet) + "\n"
        to_print += "board: " + self._Dealer__board.__repr__() + "\n\n"

        to_print += "players:\n"
        for _, player in self._Dealer__players_dict.items():
            to_print += player.print_without_hand() + "\n"
        to_print += "=" * 30 + "\n"

        return to_print
