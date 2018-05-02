

from gameframework import *




def test_can_identify_ranks_accurately():
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

    expected = [0.174, 0.438, 0.235, 0.0483, 0.0462, 0.0303, 0.0260, 0.00168, 0.0000311]

    dealer = Dealer([])
    hand = Hand(dealer)
    board = Board(dealer)

    frequencies = np.zeros(9, dtype=int)

    nb_draws = int(1e4)

    for i in range(nb_draws):
        hand.receive_cards()
        board.flop()
        board.turn()
        board.river()

        showdown = Showdown(hand, board)
        frequencies[showdown.rank-1] += 1

        hand.reset_cards()
        board.reset()
        dealer.reset()

        if (i % (nb_draws / 10)) == 0:
            print(str(i * 100 / nb_draws) + "%" )

    frequencies = frequencies / nb_draws

    print("Number of cards drawn:", nb_draws)
    for index, rank in enumerate(Showdown.RANKS):
        assert abs(frequencies[index] - expected[index]) < 0.01
