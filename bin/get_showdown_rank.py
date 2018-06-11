import sys

#print(sys.path)

sys.path.append(sys.path[0] + '/../src')

from gameframework import *



def main():

    print("Provide all cards in R-S format")
    print("Provide a hand:")

    hand = []
    b = input("Card1: ")
    hand += [Card.create_from_string(b)]
    hand += [Card.create_from_string(input("Card2: "))]

    print("Provide a board:")
    board = []
    board += [Card.create_from_string(input("Card1: "))]
    board += [Card.create_from_string(input("Card2: "))]
    board += [Card.create_from_string(input("Card3: "))]
    board += [Card.create_from_string(input("Card4: "))]
    board += [Card.create_from_string(input("Card5: "))]

    print("board len", len(board))
    showdown = Showdown(hand, board)

    string_rank = showdown.get_string_rank()
    print("Rank:", string_rank)


if __name__ == "__main__":
    print(sys.argv[0])
    main()
