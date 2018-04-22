[![Build Status](https://travis-ci.org/adrienruault/pokerface.svg?branch=master)](https://travis-ci.org/adrienruault/pokerface)
[![Coverage Status](https://coveralls.io/repos/github/adrienruault/pokerface/badge.svg?branch=master)](https://coveralls.io/github/adrienruault/pokerface?branch=master)
# pokerface

`gameframework` is a package that emulates poker games.

Here is an example of how to run a game:

```python
def main():
    players_list = [Player(1, 1000.), Player(2, 1000.), Player(3, 1000.)]
    
    game = Game(players_list)
    
    game.collect_blinds()
    game.distribute_hands()
    game.flop()
    game.turn()
    game.river()
```

At each step of the game, the the `Player.next_action` method is called to know the policy of each Player when they have to take a decision.


## Tests

**run the tests**: run the command `pytest`. It automatically finds files starting with "test_" and run them.

**Get line coverage**: run the command `pytest --cov=gameframework .`. It is the same as running `pytest` but also computes the line coverage in `gameframework`
