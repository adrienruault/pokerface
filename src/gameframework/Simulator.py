
import math
import copy
import sys
from datetime import datetime

import numpy as np
import pandas as pd

from gameframework import *





class Simulator:



    def generate_training_set(self, nb_trainings, verbose = True):
        """
        Outputs a dataframe with the winning probabilities given a game situation
        that is: a hand and a board.
        """

        columns = ['hand_c1', 'hand_c2',\
                     'board_c1', 'board_c2', 'board_c3',\
                     'board_c4', 'board_c5',\
                     'winprob1', 'drawprob1', 'confwin1', 'confdraw1',\
                     'winprob2', 'drawprob2', 'confwin2', 'confdraw2',\
                     'winprob3', 'drawprob3', 'confwin3', 'confdraw3',\
                     'winprob4', 'drawprob4', 'confwin4', 'confdraw4']

        train_set = []
        for i in range(nb_trainings):
            #print("training:", i)

            # The board output by draw_game_situation is an empty board
            # And it is filled up as we go through the coming loop
            hand, board, card_pack = self.draw_game_situation()

            results = []
            for j in range(4):
                #print("\tstage ->", j)
                win_prob, conf_win, draw_prob, conf_draw = self.simulate_random_head_to_head(
                                                        tol=1e-3,
                                                        hand=hand,
                                                        board_ref=board,
                                                        card_pack_ref=card_pack
                                                        )
                results +=  [win_prob] + [draw_prob] + [conf_win] + [conf_draw]

                if j < 3:
                    board.next_stage()


            if verbose == True and (i+1)%10 == 0:
                date = datetime.now()
                string_date = "[%02d:%02d:%02d]" % (date.hour, date.minute, date.second)
                print(string_date, "generated", i+1, "trainings")

            showdown = Showdown(hand.cards, board.cards)
            compressed_game = showdown.compress()

            line = compressed_game + results
            train_set += [line]

        if verbose == True:
            date = datetime.now()
            string_date = "[%02d:%02d:%02d]" % (date.hour, date.minute, date.second)
            print(string_date, "finished: generated", i+1, "trainings in total")

        return pd.DataFrame(train_set, columns=columns)












    def simulate_random_head_to_head(self, tol, hand, board_ref, card_pack_ref):
        """
        This methods takes as input a game situuation in head to head and then
        simulate #nb_simu games to estimate the winning probability for the player
        in the game situation.
        """
        board_stage_ref = board_ref.stage
        #print("\t\t", hand)
        #print("\t\t", board_ref)

        drawn_cards_ref = card_pack_ref.drawn_cards

        referee = Referee()

        nb_max_iter = int(1e5)
        test_var_every = 1000
        victory_array = np.zeros(nb_max_iter, dtype=np.int64)
        draw_array = np.zeros(nb_max_iter, dtype=np.int64)
        for i in range(nb_max_iter):
            # create card_pack thet inherits the cards that have already been drawn
            drawn_cards = list(drawn_cards_ref)
            card_pack = CardPack(drawn_cards)

            # create new board which is a copy of the board passed as input
            board = Board(card_pack)
            board.cards = list(board_ref.cards)
            board.stage = board_stage_ref

            # Draw the remaining cards to finish the game
            for j in range(board_stage_ref, 3):
                board.next_stage()

            # Create an opponent hand
            opponent_hand = Hand(card_pack)
            opponent_hand.receive_cards()

            winner_ids = referee.arbitrate([hand, opponent_hand], board)
            showdown1 = Showdown(hand.cards, board.cards)
            showdown2 = Showdown(opponent_hand.cards, board.cards)
            """
            print()
            print("Game:")
            print("me", hand)
            print("\t", showdown1.get_string_rank())
            print("\t", showdown1.characterize())
            print("opp", opponent_hand)
            print("\t", showdown2.get_string_rank())
            print("\t", showdown2.characterize())
            print("board", board)
            print("winners", winner_ids)
            """

            # First spotting if their is a draw and then checking
            # whether player 0 won
            if len(winner_ids) == 2:
                draw_array[i] = 1 # was 0.5
            elif 0 in winner_ids:
                victory_array[i] = 1

            #print("\t\t -> ", i)
            if (i+1) % test_var_every == 0:
                #print("\t\titer ->", i)
                # compute confidence interval of the winning probability estimator
                p_win_hat, win_confidence = self.compute_bernoulli_estimator(victory_array[:i])
                p_draw_hat, draw_confidence = self.compute_bernoulli_estimator(draw_array[:i])
                if win_confidence < tol and draw_confidence < tol:
                    break

        if i == nb_max_iter-1:
            p_win_hat, win_confidence = self.compute_bernoulli_estimator(victory_array)
            p_draw_hat, draw_confidence = self.compute_bernoulli_estimator(draw_array)

        return p_win_hat, win_confidence, p_draw_hat, draw_confidence



    def compute_bernoulli_estimator(self, bin_array):
        # compute confidence interval of the winning probability estimator
        p_hat = np.mean(bin_array)
        nb_simu = bin_array.shape[0]
        # See https://www.youtube.com/watch?v=ESKpJi2vLCw for variance of the
        # Bernoulli estimator p hat
        var_p_hat = p_hat * (1 - p_hat) / nb_simu
        std_hat = np.sqrt(var_p_hat)

        # width of the confidence interval at 95%
        width_conf_interval = 2 * 1.96 * std_hat / np.sqrt(nb_simu)

        return p_hat, width_conf_interval



    def draw_game_situation(self):

        card_pack = CardPack([])

        hand = Hand(card_pack)
        hand.receive_cards()

        board = Board(card_pack)

        #for i in range(3):
        #    board.next_stage()

        return hand, board, card_pack
