
import pytest
import unittest.mock as mock
from gameframework.terminal_emulator import *
from gameframework import Game, WrongTypeError

def initialize():
    players_list = [TerminalPlayer("a", 100.), TerminalPlayer("b", 100.)]
    game = Game(players_list)

    return game, players_list

@mock.patch('builtins.input', side_effect=['fold', 'caca', 'raise'])
def test_ask_action(input):
    game, players_list = initialize()

    player1 = players_list[0]
    player1.ask_action(game)

    assert player1.next_action == 'fold'

    player1.ask_action(game)
    assert player1.next_action == 'raise'


    with pytest.raises(WrongTypeError):
        player1.ask_action(1)
