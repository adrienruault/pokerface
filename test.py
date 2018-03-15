
#from gameframework import *
from gameframework import *
import numpy as np



def can_draw_board():
    print("*** can_draw_board ***")
    dealer = Dealer([])

    card1 = dealer.draw()
    print("Draw a card:", card1)

    hand = Hand()
    hand.distribute(dealer)
    print("Draw a hand:", hand)

    print("\nBoard creation:")
    board = Board()
    print("Empty board:", board)
    board.flop(dealer)
    print("After flop:", board)
    board.turn(dealer)
    print("After turn:", board)
    board.river(dealer)
    print("After river:", board)

    print()
    print("Drawn cards:", dealer.get_drawn_cards())
    assert len(dealer.get_drawn_cards()) == 8

    print("*** can_draw_board finished ***")




def can_showdown():

    print()
    print("*** can_showdown ***")
    dealer = Dealer([])

    hand = Hand()
    hand.distribute(dealer)

    board = Board()
    board.flop(dealer)
    board.turn(dealer)
    board.river(dealer)

    showdown = Showdown(hand, board)
    print('Hand:', hand)
    print('Board:', board)
    print('Showdown:', showdown)


    print("*** can_showdown finished ***")



def can_identify_ranks_accurately():
    # Royal flush 	4,324 	0.0032% 	0.0032% 	30,939 : 1
    # Straight flush (excl. royal flush) 	37,260 	0.0279% 	0.0311% 	3,589.6 : 1
    # Four of a kind 	224,848 	0.168% 	0.199% 	594 : 1
    # Full house 	3,473,184 	2.60% 	2.80% 	37.5 : 1
    # Flush 	4,047,644 	3.03% 	5.82% 	32.1 : 1
    # Straight 	6,180,020 	4.62% 	10.4% 	20.6 : 1
    # Three of a kind 	6,461,620 	4.83% 	15.3% 	19.7 : 1
    # Two pair 	31,433,400 	23.5% 	38.8% 	3.26 : 1
    # One pair 	58,627,800 	43.8% 	82.6% 	1.28 : 1
    # No pair 	23,294,460 	17.4%

    expected = [17.4, 43.8, 23.5, 4.83, 4.62, 3.03, 2.60, 0.168, 0.0311]

    dealer = Dealer([])
    hand = Hand()
    board = Board()

    frequencies = np.zeros(9, dtype=int)

    nb_draws = 1e7

    for i in range(int(nb_draws)):
        hand.distribute(dealer)
        board.flop(dealer)
        board.turn(dealer)
        board.river(dealer)

        showdown = Showdown(hand, board)
        frequencies[showdown.get_rank()-1] += 1

        hand.reset()
        board.reset()
        dealer.reset()

        if (i % (nb_draws / 100)) == 0:
            print(str(i * 100 / nb_draws) + "%" )

    frequencies = frequencies / nb_draws *100

    for index, rank in enumerate(Showdown.RANKS):
        print(rank, ' -> computed probability:', frequencies[index], '(target: ' + str(expected[index]) + ')')










if __name__ == '__main__':
    can_draw_board()
    can_showdown()
    can_identify_ranks_accurately()
