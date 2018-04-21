

from .Dealer import Dealer
from .Board import Board
from .Hand import Hand
from .Player import Player
from .Error import *
import copy

class Game:

    def __init__(self, players_list):
        players_id_list = []
        self.__players_dict = {}

        for player in players_list:
            current_id = player.id
            if current_id in players_id_list:
                raise PokerError("Trying to instantiate a Game object with two players having the same id")
            self.__players_dict[current_id] = copy.deepcopy(player)
            players_id_list += [current_id]

        #self.__players_list = players_list
        self.__playing_order = players_id_list
        self.__dealer =  Dealer([])
        self.__board = Board(self.__dealer)
        self.__state = "start"
        self.__small_blind = 1.
        self.__big_blind = 2 * self.__small_blind
        self.__pot = 0.

    @property
    def dealer(self):
        return self.__dealer

    @property
    def players_dict(self):
        return copy.deepcopy(self.__players_dict)

    @property
    def players_id(self):
        return self.__players_id

    @property
    def board(self):
        return self.__board

    @property
    def state(self):
        return self.__state


    def collect_money(self, player_id, amount):
        player = self.__players_dict[player_id]
        if not isinstance(player, Player):
            raise PokerError("Trying to collect money from an object which is not a player")
        if not isinstance(amount, float):
            raise PokerError("Trying to collect something else than money from a Player")

        player.decrease_wallet(amount)
        self.__pot += amount

    def get_blinds(self):
        small_blind_player = self.__players_dict[self.__playing_order[0]]
        big_blind_player = self.__players_dict[self.__playing_order[1]]

        self.__collect_money(small_blind_player, self.__small_blind)
        self.__collect_money(big_blind_player, self.__big_blind)


    def distribute_hands(self):
        if self.__state != "start":
            raise PokerError("Trying to distribute cards to players in a game that is not in start state")

        for _, player in self.__players_dict.items():
            hand = Hand(self.__dealer)
            hand.receive_cards()
            player.receive_hand(hand)

        self.__state = "pre-flop"

    def flop(self):
        if self.__state != "pre-flop":
            raise PokerError("Trying to distribute flop in a game that is not in pre-flop state")

        self.__board.flop()
        self.__state = "pre-turn"

    def turn(self):
        if self.__state != "pre-turn":
            raise PokerError("Trying to distribute turn in a game that is not in pre-turn state")

        self.__board.turn()
