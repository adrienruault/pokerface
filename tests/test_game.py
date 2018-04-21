import pytest

from gameframework import *
import pdb


def initialize():
    players_list = [Player(1, 1000.), Player(2, 1000.), Player(3, 1000.)]
    game = Game(players_list)

    return game


def test_init():

    players_list1 = [Player(1, 1000.), Player(2, 1000.), Player(3, 1000.)]
    game1 = Game(players_list1)
    for player in players_list1:
        assert game1.players_dict[player.id] == player
    #assert game1.players_dict == players_list1
    assert game1.state == "start"

    players_list2 = [Player(1, 1000.), Player(1, 1000.)]
    with pytest.raises(PokerError):
        game2 = Game(players_list2)


def test_distribute_hands():
    game = initialize()

    game.collect_blinds()

    game.distribute_hands()

    for _, player in game.players_dict.items():
        assert isinstance(player.hand, Hand)

    assert len(game.dealer.drawn_cards) == 6

    with pytest.raises(PokerError):
        game.distribute_hands()


def test_flop():
    game = initialize()

    with pytest.raises(PokerError):
        game.flop()

    game.collect_blinds()
    game.distribute_hands()

    game.flop()
    assert len(game.dealer.drawn_cards) == 9


    with pytest.raises(PokerError):
        game.flop()


def test_turn():
    game = initialize()

    with pytest.raises(PokerError):
        game.turn()


def test_transfer_money():
    players_list = [Player(1, 1000.), Player(2, 1000.), Player(3, 1000.)]
    game = Game(players_list)

    game.transfer_money(1, -10.)
    player1 = game.get_player_from_id(1)
    assert abs(player1.wallet - 990.) < 1e-8

    game.transfer_money(2, 5.)
    player2 = game.get_player_from_id(2)
    assert abs(player2.wallet - 1005.) < 1e-8

    assert abs(game.pot - (10 - 5)) < 1e-8

    with pytest.raises(MoneyError):
        game.transfer_money(3, 2000.)


def test_collect_blinds():
    players_list = [Player(1, 1000.), Player(2, 1000.), Player(3, 1000.)]
    game = Game(players_list)

    game.collect_blinds()

    player1 = game.get_player_from_id(1)
    assert abs(player1.wallet - (1000 - game.small_blind)) < 1e-8

    player2 = game.get_player_from_id(2)
    assert abs(player2.wallet - (1000 - game.big_blind)) < 1e-8

    player3 = game.get_player_from_id(3)
    assert abs(player3.wallet - 1000) < 1e-8

    assert abs(game.pot - (game.small_blind + game.big_blind)) < 1e-8

    with pytest.raises(PokerError):
        game.collect_blinds()
