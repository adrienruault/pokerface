






class Card:

    VALUES = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    SUITS = ['H', 'D', 'C', 'S']


    def __init__(self, value, suit):
        assert 0 < value <= 13
        assert 0 < suit <= 4
        self.__value = value
        self.__suit = suit

    def __eq__(self, other):
        if (type(other) is not Card):
            raise WrongTypeError('Trying to check equality of a Card with an object that is not a Card')

        return (other.get_value() == self.__value and other.get_suit() == self.__suit)

    def __lt__(self, other):
        if type(other) is not Card:
            raise WrongTypeError('Trying to compare a Card with something else than a Card object.')

        if self.__value < other.get_value():
            return True
        elif self.__value == other.get_value():
            return self.__suit < other.get_suit()
        else:
            return False


    def __repr__(self):
        return self.VALUES[self.__value-1] + "-" + self.SUITS[self.__suit-1]


    def get_value(self):
        return self.__value

    def get_suit(self):
        return self.__suit
