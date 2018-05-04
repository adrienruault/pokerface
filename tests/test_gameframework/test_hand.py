

from gameframework import *



def initialize():
    card_pack = CardPack([])
    return Hand(card_pack), card_pack


def test_init():
    hand, card_pack = initialize()

    assert isinstance(hand, Hand)
    assert hand.card_pack == card_pack


def test_reset():
    hand, card_pack = initialize()

    assert len(card_pack.drawn_cards) == 0

    hand.receive_cards()

    assert len(card_pack.drawn_cards) == 2

def test__repr__():
    hand, card_pack = initialize()
    hand.__repr__()
