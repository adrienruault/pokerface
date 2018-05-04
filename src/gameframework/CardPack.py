



import random
import datetime
from .Card import Card
from .Error import *


class CardPack:

    def __init__(self, already_drawn_cards):
        for i, card in enumerate(already_drawn_cards):
            if not isinstance(card, Card):
                raise WrongTypeError("Trying to instantiate a CardPack object and specifying already_drawn_cards that are not Card objects")

            for j in range (len(already_drawn_cards)):
                if card == already_drawn_cards[j] and j != i:
                    raise PokerError("Trying to instantiate a CardPack object and specifying identical Card objects in already_drawn_cards")

        self.__drawn_cards = already_drawn_cards
        self.__random_gen = random.Random(datetime.datetime.now())

    # return one card taking into account cards that have already been drawn
    def draw(self):
        if len(self.__drawn_cards) >= 52:
            raise PokerError('Trying to distribute more than 52 cards')

        value = self.__random_gen.randint(1, 13)
        suit = self.__random_gen.randint(1,4)
        new_card = Card(value, suit)

        if (new_card in self.__drawn_cards):
            return self.draw()

        self.__drawn_cards += [new_card]
        return new_card


    # reset the drawn cards to an empty array
    def reset(self):
        self.__drawn_cards = []

    @property
    def drawn_cards(self):
        return self.__drawn_cards
