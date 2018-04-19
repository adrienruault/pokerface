
from .Card import Card





class Board:

    def __init__(self, dealer):
        self.__cards = [None, None, None, None, None]
        self.__stage = 0
        self.__dealer = dealer

    def flop(self):
        if self.__stage != 0:
            raise PokerError('Trying to draw a flop that is not authorized.')

        else:
            self.__cards[0] = self.__dealer.draw()
            self.__cards[1] = self.__dealer.draw()
            self.__cards[2] = self.__dealer.draw()

            self.__stage += 1;

    def turn(self):
        if self.__stage != 1:
            raise PokerError('Trying to draw a turn that is not authorized.')

        else:
            self.__cards[3] = self.__dealer.draw()

            self.__stage += 1

    def river(self):
        if self.__stage != 2:
            raise PokerError('Trying to draw a river that is not authorized.')

        else:
            self.__cards[4] = self.__dealer.draw()

            self.__stage +=1

    def __repr__(self):
        return self.__cards.__repr__()

    @property
    def stage(self):
        return self.__stage

    def get_cards(self):
        return self.__cards

    def reset(self):
        self.__cards = [None, None, None, None, None]
        self.__stage = 0
