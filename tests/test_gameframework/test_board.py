import pytest

from gameframework import *


def initialize():
    dealer = Dealer([])
    board = Board(dealer)
    return board, dealer


def test_init():
    board, dealer = initialize()
    assert board.cards[4] == None
    assert board.stage == 0
    assert board.dealer == dealer


def test_flop():
    board, dealer = initialize()
    board.flop()

    assert board.cards[4] == None
    assert isinstance(board.cards[0], Card)
    assert len(board.cards) == 5
    assert board.stage == 1
    assert len(dealer.drawn_cards) == 3

def test_turn():
    board, dealer = initialize()

    with pytest.raises(Exception):
        board.turn()

    board.flop()
    board.turn()

    assert board.cards[4] == None
    assert isinstance(board.cards[0], Card)
    assert len(board.cards) == 5
    assert board.stage == 2
    assert len(dealer.drawn_cards) == 4


def test_river():
    board, dealer = initialize()

    with pytest.raises(Exception):
        board.river()

    board.flop()
    board.turn()
    board.river()

    assert isinstance(board.cards[4], Card)
    assert isinstance(board.cards[0], Card)
    assert len(board.cards) == 5
    assert board.stage == 3
    assert len(dealer.drawn_cards) == 5


def test_reset():
    board, dealer = initialize()

    board.flop()
    board.turn()
    board.river()

    assert isinstance(board.cards[4], Card)

    board.reset()
    assert board.cards[4] == None
    assert board.stage == 0
    assert board.dealer == dealer


def test__eq__():
    dealer = Dealer([])
    board1 = Board(dealer)
    board2 = Board(dealer)

    assert board1 == board2

    board2.flop()

    assert board1 != board2
