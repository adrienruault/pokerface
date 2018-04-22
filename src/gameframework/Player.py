

from .Error import *
from .Hand import Hand


class Player():

    ACTIONS = ['check', 'fold', 'call', 'raise']

    def __init__(self, id_, wallet):
        if not isinstance(id_, int):
            raise WrongTypeError("The Player id that you provided is not an int.")
        if not isinstance(wallet, float):
            raise WrongTypeError("The Player's wallet that you provided is not a float")

        self.__id = id_
        self.__wallet = wallet
        self.__hand = None
        self.__next_action = None

        self.__next_player = None
        self.__prev_player = None
        self.__playing_flag = None

        self.__current_bet = 0.


    def receive_hand(self, hand):
        self.__hand = hand


    def __eq__(self, other):
        if (type(other) is not Player):
            raise WrongTypeError('Trying to check equality of a Player with an object that is not a Player.')

        return (other.id == self.__id)


    def __repr__(self):
        return "{id: " + str(self.__id) + ' | Hand: ' + self.__hand.__repr__() + "}"

    @property
    def id(self):
        return self.__id

    @property
    def wallet(self):
        return self.__wallet

    @wallet.setter
    def wallet(self, new_wallet):
        if new_wallet < 0:
            raise PokerError("Trying to set a negative player's wallet.")
        self.__wallet = new_wallet

    @property
    def hand(self):
        return self.__hand

    @property
    def next_player(self):
        return self.__next_player

    @next_player.setter
    def next_player(self, new_next_player):
        self.__next_player = new_next_player

    @property
    def prev_player(self):
        return self.__prev_player

    @prev_player.setter
    def prev_player(self, new_prev_player):
        self.__prev_player = new_prev_player


    @property
    def playing_flag(self):
        return self.__playing_flag

    @playing_flag.setter
    def playing_flag(self, new_playing_flag):
        self.__playing_flag = new_playing_flag


    @property
    def next_action(self):
        return self.__next_action

    @next_action.setter
    def next_action(self, new_action):
        if new_action not in self.ACTIONS:
            raise PokerError("Trying to assign an action to a Player object that is not allowed ")
        self.__next_action = new_action


    @property
    def current_bet(self):
        return self.__current_bet

    @current_bet.setter
    def current_bet(self, new_current_bet):
        if new_current_bet > self.__wallet:
            raise MoneyError("Player trying to bet more than what it has.")
        if new_current_bet < 0:
            raise MoneyError("Trying to bet with negative values")

        self.__current_bet = new_current_bet
