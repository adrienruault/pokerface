
from .Card import Card





class Board:

    def __init__(self):
        self.__cards = [None, None, None, None, None]
        self.__turn = 0

    def flop(self, dealer):
        if self.__turn != 0:
            raise PokerError('Trying to draw a flop that is not authorized.')

        else:
            self.__cards[0] = dealer.draw()
            self.__cards[1] = dealer.draw()
            self.__cards[2] = dealer.draw()

            self.__turn += 1;

    def turn(self, dealer):
        if self.__turn != 1:
            raise PokerError('Trying to draw a turn that is not authorized.')

        else:
            self.__cards[3] = dealer.draw()

            self.__turn += 1

    def river(self, dealer):
        if self.__turn != 2:
            raise PokerError('Trying to draw a river that is not authorized.')

        else:
            self.__cards[4] = dealer.draw()

            self.__turn +=1

    def __repr__(self):
        return self.__cards.__repr__()

    def get_turn(self):
        return self.__turn

    def get_cards(self):
        return self.__cards

    def reset(self):
        self.__cards = [None, None, None, None, None]
        self.__turn = 0
