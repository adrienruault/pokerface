[![Build Status](https://travis-ci.org/adrienruault/pokerface.svg?branch=master)](https://travis-ci.org/adrienruault/pokerface)
[![Coverage Status](https://coveralls.io/repos/github/adrienruault/pokerface/badge.svg?branch=master)](https://coveralls.io/github/adrienruault/pokerface?branch=master)
# pokerface

`gameframework` is a package that emulates poker dealers.

Here is an example of how to run a dealer:

```python
def main():
    # Definition of all the players
    players_list = [Player(1, 1000.), Player(2, 1000.), Player(3, 1000.)]
    
    # Instantiation of the dealer
    dealer = Dealer(players_list)
    
    # Proceedings of the dealer
    dealer.collect_blinds()
    dealer.distribute_hands()
    dealer.flop()
    dealer.turn()
    dealer.river()
    
    # The restart method allows to start a new dealer with the same set of players
    dealer.restart()
```

At each step of the dealer, the the `Player.next_action()` method is called to know the policy of each player when they have to take a decision. Finding a good policy to be coded in this method is all the point of this project.


## Tests

**Run the tests**: run the command `pytest`. It automatically finds files starting with "test_" and run them.

**Get line coverage**: run the command `pytest --cov=gameframework .`. It is the same as running `pytest` but also computes the line coverage in `gameframework`
