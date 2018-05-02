import pytest

from gameframework import *




def test_init():
    with pytest.raises(Exception):
        card = Card(0, 3)

    with pytest.raises(Exception):
        card = Card(14, 3)

    with pytest.raises(Exception):
        card = Card(2, 0)

    with pytest.raises(Exception):
        card = Card(2, 5)


def test_eq():

    card1 = Card(2, 1)
    card2 = Card(2, 1)
    card3 = Card(2, 3)
    card4 = Card(1, 1)

    with pytest.raises(Exception):
        card1 == 2

    assert card1 == card2
    assert card1 != card3
    assert card1 != card4

def test_lq():

    card1 = Card(2, 3)
    card2 = Card(1, 4)
    card3 = Card(4, 1)
    card4 = Card(2, 2)
    card5 = Card(2, 4)

    assert card1 > card2
    assert card1 < card3
    assert card1 > card4
    assert card1 < card5
