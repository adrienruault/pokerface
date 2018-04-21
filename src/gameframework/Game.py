

from .Dealer import Dealer
from .Board import Board
from .Hand import Hand
from .Player import Player
from .Error import *
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

        nb_players = len(players_id_list)
        for i in range(nb_players):
            current_player = self.get_player_from_id(players_id_list[i])
            next_player = self.get_player_from_id(players_id_list[(i+1) % nb_players])
            prev_player = self.get_player_from_id(players_id_list[i-1])

            current_player.playing_flag = True
            current_player.next_player = next_player
            current_player.prev_player = prev_player

        # Attributes
        self.__playing_order = players_id_list
        self.__dealer =  Dealer([])
        self.__board = Board(self.__dealer)
        self.__state = "start"
        self.__small_blind = 1.
        self.__big_blind = 2 * self.__small_blind
        self.__small_blind_player_id = players_id_list[0]
        self.__big_blind_player_id = self.get_player_from_id(self.__small_blind_player_id).next_player.id
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

    @property
    def pot(self):
        return self.__pot


    def get_player_from_id(self, player_id):
        return self.__players_dict[player_id]


    def transfer_money(self, player_id, amount):
        """
        Transfer money from a player to the games's pot.
        If amount is positive then the player's wallet is decreased by the specified amount
        and the game's pot is credited with the same amount.
        Otherwise the money is transfered the other way round.
        For example game.transfer_money(1, 10) transfer 10 from game's pot
        to player's wallet with id 1.
        And game.transfer_money(2, -20) transfer 20 from player's wallet with id 2
        to game's pot.

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
        if amount > self.__pot:
            raise MoneyError("Trying to distribute more than there is in the pot")

        player = self.__players_dict[player_id]

        player.change_wallet(amount)
        self.__pot -= amount


    def bet_round(self):
        tmp_playing_order = copy.deepcopy(self.__playing_order)
        # first_round
        for player_id in tmp_playing_order:
            player = self.get_player_from_id(player_id)
            action = player.next_action

            if action == 'fold':
                pass





    def collect_blinds(self):
        if self.__state != "start":
            raise PokerError("Trying to get blinds in a game that is not in start state")

        self.transfer_money(self.__small_blind_player_id, (-1) * self.__small_blind)
        self.transfer_money(self.__big_blind_player_id, (-1) * self.__big_blind)

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
