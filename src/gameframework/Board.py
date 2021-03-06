
from .Card import Card





class Board:

    def __init__(self, card_pack):
        self.__cards = [None, None, None, None, None]
        self.__stage = 0
        self.__card_pack = card_pack

    def flop(self):
        if self.__stage != 0:
            raise PokerError('Trying to draw a flop that is not authorized.')

        else:
            self.__cards[0] = self.__card_pack.draw()
            self.__cards[1] = self.__card_pack.draw()
            self.__cards[2] = self.__card_pack.draw()

            self.__stage += 1;

    def turn(self):
        if self.__stage != 1:
            raise PokerError('Trying to draw a turn that is not authorized.')

        else:
            self.__cards[3] = self.__card_pack.draw()

            self.__stage += 1

    def river(self):
        if self.__stage != 2:
            raise PokerError('Trying to draw a river that is not authorized.')

        else:
            self.__cards[4] = self.__card_pack.draw()

            self.__stage +=1




    def next_stage(self):
        """
        This method identifies the stage the board is in and then triggers the
        next stage.
        """

        if self.__stage == 0:
            self.flop()
        elif self.__stage == 1:
            self.turn()
        elif self.__stage == 2:
            self.river()
        else:
            raise PokerError("Trying to go further than the river")






    def __repr__(self):
        return self.__cards.__repr__()

    def __eq__(self, other):
        if (type(other) is not Board):
            raise WrongTypeError('Trying to check equality of a Board with an object that is not a Board')

        for i in range(5):
            if self.__cards[i] != other.cards[i]:
                return False

            if self.__stage != other.stage:
                return False

            return True

    def reset(self):
        self.__cards = [None, None, None, None, None]
        self.__stage = 0


    @property
    def stage(self):
        return self.__stage

    @stage.setter
    def stage(self, new_stage):
        self.__stage = new_stage


    @property
    def cards(self):
        return self.__cards

    @cards.setter
    def cards(self, new_cards):
        self.__cards = new_cards


    @property
    def card_pack(self):
        return self.__card_pack
