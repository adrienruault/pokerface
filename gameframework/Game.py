

from .Dealer import Dealer
from .Board import Board

class Game:

    def __init__(self, players_list):
        self.__players_list = players_list
        self.__dealer =  Dealer()
        self.__board = Board(self.dealer)

    @property
    def dealer(self):
        return self.__dealer

    @property
    def players_list(self):
        return self.__players_list

    @property
    def board(self):
        return self.__board





    def get_winner(self):
        if self.__table.board.stage != 3:
            raise PokerError("Trying to get the winner of a Table with a Board object that haven't passed river")

        rank_matrix = np.zeros((len(self.__players_list), 6))

        for i, player in enumerate(self.__players_list):
            if type(player) is not Player:
                raise WrongTypeError('Trying to construct a Referee object with a list that does not contain only players')

            # Construct the showdown related to the current player and add it to
            # the list of showdowns
            showdown = Showdown(player.get_hand(), board)
            rank_matrix[i, 0] = showdown.get_rank()
            rank_matrix[i, 1:] = showdown.get_kickers()

        # Now I need to identify the best Player
        winner_found = True
        i = 0
        while winner_found == False and i < 6:
            max_value = np.max(rank_matrix[:, i])
            best_players = np.where(rank_matrix[:,i] == max_value)

            # We restrict the rank_matrix to the set of still potential winners
            rank_matrix = rank_matrix[best_players,:]
            if len(best_players) == 1:
                winner_found = True
            i+=1

        self.__last_winner_id = best_players

        return best_players
