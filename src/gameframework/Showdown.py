
import copy
import numpy as np
from .Hand import Hand
from .Board import Board
from .Error import PokerError



class Showdown:
    """
    Takes a hand and a board and characterize the strength of the combination
    by identifying its rank and the kickers (an array of 5 cards)
    Later on when we will want to compare hands: the one with the greatest rank wins
    and if hands have equal rank they are differentiated by comparing one by one
    the kickers until finding one that can differentiate the two players.
    The kicker with the highest value determining the winner of the confrontation.
    """

    RANKS = ['high card', 'pair', 'two pair', 'three of a kind', 'straight', \
                'flush', 'full house', 'four of a kind', 'straight flush']


    def __init__(self, hand_cards, board_cards):
        if len(hand_cards) != 2:
            raise InvalidArgumentError('Trying to construct a Showdown object with\
                                        a hand that is not of length 2.')
        if len(board_cards) != 5:
            raise WrongTypeError('Trying to construct a Showdown object with a\
                                    board that is not of length 5.')
        if None in board_cards:
            raise PokerError("Trying to construct a Showdown with undefined cards\
                                for board.")

        self.__hand = hand_cards
        self.__board = board_cards

        self.__cards = sorted(hand_cards + board_cards)




    def __repr__(self):
        return self.__cards.__repr__()


    # ranks
    # 9: straight flush
    # 8: four of a kind
    # 7: full house
    # 6: flush
    # 5: straight
    # 4: three of a kind
    # 3: two pairs
    # 2: pair
    # 1: high card
    def characterize(self):
        """
        Return a tuple with the first argument being the rank of the hand and the
        second one being a numpy array of length 5 representing the 5 kickers of
        the hand.
        """
        value_array = np.array(list(map(lambda x: x.value, self.__cards)))
        suit_array = np.array(list(map(lambda x: x.suit, self.__cards)))
        value_bins = np.bincount(value_array, minlength=14)

        # Two lists used to keep highest value of successive cards and the count of successive cards
        straight__flush__current_value = [0 for i in range(4)]
        straight__flush__count = [0 for i in range(4)]

        # suit_count is only used to spot a flush later
        # Each entry counts the number of cards encountered in each suit
        suit_count = np.zeros(4)

        # go through showdown's cards to check straight flush and plain flush
        for card in self.__cards:
            suit = card.suit

            # checking straight flush
            current_value = card.value
            if straight__flush__current_value[suit-1] == 0:
                straight__flush__current_value[suit-1] = current_value
                straight__flush__count[suit-1] = 1
            elif current_value == straight__flush__current_value[suit-1] + 1:
                straight__flush__current_value[suit-1] = current_value
                straight__flush__count[suit-1] += 1
            else:
                straight__flush__current_value[suit-1] = current_value
                straight__flush__count[suit-1] = 1

            if straight__flush__count[suit-1] >= 5:
                values_ans = np.zeros(5)
                values_ans[0] = straight__flush__current_value[suit-1]

                return np.append(np.array(9), values_ans)

            # suit_count is only used to spot a flush later
            suit_count[suit-1] += 1



        # intermediary step: check three of a kind and pairs
        four__of__a__kind__value = np.where(value_bins==4)[0]
        three_of_a_kind_value = np.where(value_bins==3)[0]
        pair_values = np.where(value_bins==2)[0]

        # check four of a kind
        if len(four__of__a__kind__value) != 0:
            values_ans = np.zeros(5)
            values_ans[0] = four__of__a__kind__value[0]

            # spotting the kicker
            if self.__cards[-1].value == four__of__a__kind__value[0]:
                kicker__value = self.__cards[-2].value
            else:
                kicker__value = self.__cards[-1].value
            values_ans[1] = kicker__value
            return np.append(np.array(8), values_ans)



        # check full house
        if len(three_of_a_kind_value) != 0 and len(pair_values) != 0:
            values_ans = np.zeros(5)
            values_ans[0] = three_of_a_kind_value[0]
            values_ans[1] = pair_values[-1]
            return np.append(np.array(7), values_ans)

        # check flush
        flush_finder = np.where(suit_count >= 5)[0]
        if len(flush_finder) != 0:
            suit_flush = flush_finder[0] + 1
            flush_values = value_array[np.where(suit_array == suit_flush)]
            values_ans = flush_values[-5:][::-1]
            return np.append(np.array(6), values_ans)



        # check straight
        if value_bins[-1] > 0:
            straight_value = 13
            straight_count = 1
            max_straight_count = 1
            max_straight_value = 0
        else:
            straight_value = 0
            straight_count = 0
            max_straight_count = 0
            max_straight_value = 0
        for i in range(1, value_bins.shape[0]):
            current_value = i
            if value_bins[i] > 0:
                if straight_value == 0:
                    straight_value = current_value
                    straight_count += 1
                elif current_value == straight_value % 13 + 1:
                    straight_value = current_value
                    straight_count += 1
                    if straight_count > max_straight_count:
                        max_straight_count = straight_count
                        max_straight_value = straight_value
                else:
                    straight_value = current_value
                    straight_count = 1

        if max_straight_count >= 5:
            values_ans = np.zeros(5)
            values_ans[0] = max_straight_value
            return np.append(np.array(5), values_ans)

        # check three of a kind
        if len(three_of_a_kind_value) != 0:
            values_ans = np.zeros(5)
            values_ans[0] = three_of_a_kind_value[-1]

            first_kicker_found = False
            for index in range(13, -1, -1):
                if value_bins[index] != 0 and index != three_of_a_kind_value[-1]:
                    if value_bins[index] > 1:
                        values_ans[1] = index
                        values_ans[2] = index
                        return np.append(np.array(4), values_ans)
                    if value_bins[index] == 1 and first_kicker_found == False:
                        values_ans[1] = index
                        first_kicker_found = True
                    else:
                        values_ans[2] = index
                        return np.append(np.array(4), values_ans)

        # check two pair
        if len(pair_values) >= 2:
            values_ans = np.zeros(5)
            values_ans[0] = pair_values[-1]
            values_ans[1] = pair_values[-2]

            # spotting the kicker
            for index in range(13, -1, -1):
                if index != pair_values[-1] and index != pair_values[-2]:
                    values_ans[2] = index
                    return np.append(np.array(3), values_ans)

        # check one pair
        if len(pair_values) == 1:
            values_ans = np.zeros(5)
            values_ans[0] = pair_values[0]

            # spotting the kickers
            # in this situation we know that there are only one pair amongst the
            # 7 cards of the showdown therefore no need to worry about the multiplicity
            # about the card's value when looking for the kickers
            nb_kickers_found = 0
            for index in range(13, -1, -1):
                if index != pair_values[0] and nb_kickers_found < 3:
                    nb_kickers_found += 1
                    values_ans[nb_kickers_found] = index
            return np.append(np.array(2), values_ans)

        return np.append(np.array(1), value_array[-5:][::-1])








    def compress(self):
        sort_hand = sorted(self.__hand)
        sort_board = sorted(self.__board)
        concat = copy.deepcopy(sort_hand + sort_board)

        # suit_refs contains
        suit_converter = {1: None, 2: None, 3: None, 4: None}

        count_new_suits = 1
        for card in concat:
            suit = card.suit
            if suit_converter[suit] == None:
                suit_converter[suit] = count_new_suits
                card.suit = count_new_suits
                count_new_suits += 1
            else:
                card.suit = suit_converter[suit]

        return concat
