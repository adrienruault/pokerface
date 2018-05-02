import pytest

from gameframework import *
import pdb


def initialize_check_players():
    players_list = [Player("a", 1000.), Player("b", 1000.), Player("c", 1000.)]
    for player in players_list:
        player.next_action = "check"
    game = Game(players_list)

    return game

def test_properties():
    game = initialize_check_players()
    empty_board = Board(game.dealer)

    board = game.board

    assert board == empty_board

def test_init_players_are_well_added():

    players_list1 = [Player("a", 1000.), Player("b", 1000.), Player("c", 1000.)]
    game1 = Game(players_list1)

    # Check that the players are well added
    for player in players_list1:
        assert game1.players_dict[player.id] == player
    #assert game1.players_dict == players_list1
    assert game1.state == "start"


def test_init_players_have_unique_id():
    # Check that cannot have two players with same id
    players_list2 = [Player("a", 1000.), Player("a", 1000.)]
    with pytest.raises(PokerError):
        game2 = Game(players_list2)


def test_init_players_are_doubly_linked_listed():
    # Check the good working of the doubly linked list
    players_list = [Player("a", 1000.), Player("b", 1000.), Player("c", 1000.)]
    game = Game(players_list)

    player = game.get_player_from_id("a")
    player_next1 = player.next_player
    player_next2 = player_next1.next_player

    assert player == players_list[0]
    assert player_next1 == players_list[1]
    assert player_next2 == players_list[2]
    assert player.playing_flag == True
    assert player_next1.playing_flag == True
    assert player_next2.playing_flag == True


def test_init_game_contains_more_than_2_players():
    # Check that we cannot create a game with only one Player
    with pytest.raises(PokerError):
        game3 = Game([Player("a", 1000.)])



def test_distribute_hands():
    game = initialize_check_players()

    game.collect_blinds()

    game.distribute_hands()

    for _, player in game.players_dict.items():
        assert isinstance(player.hand, Hand)

    assert len(game.dealer.drawn_cards) == 6

    with pytest.raises(PokerError):
        game.distribute_hands()


def test_flop():
    game = initialize_check_players()

    with pytest.raises(PokerError):
        game.flop()

    game.collect_blinds()
    game.distribute_hands()

    game.flop()
    assert len(game.dealer.drawn_cards) == 9


    with pytest.raises(PokerError):
        game.flop()


def test_turn():
    game = initialize_check_players()

    with pytest.raises(PokerError):
        game.turn()

    game.collect_blinds()
    game.distribute_hands()
    game.flop()
    game.turn()

    assert len(game.dealer.drawn_cards) == 10

    with pytest.raises(PokerError):
        game.turn()

def test_river():
    game = initialize_check_players()

    with pytest.raises(PokerError):
        game.river()

    game.collect_blinds()
    game.distribute_hands()
    game.flop()
    game.turn()
    game.river()

    assert len(game.dealer.drawn_cards) == 11




def test_collect_blinds():
    game = initialize_check_players()

    game.collect_blinds()

    player1 = game.get_player_from_id("a")
    assert abs(player1.wallet - (1000 - game.small_blind)) < 1e-8

    player2 = game.get_player_from_id("b")
    assert abs(player2.wallet - (1000 - game.big_blind)) < 1e-8

    player3 = game.get_player_from_id("c")
    assert abs(player3.wallet - 1000) < 1e-8

    assert abs(game.pot - (game.small_blind + game.big_blind)) < 1e-8

    with pytest.raises(PokerError):
        game.collect_blinds()



def test_full_game_with_checking_players():

    players_list = [Player("a", 1000.), Player("b", 1000.), Player("c", 1000.)]
    players_list[0].next_action = "call"
    players_list[1].next_action = "raise"
    players_list[2].next_action = "fold"

    game = Game(players_list)

    game.collect_blinds()
    game.distribute_hands()
    game.flop()
    game.turn()
    game.river()

    assert game.state == "finished"
    assert abs(game.pot) < 1e-8
    assert game.target_bet > 0
    assert len(game.dealer.drawn_cards) == 11

    game.restart()
