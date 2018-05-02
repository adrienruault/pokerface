[![Build Status](https://travis-ci.org/adrienruault/pokerface.svg?branch=master)](https://travis-ci.org/adrienruault/pokerface)
[![Coverage Status](https://coveralls.io/repos/github/adrienruault/pokerface/badge.svg?branch=master)](https://coveralls.io/github/adrienruault/pokerface?branch=master)
# pokerface

The idea of this project is to use reinforcement learning to create an AI able to play poker.


## Requirements

The software runs with python3 and the following python packages are needed:

- numpy



## gameframework

`gameframework` is a package that allows to emulate poker games.

Here is an example of how to run a simple game programmatically:

```python
def main():
    # Definition of all the players
    players_list = [Player("a", 1000.), Player("b", 1000.), Player("c", 1000.)]
    
    # Instantiation of the game
    game = Game(players_list)
    
    # Proceedings of the game
    game.collect_blinds()
    game.distribute_hands()
    game.flop()
    game.turn()
    game.river()
    
    # The restart method allows to start a new game with the same set of players
    game.restart()
```

At each step of the game, the the `Player.next_action()` method is called to know the policy of each player when they have to take a decision. Finding a good policy to be encapsulated in this method is all the point of this project.


### Terminal emulator

A terminal emulator to play poker on terminal has been developed that you can use by running `try_terminal_emulator.py`. From the parent directory you can run:

```python
# From parent directory
python src/try_terminal_emulator.py
```

The emulator haven't been fully tested yet and might be a little buggy but you should be able to play some games against yourself.



## Tests

**Run the tests**: run the command `pytest`. It automatically finds files starting with "test_" and run them.

**Get line coverage**: run the command `pytest --cov=gameframework .`. It is the same as running `pytest` but also computes the line coverage in `gameframework`



## Credits

- Template for the TensorFlow models: https://github.com/MrGemy95/Tensorflow-Project-Template
