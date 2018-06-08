import pytest

from gameframework import *
import pdb


def initialize_call_players():
    players_list = [Player("a", 1000.), Player("b", 1000.), Player("c", 1000.)]
    for player in players_list:
        player.played_action = "call"
    game_master = GameMaster(players_list)

    return game_master

def test_properties():
    game_master = initialize_call_players()
    empty_board = Board(game_master.card_pack)

    board = game_master.board

    assert board == empty_board

def test_init_players_are_well_added():

    players_list1 = [Player("a", 1000.), Player("b", 1000.), Player("c", 1000.)]
    game_master1 = GameMaster(players_list1)

    # Check that the players are well added
    for player in players_list1:
        assert game_master1.players_dict[player.id] == player
    #assert game_master1.players_dict == players_list1
    assert game_master1.state == "start"


def test_init_players_have_unique_id():
    # Check that cannot have two players with same id
    players_list2 = [Player("a", 1000.), Player("a", 1000.)]
    with pytest.raises(PokerError):
        game_master2 = GameMaster(players_list2)


def test_init_players_are_doubly_linked_listed():
    # Check the good working of the doubly linked list
    players_list = [Player("a", 1000.), Player("b", 1000.), Player("c", 1000.)]
    game_master = GameMaster(players_list)

    player = game_master.get_player_from_id("a")
    player_next1 = player.next_player
    player_next2 = player_next1.next_player

    assert player == players_list[0]
    assert player_next1 == players_list[1]
    assert player_next2 == players_list[2]
    assert player.playing_flag == True
    assert player_next1.playing_flag == True
    assert player_next2.playing_flag == True


def test_init_game_master_contains_more_than_2_players():
    # Check that we cannot create a game_master with only one Player
    with pytest.raises(PokerError):
        game_master3 = GameMaster([Player("a", 1000.)])



def test_distribute_hands():
    game_master = initialize_call_players()

    game_master.collect_blinds()

    game_master.distribute_hands()

    for _, player in game_master.players_dict.items():
        assert isinstance(player.hand, Hand)

    assert len(game_master.card_pack.drawn_cards) == 6

    with pytest.raises(PokerError):
        game_master.distribute_hands()


def test_flop():
    game_master = initialize_call_players()

    with pytest.raises(PokerError):
        game_master.flop()

    game_master.collect_blinds()

    game_master.distribute_hands()
    game_master.bet_round()

    game_master.flop()
    game_master.bet_round()

    assert len(game_master.card_pack.drawn_cards) == 9


    with pytest.raises(PokerError):
        game_master.flop()


def test_turn():
    game_master = initialize_call_players()

    with pytest.raises(PokerError):
        game_master.turn()

    game_master.collect_blinds()

    game_master.distribute_hands()
    game_master.bet_round()

    game_master.flop()
    game_master.bet_round()

    game_master.turn()
    game_master.bet_round()

    assert len(game_master.card_pack.drawn_cards) == 10

    with pytest.raises(PokerError):
        game_master.turn()

def test_river():
    game_master = initialize_call_players()

    with pytest.raises(PokerError):
        game_master.river()

    game_master.collect_blinds()

    game_master.distribute_hands()
    game_master.bet_round()

    game_master.flop()
    game_master.bet_round()

    game_master.turn()
    game_master.bet_round()

    game_master.river()
    game_master.bet_round()

    assert len(game_master.card_pack.drawn_cards) == 11




def test_collect_blinds():
    game_master = initialize_call_players()

    game_master.collect_blinds()

    player1 = game_master.get_player_from_id("a")
    assert abs(player1.wallet - (1000 - game_master.small_blind)) < 1e-8

    player2 = game_master.get_player_from_id("b")
    assert abs(player2.wallet - (1000 - game_master.big_blind)) < 1e-8

    player3 = game_master.get_player_from_id("c")
    assert abs(player3.wallet - 1000) < 1e-8

    assert abs(player1.current_bet + player2.current_bet - (game_master.small_blind + game_master.big_blind)) < 1e-8

    with pytest.raises(PokerError):
        game_master.collect_blinds()



def test_full_game_master_with_various_players():

    #pdb.set_trace()

    players_list = [Player("a", 1000.), Player("b", 1000.), Player("c", 1000.)]
    players_list[0].played_action = "call"
    players_list[1].played_action = "raise"
    players_list[2].played_action = "fold"

    game_master = GameMaster(players_list)

    game_master.collect_blinds()

    game_master.distribute_hands()
    game_master.bet_round()

    game_master.flop()
    game_master.bet_round()

    game_master.turn()
    game_master.bet_round()

    game_master.river()
    game_master.bet_round()


    assert game_master.state == "finished"
    assert abs(game_master.pot) < 1e-8
    assert abs(game_master.target_bet) <  1e-8
    assert len(game_master.card_pack.drawn_cards) == 11

    game_master.reset()
