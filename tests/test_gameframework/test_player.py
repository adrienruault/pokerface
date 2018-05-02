

from gameframework import *
import pytest




def test_init__():

    with pytest.raises(WrongTypeError):
        player = Player(4, 3.)

    with pytest.raises(WrongTypeError):
        player = Player(2, 3)


def test__eq__():
    player1 = Player("a", 1000.)
    player2 = Player("a", 1000.)
    player3 = Player("b", 1000.)

    assert player1 == player2
    assert player1 != player3

    with pytest.raises(WrongTypeError):
        player1 == 1

def test__repr__():
    player = Player("a", 1000.)
    player.__repr__()

def test_wallet():
    player = Player("a", 1000.)
    player.wallet = 2.

    assert abs(player.wallet - 2.) < 1e-8

    with pytest.raises(PokerError):
        player.wallet = -2.

    with pytest.raises(WrongTypeError):
        player.wallet = "alpha"
