





class Hand:

    def __init__(self, card_pack):
        self.__cards = [None, None]
        self.__card_pack = card_pack

    def __repr__(self):
        return self.__cards.__repr__()

    def reset(self):
        self.__cards = [None, None]

    def receive_cards(self):
        self.__cards = [self.__card_pack.draw(), self.__card_pack.draw()]


    @property
    def cards(self):
        return self.__cards


    @property
    def card_pack(self):
        return self.__card_pack
