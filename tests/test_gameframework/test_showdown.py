

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

    card_pack = CardPack([])
    hand = Hand(card_pack)
    board = Board(card_pack)

    frequencies = np.zeros(9, dtype=int)

    nb_draws = int(1e4)

    for i in range(nb_draws):
        hand.receive_cards()
        board.flop()
        board.turn()
        board.river()

        showdown = Showdown(hand, board)
        frequencies[showdown.rank-1] += 1

        hand.reset()
        board.reset()
        card_pack.reset()

        if (i % (nb_draws / 10)) == 0:
            print(str(i * 100 / nb_draws) + "%" )

    frequencies = frequencies / nb_draws

    print("Number of cards drawn:", nb_draws)
    for index, rank in enumerate(Showdown.RANKS):
        assert abs(frequencies[index] - expected[index]) < 0.01







def test_can_compress():

    hand = Hand(None)
    board = Board(None)

    hand.cards[0] = Card(10, 3)
    hand.cards[1] = Card(7, 1)

    board.cards[0] = Card(2, 1)
    board.cards[1] = Card(3, 4)
    board.cards[2] = Card(1, 1)
    board.cards[3] = Card(2, 4)
    board.cards[4] = Card(13, 2)

    board.stage = 3

    showdown = Showdown(hand, board)

    concat = showdown.compress()

    assert concat[0].value == 7 and concat[0].suit == 1
    assert concat[1].value == 10 and concat[1].suit == 2
    assert concat[2].value == 1 and concat[2].suit == 1
    assert concat[3].value == 2 and concat[3].suit == 1
    assert concat[4].value == 2 and concat[4].suit == 3
    assert concat[5].value == 3 and concat[5].suit == 3
    assert concat[6].value == 13 and concat[6].suit == 4
