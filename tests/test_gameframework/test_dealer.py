import pytest

from gameframework import *


def test_init():
    dealer1 = Dealer([])

    assert len(dealer1.drawn_cards) == 0

    card1 = Card(1, 2)
    card2 = Card(1, 3)
    card3 = Card(1, 2)

    dealer2 = Dealer([card1, card2])

    assert len(dealer2.drawn_cards) == 2


    with pytest.raises(Exception):
        dealer3 = Dealer([card1, card3])

def test_cannot_draw_more_than_52():
    dealer = Dealer([])

    with pytest.raises(Exception):
        for i in range(53):
            dealer.draw()

def test_suit_odds():
    dealer = Dealer([])

    count_suit_1 = 0
    total_drawn = 0
    number_draw = 1000

    for i in range(number_draw):
        card = dealer.draw()
        if card.suit == 1:
            count_suit_1 += 1
        total_drawn += 1
        dealer.reset()

    observed_odd = float(count_suit_1) / float(number_draw)
    assert abs(observed_odd - 0.25) < 0.05

def test_value_odds():
    dealer = Dealer([])

    count_value_13 = 0
    total_drawn = 0
    number_draw = 1000

    for i in range(number_draw):
        card = dealer.draw()
        if card.value == 13:
            count_value_13 += 1
        total_drawn += 1
        dealer.reset()

    observed_odd = float(count_value_13) / float(number_draw)
    assert abs(observed_odd - 1 / 13.) < 0.05

def test_reset():

    dealer = Dealer([])
    dealer.draw()
    assert len(dealer.drawn_cards) == 1
    dealer.reset()
    assert len(dealer.drawn_cards) == 0
