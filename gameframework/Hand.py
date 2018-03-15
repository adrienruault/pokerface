





class Hand:

    def __init__(self):
        self.__cards = [None, None]

    def __repr__(self):
        return self.__cards.__repr__()

    def get_cards(self):
        return self.__cards

    def reset(self):
        self.__cards = [None, None]

    def distribute(self, dealer):
        self.__cards = [dealer.draw(), dealer.draw()]
