

from gameframework import *



def initialize():
    dealer = Dealer([])
    return Hand(dealer), dealer


def test_init():
    hand, dealer = initialize()

    assert isinstance(hand, Hand)
    assert hand.dealer == dealer


def test_reset_cards():
    hand, dealer = initialize()

    assert len(dealer.drawn_cards) == 0

    hand.receive_cards()

    assert len(dealer.drawn_cards) == 2

def test__repr__():
    hand, dealer = initialize()    
    hand.__repr__()
