

from .CardPack import CardPack
from .Board import Board
from .Hand import Hand
from .Player import Player
from .Error import *
from .Referee import Referee
import copy

class Dealer():

    def __init__(self, players_list):

        if len(players_list) < 2:
            raise PokerError("Trying to instantiate a Dealer object with less than 2 players")

        players_id_list = []
        self.__players_dict = {}

        for player in players_list:
            current_id = player.id

            if current_id in players_id_list:
                raise PokerError("Trying to instantiate a Dealer object with two players having the same id")

            # Adding players to the dictionary
            new_player = copy.deepcopy(player)
            self.__players_dict[current_id] = new_player
            players_id_list += [current_id]


        # updating playing_flag of each player to make it True
        for _, player in self.__players_dict.items():
            player.playing_flag = True


        # Creating the doubly linked list defining the playing order of the players
        nb_players = len(players_id_list)
        for i in range(nb_players):
            current_player = self.get_player_from_id(players_id_list[i])
            next_player = self.get_player_from_id(players_id_list[(i+1) % nb_players])
            prev_player = self.get_player_from_id(players_id_list[i-1])

            current_player.playing_flag = True
            current_player.next_player = next_player
            current_player.prev_player = prev_player

        # Attributes
        self.__card_pack =  CardPack([])
        self.__board = Board(self.__card_pack)
        self.__state = "start"
        self.__bet_round_done = False



    @property
    def card_pack(self):
        return self.__card_pack

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
    def bet_round_done(self):
        return self.__bet_round_done




    def get_player_from_id(self, player_id):
        return self.__players_dict[player_id]

    def get_nb_players(self):
        return len(self.__players_dict)


    def distribute_hands(self):
        if self.__state != "start":
            raise PokerError("Trying to get blinds in a dealer that is not in blinds-collected state")

        for _, player in self.__players_dict.items():
            hand = Hand(self.__card_pack)
            hand.receive_cards()
            player.receive_hand(hand)

        self.__state = "pre-flop"

        # Updating bet_round_done to False in order to allow betting round to occur
        self.__bet_round_done = False


    def flop(self):
        if self.__state == "finished":
            return
        if self.__state != "pre-flop":
            raise PokerError("Trying to distribute flop with Dealer that is not in pre-flop-collected state")

        self.__board.flop()

        self.__state = "flop"

        # Updating bet_round_done to False in order to allow betting round to occur
        self.__bet_round_done = False


    def turn(self):
        if self.__state == "finished":
            return
        if self.__state != "flop":
            raise PokerError("Trying to distribute turn with Dealer that is not in flop-collected state")

        self.__board.turn()

        self.__state = "turn"

        # Updating bet_round_done to False in order to allow betting round to occur
        self.__bet_round_done = False


    def river(self):
        if self.__state == "finished":
            return
        if self.__state != "turn":
            raise PokerError("Trying to distribute river with Dealer that is not in turn-collected state")

        self.__board.river()

        self.__state = "river"

        # Updating bet_round_done to False in order to allow betting round to occur
        self.__bet_round_done = False



    def reset(self):
        # Reset board, card_pack and player's hand
        self.__card_pack.reset()
        self.__board.reset()
        for _, player in self.__players_dict.items():
            player.hand.reset()

        self.__state = "start"
        # Updating bet_round_done to False in order to allow betting round to occur
        self.__bet_round_done = False
