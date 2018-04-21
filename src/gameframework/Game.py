

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
    def playing_order(self):
        return self.__playing_order

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


    def get_player_from_id(self, player_id):
        return copy.deepcopy(self.__players_dict[player_id])


    def transfer_money(self, player_id, amount):
        """
        Transfer money from a player to the games's pot.
        If amount is positive then the player's wallet is decreased by the specified amount
        and the game's pot is credited with the same amount.
        Otherwise the money is transfered the other way round.
        For example game.transfer_money(1, -10) transfer 10 from player's wallet with id 1
        to the game object.

        Parameters
        ----------
        player_id : int
            Id of the player concerned by the transfer.
        amount : float
            Money to transfer from game to player.

        Returns
        -------
        None

        """

        if not isinstance(player_id, int):
            raise WrongTypeError("Trying to collect money with a player_id that is not an int.")
        if not isinstance(amount, float):
            raise WrongTypeError("Trying to collect money with an amount of money that is not a float.")

        player = self.__players_dict[player_id]

        player.change_wallet(amount)
        self.__pot -= amount



    def collect_blinds(self):
        if self.__state != "start":
            raise PokerError("Trying to get blinds in a game that is not in start state")
        small_blind_player_id = self.__playing_order[0]
        big_blind_player_id = self.__playing_order[1]

        self.transfer_money(small_blind_player_id, (-1) * self.__small_blind)
        self.transfer_money(big_blind_player_id, (-1) * self.__big_blind)

        self.__state = "blinds-collected"



    def distribute_hands(self):
        if self.__state != "blinds-collected":
            raise PokerError("Trying to get blinds in a game that is not in blinds-collected state")

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
