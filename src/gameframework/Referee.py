

import copy



class Referee:


    def __init__(self, players_dict, board):
        if board.stage != 3:
            raise PokerError("Trying to get the winner of a Table with a Board object that haven't passed river")

        # Creating Showdown objects for each (player, board) pair and appending their
        # rank_array to the rank_matrix that will be used in the get_winner method
        rank_matrix = np.zeros((len(players_dict), 6))
        nb_players_in_game = 0
        for i, player in enumerate(players_dict.items()):
            if player.playing_flag == True:
                showdown = Showdown(player.hand, board)
                rank_matrix[i, :] = showdown.rank_array
                nb_players_in_game += 1

        players_id_list = list(players_dict.keys())

        # Best Player identification
        in_course_idx = range(rank_matrix.shape[0])
        winner_found = False
        i = 0
        while winner_found == False and i < 6:
            max_value = np.max(rank_matrix[in_course_players_idx, i])
            in_course_idx = np.where(rank_matrix[in_course_idx, i] == max_value)

            if len(in_course_idx) == 1:
                winner_found = True
            i+=1

        self.__winner_ids = players_id_list[in_course_idx]


    @property
    def winner_ids(self):
        return self.__winner_ids
