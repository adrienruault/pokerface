import pytest

from gameframework import *


def test_init():
    card_pack1 = CardPack([])

    assert len(card_pack1.drawn_cards) == 0

    card1 = Card(1, 2)
    card2 = Card(1, 3)
    card3 = Card(1, 2)

    card_pack2 = CardPack([card1, card2])

    assert len(card_pack2.drawn_cards) == 2


    with pytest.raises(Exception):
        card_pack3 = CardPack([card1, card3])

def test_cannot_draw_more_than_52():
    card_pack = CardPack([])

    with pytest.raises(Exception):
        for i in range(53):
            card_pack.draw()

def test_suit_odds():
    card_pack = CardPack([])

    count_suit_1 = 0
    total_drawn = 0
    number_draw = 1000

    for i in range(number_draw):
        card = card_pack.draw()
        if card.suit == 1:
            count_suit_1 += 1
        total_drawn += 1
        card_pack.reset()

    observed_odd = float(count_suit_1) / float(number_draw)
    assert abs(observed_odd - 0.25) < 0.05

def test_value_odds():
    card_pack = CardPack([])

    count_value_13 = 0
    total_drawn = 0
    number_draw = 1000

    for i in range(number_draw):
        card = card_pack.draw()
        if card.value == 13:
            count_value_13 += 1
        total_drawn += 1
        card_pack.reset()

    observed_odd = float(count_value_13) / float(number_draw)
    assert abs(observed_odd - 1 / 13.) < 0.05

def test_reset():

    card_pack = CardPack([])
    card_pack.draw()
    assert len(card_pack.drawn_cards) == 1
    card_pack.reset()
    assert len(card_pack.drawn_cards) == 0
