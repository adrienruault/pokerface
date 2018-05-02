

from .Dealer import Dealer
from .Board import Board
from .Hand import Hand
from .Player import Player
from .Error import *
from .Referee import Referee
import copy

class Game:

    def __init__(self, players_list):
        if len(players_list) < 2:
            raise PokerError("Trying to instantiate a Game object with less than 2 players")

        players_id_list = []
        self.__players_dict = {}

        for player in players_list:
            current_id = player.id

            if current_id in players_id_list:
                raise PokerError("Trying to instantiate a Game object with two players having the same id")

            # Adding players to the dictionary
            new_player = copy.deepcopy(player)
            self.__players_dict[current_id] = new_player
            players_id_list += [current_id]


        # Creating the doubly linked list defining the playing order of the players
        nb_players = len(players_id_list)
        self.__nb_players_in_game = nb_players
        for i in range(nb_players):
            current_player = self.get_player_from_id(players_id_list[i])
            next_player = self.get_player_from_id(players_id_list[(i+1) % nb_players])
            prev_player = self.get_player_from_id(players_id_list[i-1])

            current_player.playing_flag = True
            current_player.next_player = next_player
            current_player.prev_player = prev_player

        # Attributes
        self.__dealer =  Dealer([])
        self.__board = Board(self.__dealer)
        self.__state = "start"
        self.__small_blind = 1.
        self.__big_blind = 2 * self.__small_blind
        self.__small_blind_player_id = players_id_list[0]
        self.__big_blind_player_id = self.get_player_from_id(self.__small_blind_player_id).next_player.id
        self.__controlling_player_id = self.__big_blind_player_id
        self.__pot = 0.
        self.__target_bet = 0.

    @property
    def dealer(self):
        return self.__dealer

    @property
    def players_dict(self):
        return copy.deepcopy(self.__players_dict)

    @property
    def board(self):
        return self.__board

    @property
    def state(self):
        return self.__state

    @property
    def small_blind(self):
        return self.__small_blind

    @property
    def big_blind(self):
        return self.__big_blind

    @property
    def pot(self):
        return self.__pot

    @property
    def target_bet(self):
        return self.__target_bet

    @property
    def winner_ids(self):
        return self.__winner_ids


    def get_player_from_id(self, player_id):
        return self.__players_dict[player_id]



    def bet_round(self):

        # first_r
        first_player = self.get_player_from_id(self.__controlling_player_id)
        controlling_player = first_player

        next_action = controlling_player.ask_action(self)

        # The very first player of the round can only check or raise
        if next_action == "raise":
            self.__target_bet += self.small_blind
            first_player.current_bet = self.__target_bet
        elif next_action == "fold":
            first_player.playing_flag = False
            self.__nb_players_in_game -= 1
            controlling_player = first_player.next_player
            if self.__nb_players_in_game < 2:
                self.__winner_ids = [controlling_player.id]
                self.__update_pot()
                self.terminate()

        elif next_action == "check" or next_action == "call":
            pass
        else:
            raise PokerError("None of the allowed actions has been identified for a Player object in a bet round.")

        # If the next players are not playing anymore then go to next Player
        current_player = first_player.next_player
        while current_player.playing_flag == False:
            current_player = current_player.next_player

        while current_player != controlling_player:
            next_action = current_player.ask_action(self)

            if next_action == "check":
                if self.__target_bet > current_player.current_bet:
                    raise PokerError("Player is checking whereas it should call or raise")

            elif next_action == "fold":
                current_player.playing_flag = False
                self.__nb_players_in_game -= 1

                if self.__nb_players_in_game < 2:
                    self.__winner_ids = [controlling_player.id]
                    self.__update_pot()
                    self.terminate()

            elif next_action == "call":
                current_player.current_bet = self.__target_bet

            elif next_action == "raise":
                self.__target_bet += self.small_blind
                current_player.current_bet = self.__target_bet
                controlling_player = current_player
            else:
                raise PokerError("None of the allowed actions has been identified for a Player object in a bet round.")

            # If the next players are not playing anymore then go to next Player
            current_player = current_player.next_player
            while current_player.playing_flag == False:
                current_player = current_player.next_player

        # updating controlling player id
        self.__controlling_player_id = controlling_player.id

        self.__update_pot()

        if self.__nb_players_in_game < 2:
            self.__winner_ids = [self.__controlling_player_id]
            self.terminate()





    def __update_pot(self):
        """
        Finishing the betting round by transferring player's bets to the pot
        and by updating their wallet.
        """

        # Adding bet of first Player
        first_player = self.get_player_from_id(self.__controlling_player_id)
        bet_sum = 0
        bet_sum += first_player.current_bet
        first_player.wallet -= first_player.current_bet
        first_player.current_bet = 0

        current_player = first_player.next_player

        while current_player != first_player:
            bet_sum += current_player.current_bet
            current_player.wallet -= current_player.current_bet
            current_player.current_bet = 0
            current_player = current_player.next_player

            #if current_player.playing_flag == True:
            #    nb_players_in_game += 1
        self.__pot += bet_sum






    def collect_blinds(self):
        if self.__state != "start":
            raise PokerError("Trying to get blinds in a game that is not in start state")

        self.get_player_from_id(self.__small_blind_player_id).wallet -= self.__small_blind
        self.get_player_from_id(self.__big_blind_player_id).wallet -= self.__big_blind

        self.__pot += self.__small_blind + self.__big_blind

        self.__state = "blinds-collected"



    def distribute_hands(self):
        if self.__state != "blinds-collected":
            raise PokerError("Trying to get blinds in a game that is not in blinds-collected state")

        for _, player in self.__players_dict.items():
            hand = Hand(self.__dealer)
            hand.receive_cards()
            player.receive_hand(hand)

        self.bet_round()

        if self.__state != "finished":
            self.__state = "pre-flop"


    def flop(self):
        if self.__state == "finished":
            return
        if self.__state != "pre-flop":
            raise PokerError("Trying to distribute flop in a game that is not in pre-flop state")

        self.__board.flop()

        self.bet_round()

        if self.__state != "finished":
            self.__state = "pre-turn"


    def turn(self):
        if self.__state == "finished":
            return
        if self.__state != "pre-turn":
            raise PokerError("Trying to distribute turn in a game that is not in pre-turn state")

        self.__board.turn()

        self.bet_round()

        if self.__state != "finished":
            self.__state = "pre-river"


    def river(self):
        if self.__state == "finished":
            return
        if self.__state != "pre-river":
            raise PokerError("Trying to distribute river in a game that is not in pre-river state")

        self.__board.river()

        self.bet_round()

        if self.__state != "finished":
            referee = Referee(self.__players_dict, self.__board)
            self.__winner_ids = referee.winner_ids
            self.terminate()


    def terminate(self):

        # Distribute pot to winners
        award = self.__pot / len(self.__winner_ids)
        for winner_id in self.__winner_ids:
            player = self.get_player_from_id(winner_id)
            player.wallet += award
        self.__pot = 0.

        self.__state = "finished"


    def restart(self):
        # Reset board and dealer
        self.__dealer.reset()
        self.__board.reset()

        self.__nb_players_in_game = len(self.__players_dict)
        self.__small_blind_player_id = self.get_player_from_id(self.__small_blind_player_id).next_player.id
        self.__big_blind_player_id = self.get_player_from_id(self.__small_blind_player_id).next_player.id
        self.__controlling_player_id = self.__big_blind_player_id
        self.__target_bet = 0.
        self.__state = "start"

        # updating playing_flag of each player to make it True
        for _, player in self.__players_dict.items():
            player.playing_flag = True





    def __repr__(self):
        to_print = "state: " + str(self.__state) + "\n"
        to_print += "current pot: " + str(self.__pot) + "\n"
        to_print += "board: " + self.__board.__repr__() + "\n"

        for _, player in self.__players_dict.items():
            to_print += player.__repr__() + "\n"

        return to_print
