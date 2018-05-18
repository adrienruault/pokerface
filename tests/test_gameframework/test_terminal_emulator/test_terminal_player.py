
import pytest
import unittest.mock as mock
from gameframework.terminal_emulator import *
from gameframework import Dealer, WrongTypeError

def initialize():
    players_list = [TerminalPlayer("a", 100.), TerminalPlayer("b", 100.)]
    dealer = Dealer(players_list)

    return dealer, players_list

@mock.patch('builtins.input', side_effect=['', 'fold', '', '',  'caca', 'raise', ''])
def test_ask_action(input):
    dealer, players_list = initialize()

    player1 = players_list[0]
    player1.ask_action(dealer)

    assert player1.played_action == 'fold'

    player1.ask_action(dealer)
    assert player1.played_action == 'raise'


    with pytest.raises(WrongTypeError):
        player1.ask_action(1)
