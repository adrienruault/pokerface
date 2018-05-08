

from .Error import *
from .Hand import Hand


class Player():

    ACTIONS = ['check', 'fold', 'call', 'raise']

    def __init__(self, id_, wallet):
        if not isinstance(id_, str):
            raise WrongTypeError("The Player's id must be a string.")
        if not isinstance(wallet, float):
            raise WrongTypeError("The Player's wallet that you provided is not a float")
        if wallet < 0:
            raise PokerError("Trying to create a Player object with negative wallet.")

        self.__id = id_
        self.__wallet = wallet
        self.__hand = None
        self._next_action = None

        self.__next_player = None
        self.__prev_player = None
        self.__playing_flag = None

        self.__current_bet = 0.


    def receive_hand(self, hand):
        if not isinstance(hand, Hand):
            raise WrongTypeError("Trying to give something else than a Hand object to a Player with the receive_hand method")
        self.__hand = hand


    def __eq__(self, other):
        if not isinstance(other, Player):
            raise WrongTypeError('Trying to check equality of a Player with an object that is not a Player.')

        return (other.id == self.__id)


    def __repr__(self):
        to_print = str(self.__id) + "\n"
        to_print += "\twallet: " + str(self.__wallet) + "\n"
        to_print += "\tcurrent bet: " + str(self.__current_bet) + "\n"
        to_print += "\tHand: " + self.__hand.__repr__() + "\n"
        if self.__playing_flag:
            playing_status = "playing"
        else:
            playing_status = "fold"
        to_print += "\tstatus: " + playing_status + "\n"
        return to_print

    def print_without_hand(self):
        to_print = str(self.__id) + "\n"
        to_print += "\twallet: " + str(self.__wallet) + "\n"
        to_print += "\tcurrent bet: " + str(self.__current_bet) + "\n"
        if self.__playing_flag:
            playing_status = "playing"
        else:
            playing_status = "fold"
        to_print += "\tstatus: " + playing_status + "\n"
        return to_print

    @property
    def id(self):
        return self.__id

    @property
    def wallet(self):
        return self.__wallet

    @wallet.setter
    def wallet(self, new_wallet):
        if not isinstance(new_wallet, float):
            raise WrongTypeError("The Player's wallet that you provided is not a float")
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
        if not isinstance(new_playing_flag, bool):
            raise WrongTypeError("Trying to assign a playing flag that is not a boolean to a Player object.")
        self.__playing_flag = new_playing_flag


    @property
    def next_action(self):
        return self._next_action

    @next_action.setter
    def next_action(self, new_action):
        if new_action not in self.ACTIONS:
            raise PokerError("Trying to assign an action to a Player object that is not allowed ")
        self._next_action = new_action



    def ask_action(self, dealer):
        """
        This is maybe the most important action of the program since it is the method that encapsulates the whole
        policy of a player.
        In the standard case: that is for the base case it returns the exact same as a getter.
        """
        return self.next_action






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
