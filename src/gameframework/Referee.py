

import copy
import numpy as np
from .Showdown import Showdown



class Referee:


    def arbitrate(self, competing_hands, board):
        if board.stage != 3:
            raise PokerError("Trying to get the winner of a Table with a Board object that haven't passed river")

        nb_hands = len(competing_hands)

        # Creating Showdown objects for each (player, board) pair and appending their
        # rank_array to the rank_matrix that will be used in the get_winner method
        rank_matrix = np.zeros((nb_hands, 6))

        for i, hand in enumerate(competing_hands):
            showdown = Showdown(hand, board)
            rank_matrix[i, :] = showdown.characterize()

        # hands that are still potential winners
        in_course_idx = np.arange(0, rank_matrix.shape[0], dtype=int)

        # set of all ids
        set_ids = set(range(nb_hands))

        i = 0
        while i < 6:
            # Getting max current value
            # then getting the indices that correspond to that values
            #
            max_value = np.max(rank_matrix[:, i])
            in_course_idx = np.where(rank_matrix[:, i] == max_value)[0]
            excluded_idx = list(set_ids - set(in_course_idx))

            rank_matrix[excluded_idx, :] = np.zeros(shape=(len(excluded_idx), 6)) - 1
            #rank_matrix = rank_matrix[in_course_idx, :]

            if len(in_course_idx) == 1:
                break
            i+=1

        #winner_ids = [players_id_list[i] for i in in_course_idx]

        return in_course_idx
