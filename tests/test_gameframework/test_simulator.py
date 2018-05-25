


from gameframework import *





def test_generate_random_head_to_head_from_river():
    simulator = Simulator()

    cards, p, conf = simulator.simulate_random_head_to_head(10, 3)

    assert len(cards) == 7
    assert (p >= 0) and (p <= 1)


def test_generate_random_head_to_head_from_turn():
    simulator = Simulator()

    cards, p, conf = simulator.simulate_random_head_to_head(10, 2)

    assert isinstance(cards[6], Card)
    assert len(cards) == 7
    assert (p >= 0) and (p <= 1)

def test_generate_random_head_to_head_from_flop():
    simulator = Simulator()

    cards, p, conf = simulator.simulate_random_head_to_head(10, 1)

    assert isinstance(cards[5], Card)
    assert isinstance(cards[6], Card)
    assert len(cards) == 7
    assert (p >= 0) and (p <= 1)


def test_generate_random_head_to_head_from_scratch():
    simulator = Simulator()

    cards, p, conf = simulator.simulate_random_head_to_head(10, 0)

    assert isinstance(cards[2], Card)
    assert isinstance(cards[3], Card)
    assert isinstance(cards[4], Card)
    assert isinstance(cards[5], Card)
    assert isinstance(cards[6], Card)
    assert len(cards) == 7
    assert (p >= 0) and (p <= 1)
