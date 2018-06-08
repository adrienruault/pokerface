


from gameframework import *


def initialize():

    simulator = Simulator()

    hand, board, card_pack = simulator.draw_game_situation()

    return simulator, hand, board, card_pack




def test_generate_random_head_to_head_from_river():
    simulator, hand, board, card_pack = initialize()
    tol = 1e-1

    p, conf = simulator.simulate_random_head_to_head(tol, hand, board,
                                                     card_pack)

    assert board.stage == 0
    assert conf < tol
    assert len(card_pack.drawn_cards) == 2
    assert (p >= 0) and (p <= 1)


def test_generate_random_head_to_head_from_turn():
    simulator, hand, board, card_pack = initialize()
    tol = 1e-1

    board.next_stage()

    p, conf = simulator.simulate_random_head_to_head(tol, hand, board,
                                                     card_pack)
    assert board.stage == 1
    assert conf < tol
    assert len(card_pack.drawn_cards) == 5
    assert (p >= 0) and (p <= 1)


def test_generate_random_head_to_head_from_flop():
    simulator, hand, board, card_pack = initialize()
    tol = 1e-1

    for i in range(2):
        board.next_stage()

    p, conf = simulator.simulate_random_head_to_head(tol, hand, board,
                                                     card_pack)

    assert board.stage == 2
    assert conf < tol
    assert len(card_pack.drawn_cards) == 6
    assert (p >= 0) and (p <= 1)


def test_generate_random_head_to_head_from_scratch():
    simulator, hand, board, card_pack = initialize()
    tol = 1e-1

    for i in range(3):
        board.next_stage()

    p, conf = simulator.simulate_random_head_to_head(tol, hand, board,
                                                     card_pack)

    assert board.stage == 3
    assert conf < tol
    assert len(card_pack.drawn_cards) == 7
    assert (p >= 0) and (p <= 1)
