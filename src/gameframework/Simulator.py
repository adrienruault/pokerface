
import math
import copy
from datetime import datetime

import numpy as np
import pandas as pd

from .Player import Player
from .CardPack import CardPack
from .Hand import Hand
from .Referee import Referee
from .Board import Board
from .Showdown import Showdown




class Simulator:



    def generate_training_set(self, nb_trainings, verbose = True):
        """
        Outputs a dataframe with the winning probabilities given a game situation
        that is: a hand and a board.
        """

        columns = ['hand_c1', 'hand_c2',\
                     'board_c1', 'board_c2', 'board_c3',\
                     'board_c4', 'board_c5',\
                     'winning_proba', 'confidence95']

        train_set = []
        nb_simu = 1000
        for i in range(nb_trainings):
            game, win_prob, conf95 = self.simulate_random_head_to_head(
                                                                    nb_simu,
                                                                    board_stage=3)
            if verbose == True and i%10 == 0:
                date = datetime.now()
                string_date = "[%02d:%02d:%02d]" % (date.hour, date.minute, date.second)
                print(string_date, "generated ", i, "trainings")
            line = game + [win_prob] + [conf95]
            train_set += [line]

        return pd.DataFrame(train_set, columns=columns)












    def simulate_random_head_to_head(self, nb_simu, board_stage):
        """
        This methods randomly picks up a game situuation in head to head and then
        simulate #nb_simu games to estimate the winning probability for the player
        in the game situation.
        """
        hand, board_ref, card_pack_ref = self.__draw_game_situation(board_stage)

        drawn_cards_ref = card_pack_ref.drawn_cards

        referee = Referee()

        victory_array = np.zeros(nb_simu)


        for i in range(nb_simu):
            # create card_pack thet inherits the cards that have already been drawn
            drawn_cards = list(drawn_cards_ref)
            card_pack = CardPack(drawn_cards)

            board = Board(card_pack)
            board.cards = list(board_ref.cards)
            board.stage = board_stage

            for i in range(3, board_stage, -1):
                board.next_stage()

            # Create an opponent hand
            opponent_hand = Hand(card_pack)
            opponent_hand.receive_cards()

            winner_ids = referee.arbitrate([hand, opponent_hand], board)
            if 0 in winner_ids:
                victory_array[i] = 1


        p_hat = np.mean(victory_array)
        # See https://www.youtube.com/watch?v=ESKpJi2vLCw for variance of the
        # Bernoulli estimator p hat
        var_p_hat = p_hat * (1 - p_hat) / nb_simu
        std_hat = np.sqrt(var_p_hat)

        # width of the confidence interval at 95%
        width_conf_interval = 2 * 1.96 * std_hat / np.sqrt(nb_simu)


        showdown = Showdown(hand, board)
        compressed_list = showdown.compress()
        return compressed_list, p_hat, width_conf_interval







    def __draw_game_situation(self, board_stage):

        card_pack = CardPack([])

        hand = Hand(card_pack)
        hand.receive_cards()

        board = Board(card_pack)

        for i in range(board_stage):
            board.next_stage()

        return hand, board, card_pack
