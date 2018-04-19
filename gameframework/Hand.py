





class Hand:

    def __init__(self, dealer):
        self.__cards = [None, None]
        self.__dealer = dealer

    def __repr__(self):
        return self.__cards.__repr__()

    def get_cards(self):
        return self.__cards

    def reset_cards(self):
        self.__cards = [None, None]

    def distribute(self):
        self.__cards = [self.__dealer.draw(), self.__dealer.draw()]
