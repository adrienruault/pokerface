
import math
import copy

import numpy as np

from .Player import Player
from .CardPack import CardPack
from .Hand import Hand
from .Referee import Referee
from .Board import Board
from .Showdown import Showdown




class Simulator:


    def __draw_end_game_situation(self):
        card_pack = CardPack([])

        hand = Hand(card_pack)
        hand.receive_cards()

        board = Board(card_pack)
        board.flop()
        board.turn()
        board.river()

        return hand, board, card_pack



    def simulate_head_to_head(self, nb_simu = 1000):
        hand, board, card_pack = self.__draw_end_game_situation()

        drawn_cards_ref = card_pack.drawn_cards

        referee = Referee()

        victory_array = np.zeros(nb_simu)
        for i in range(nb_simu):
            drawn_cards = list(drawn_cards_ref)
            # create card_pack thet inherits the cards that have already been drawn
            card_pack = CardPack(drawn_cards)


            opponent_hand = Hand(card_pack)
            opponent_hand.receive_cards()

            winner_ids = referee.arbitrate([hand, opponent_hand], board)
            if 0 in winner_ids:
                victory_array[i] = 1


        p_hat = np.mean(victory_array)
        # See https://www.youtube.com/watch?v=ESKpJi2vLCw for variance of the
        # Bernoulli estimator p hat
        var_p_hat = p_hat * (1 - p_hat) / nb_simu
        std = np.sqrt(var_p_hat)

        return hand, board, p_hat, std
