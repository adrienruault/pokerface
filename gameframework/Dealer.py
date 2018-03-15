



import random
import datetime
from .Card import Card


class Dealer:

    def __init__(self, drawn_cards):
        self.__drawn_cards = drawn_cards
        self.__random_gen = random.Random(datetime.datetime.now())

    # return one card taking into account cards that have already been drawn
    def draw(self):
        value = self.__random_gen.randint(1, 13)
        suit = self.__random_gen.randint(1,4)
        new_card = Card(value, suit)
        if (new_card in self.__drawn_cards):
            return self.draw()
        self.__drawn_cards += [new_card]
        return new_card

    def get_drawn_cards(self):
        return self.__drawn_cards

    # reset the drawn cards to an empty array
    def reset(self):
        self.__drawn_cards = []
