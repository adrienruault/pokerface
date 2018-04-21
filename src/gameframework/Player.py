

from .Error import *
from .Hand import Hand


class Player():

    ACTIONS = ['check', 'open', 'fold', 'call', 'raise']

    def __init__(self, id_, wallet):
        if not isinstance(id_, int):
            raise WrongTypeError("The Player id that you provided is not an int.")
        if not isinstance(wallet, float):
            raise WrongTypeError("The Player's wallet that you provided is not a float")

        self.__id = id_
        self.__wallet = wallet
        self.__hand = None
        self.__next_action = None

    def receive_hand(self, hand):
        self.__hand = hand

    def change_wallet(self, amount):
        if amount > self.__wallet:
            raise PokerError("Trying to collect money from a Player object but it is more than it has.")
        self.__wallet += amount

    def __eq__(self, other):
        if (type(other) is not Player):
            raise WrongTypeError('Trying to check equality of a Player with an object that is not a Player.')

        return (other.id == self.__id)


    def __repr__(self):
        return "id: " + str(self.__id) + ' / Hand: ' + self.__hand.__repr__()

    @property
    def id(self):
        return self.__id

    @property
    def wallet(self):
        return self.__wallet

    @property
    def hand(self):
        return self.__hand

    @property
    def next_action(self):
        return self.__decision

    @next_action.setter
    def next_action(self, new_action):
        if new_decison not in ACTIONS:
            raise PokerError("Trying to assign an action to a Player object that is not allowed ")
        self.__next_action = new_action
