

from .Showdown import Showdown






class Referee:


    def __init__(self, players_list, board):
        if type(board) is not Board:
            raise WrongTypeError('Trying to construct a Showdown object without a Board object')
        if board.get_turn() != 3:
            raise PokerError("Trying to construct a Showdown object with a Board object that haven't passed river")

        showdowns_list = []
        best_player_idx = []
        max_rank = -1

        for idx, player in enumerate(players_list):
            if type(player) is not Player:
                raise WrongTypeError('Trying to construct a Referee object without a players_list')

            current_showdown = Showdown(player.get_hand(), board)
            showdowns_list += [current_showdown]
            current_rank = current_showdown.get_rank()

            if current_rank > max_rank:
                best_player_idx = [idx]
                max_rank = current_rank
            elif current_rank == max_rank:
                best_player_idx += [idx]
                best_showdowns_list += [current_showdown]
