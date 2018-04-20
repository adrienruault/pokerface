





class Hand:

    def __init__(self, dealer):
        self.__cards = [None, None]
        self.__dealer = dealer

    def __repr__(self):
        return self.__cards.__repr__()

    def reset_cards(self):
        self.__cards = [None, None]

    def receive_cards(self):
        self.__cards = [self.__dealer.draw(), self.__dealer.draw()]


    @property
    def cards(self):
        return self.__cards

    @cards.setter
    def cards(self, new_cards):
        self.__cards = new_cards
