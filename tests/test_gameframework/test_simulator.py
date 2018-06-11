


from gameframework import *


def initialize():

    simulator = Simulator()

    hand, board, card_pack = simulator.draw_game_situation()

    return simulator, hand, board, card_pack




def test_generate_random_head_to_head_from_river():
    simulator, hand, board, card_pack = initialize()
    tol = 1e-1

    p_win, confwin, p_draw, confdraw = simulator.simulate_random_head_to_head(tol, hand, board,
                                                     card_pack)

    assert board.stage == 0
    assert confwin < tol
    assert confdraw < tol
    assert len(card_pack.drawn_cards) == 2
    assert (p_win >= 0) and (p_win <= 1)
    assert (p_draw >= 0) and (p_draw <= 1)


def test_generate_random_head_to_head_from_turn():
    simulator, hand, board, card_pack = initialize()
    tol = 1e-1

    board.next_stage()

    p_win, confwin, p_draw, confdraw = simulator.simulate_random_head_to_head(tol, hand, board,
                                                     card_pack)
    assert board.stage == 1
    assert confwin < tol
    assert confdraw < tol
    assert len(card_pack.drawn_cards) == 5
    assert (p_win >= 0) and (p_win <= 1)
    assert (p_draw >= 0) and (p_draw <= 1)


def test_generate_random_head_to_head_from_flop():
    simulator, hand, board, card_pack = initialize()
    tol = 1e-1

    for i in range(2):
        board.next_stage()

    p_win, confwin, p_draw, confdraw = simulator.simulate_random_head_to_head(tol, hand, board,
                                                     card_pack)

    assert board.stage == 2
    assert confwin < tol
    assert confdraw < tol
    assert len(card_pack.drawn_cards) == 6
    assert (p_win >= 0) and (p_win <= 1)
    assert (p_draw >= 0) and (p_draw <= 1)


def test_generate_random_head_to_head_from_scratch():
    simulator, hand, board, card_pack = initialize()
    tol = 1e-1

    for i in range(3):
        board.next_stage()

    p_win, confwin, p_draw, confdraw = simulator.simulate_random_head_to_head(tol, hand, board,
                                                     card_pack)

    assert board.stage == 3
    assert confwin < tol
    assert confdraw < tol
    assert len(card_pack.drawn_cards) == 7
    assert (p_win >= 0) and (p_win <= 1)
    assert (p_draw >= 0) and (p_draw <= 1)
