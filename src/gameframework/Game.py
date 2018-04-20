

from .Dealer import Dealer
from .Board import Board
from .Hand import Hand
from .Error import *
import copy

class Game:

    def __init__(self, players_list):
        players_id_list = []
        self.__players_dict = {}

        for player in players_list:
            current_id = player.id
            if current_id in players_id_list:
                raise PokerError("Trying to instantiate a Game object with two players having the same id")
            self.__players_dict[current_id] = player
            players_id_list += [current_id]

        #self.__players_list = players_list
        self.__players_list = copy.deepcopy(players_list)
        self.__playing_order = players_id_list
        self.__dealer =  Dealer([])
        self.__board = Board(self.__dealer)
        self.__state = "start"
        self.__small_blind = 1.
        self.__pot = 0.

    @property
    def dealer(self):
        return self.__dealer

    @property
    def players_list(self):
        return self.__players_list

    @property
    def players_id(self):
        return self.__players_id

    @property
    def board(self):
        return self.__board

    @property
    def state(self):
        return self.__state




    def get_winner(self):
        if self.__board.stage != 3:
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


    def distribute_to_players(self):
        if self.__state != "start":
            raise PokerError("Trying to distribute cards to players in a game that is not in start state")

        for player in self.__players_list:
            hand = Hand(self.__dealer)
            hand.receive_cards()
            player.receive_hand(hand)

        self.__state = "pre-flop"


    def flop(self):
        if self.__state != "pre-flop":
            raise PokerError("Trying to distribute flop in a game that is not in pre-flop state")

        self.__board.flop()
        self.__state = "pre-turn"

    def turn(self):
        if self.__state != "pre-turn":
            raise PokerError("Trying to distribute turn in a game that is not in pre-turn state")

        self.__board.turn()
