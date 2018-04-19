

from .Error import *
from .Hand import Hand


class Player():

    def __init__(self, num_id, wallet):
        if not isinstance(num_id, int):
            raise WrongTypeError("The Player id that you provided is not an int.")
        if not isinstance(wallet, float):
            raise WrongTypeError("The Player's wallet that you provided is not a float")

        self.__id = num_id

        self.__wallet = wallet

        self.__hand = None

    def receive_hand(hand):
        self.__hand = hand

    def __repr__(self):
        return "id: " + str(self.__id) + ' / Hand: ' + self.__hand.__repr__()
