


from .Error import *



class Card:

    VALUES = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    SUITS = ['H', 'D', 'C', 'S']


    def __init__(self, value, suit):
        if value < 1 or value > 13:
            raise PokerError("Trying to instantiate a Card object whose value is not in [1,13]")
        if suit < 1 or suit > 4:
            raise PokerError("Trying to instantiate a Card object whose suit is not in [1,4]")
        self.__value = value
        self.__suit = suit

    def __eq__(self, other):
        if (type(other) is not Card):
            raise WrongTypeError('Trying to check equality of a Card with an object that is not a Card')

        return (other.value == self.__value and other.suit == self.__suit)

    def __lt__(self, other):
        if type(other) is not Card:
            raise WrongTypeError('Trying to compare a Card with something else than a Card object.')

        if self.__value < other.value:
            return True
        elif self.__value == other.value:
                return self.__suit < other.suit
        else:
            return False


    def __repr__(self):
        return self.VALUES[self.__value-1] + "-" + self.SUITS[self.__suit-1]

    @property
    def value(self):
        return self.__value

    @property
    def suit(self):
        return self.__suit
