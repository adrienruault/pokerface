

import copy
import numpy as np
from .Showdown import Showdown



class Referee:


    def arbitrate(self, players_dict, board):
        if board.stage != 3:
            raise PokerError("Trying to get the winner of a Table with a Board object that haven't passed river")

        # Creating Showdown objects for each (player, board) pair and appending their
        # rank_array to the rank_matrix that will be used in the get_winner method
        rank_matrix = np.zeros((len(players_dict), 6))
        nb_players_in_game = 0
        players_list = list(players_dict.values())
        for i, player in enumerate(players_list):
            if player.playing_flag == True:
                showdown = Showdown(player.hand, board)
                rank_matrix[i, :] = showdown.rank_array
                nb_players_in_game += 1

        players_id_list = list(players_dict.keys())

        # Best Player identification
        in_course_idx = np.arange(0, rank_matrix.shape[0], dtype=int)
        winner_found = False
        i = 0
        while winner_found == False and i < 6:
            max_value = np.max(rank_matrix[in_course_idx, i])
            in_course_idx = np.where(rank_matrix[in_course_idx, i] == max_value)[0]

            if len(in_course_idx) == 1:
                winner_found = True
            i+=1

        winner_ids = [players_id_list[i] for i in in_course_idx]

        return winner_ids
