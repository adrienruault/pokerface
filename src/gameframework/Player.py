

from .Error import *
from .Hand import Hand


class Player():

    def __init__(self, id_, wallet):
        if not isinstance(id_, int):
            raise WrongTypeError("The Player id that you provided is not an int.")
        if not isinstance(wallet, float):
            raise WrongTypeError("The Player's wallet that you provided is not a float")

        self.__id = id_

        self.__wallet = wallet

        self.__hand = None

    def receive_hand(self, hand):
        self.__hand = hand

    def __eq__(self, other):
        if (type(other) is not Player):
            raise WrongTypeError('Trying to check equality of a Player with an object that is not a Player')

        return (other.id == self.__id)


    def __repr__(self):
        return "id: " + str(self.__id) + ' / Hand: ' + self.__hand.__repr__()

    @property
    def id(self):
        return self.__id

    @property
    def hand(self):
        return self.__hand
