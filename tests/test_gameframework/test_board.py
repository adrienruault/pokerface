import pytest

from gameframework import *


def initialize():
    card_pack = CardPack([])
    board = Board(card_pack)
    return board, card_pack


def test_init():
    board, card_pack = initialize()
    assert board.cards[4] == None
    assert board.stage == 0
    assert board.card_pack == card_pack


def test_flop():
    board, card_pack = initialize()
    board.flop()

    assert board.cards[4] == None
    assert isinstance(board.cards[0], Card)
    assert len(board.cards) == 5
    assert board.stage == 1
    assert len(card_pack.drawn_cards) == 3

def test_turn():
    board, card_pack = initialize()

    with pytest.raises(Exception):
        board.turn()

    board.flop()
    board.turn()

    assert board.cards[4] == None
    assert isinstance(board.cards[0], Card)
    assert len(board.cards) == 5
    assert board.stage == 2
    assert len(card_pack.drawn_cards) == 4


def test_river():
    board, card_pack = initialize()

    with pytest.raises(Exception):
        board.river()

    board.flop()
    board.turn()
    board.river()

    assert isinstance(board.cards[4], Card)
    assert isinstance(board.cards[0], Card)
    assert len(board.cards) == 5
    assert board.stage == 3
    assert len(card_pack.drawn_cards) == 5


def test_reset():
    board, card_pack = initialize()

    board.flop()
    board.turn()
    board.river()

    assert isinstance(board.cards[4], Card)

    board.reset()
    assert board.cards[4] == None
    assert board.stage == 0
    assert board.card_pack == card_pack


def test__eq__():
    card_pack = CardPack([])
    board1 = Board(card_pack)
    board2 = Board(card_pack)

    assert board1 == board2

    board2.flop()

    assert board1 != board2
