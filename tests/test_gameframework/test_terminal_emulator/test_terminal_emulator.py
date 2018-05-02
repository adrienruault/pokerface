
import pytest
import unittest.mock as mock

from gameframework import TerminalEmulator



@mock.patch('builtins.input', side_effect=['2', 'adrien', '100', 'antoine', '100', 'fold', 'no'])
def test_all_folding(input):

    emulator = TerminalEmulator()
    emulator.launch()
