
import pytest
import unittest.mock as mock

from gameframework import TerminalEmulator



@mock.patch('builtins.input', side_effect=['2', 'adrien', '100', 'antoine', '100', 'fold', 'no'])
def test_all_folding(input):
    emulator = TerminalEmulator()
    emulator.launch()


@mock.patch('builtins.input', side_effect=['2', 'adrien', '100', 'antoine', '100', 'call', 'call', 'call', 'call', 'call', 'call', 'call', 'call', 'no'])
def test_all_calling(input):
    emulator = TerminalEmulator()
    emulator.launch()



@mock.patch('builtins.input', side_effect=['-1', '10', '2',\
                                            'very_long_name_very_long' 'adrien',\
                                            '-1', 'abc', '100',\
                                            'antoine', '100',\
                                            'caca', 'fold', 'boudin', 'no'])
                                            
def test_challenge_input(input):
    emulator = TerminalEmulator()
    emulator.launch()
