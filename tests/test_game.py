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
    with pytest.raises(Exception):
        game2 = Game(players_list2)


def test_distribute_to_players():
    game = initialize()

    game.distribute_to_players()

    for _, player in game.players_dict.items():
        assert isinstance(player.hand, Hand)

    assert len(game.dealer.drawn_cards) == 6

    with pytest.raises(Exception):
        game.distribute_to_players()


def test_flop():
    game = initialize()

    with pytest.raises(Exception):
        game.flop()

    game.distribute_to_players()

    game.flop()

    assert len(game.dealer.drawn_cards) == 9

def test_turn():
    game = initialize()

    with pytest.raises(Exception):
        game.turn()



def test_get_winner():
    game = initialize()

    with pytest.raises(Exception):
        game.get_winner()
