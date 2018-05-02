from gameframework import *
from .TerminalPlayer import TerminalPlayer

class TerminalEmulator:

    def __init__(self):
        pass

    def launch(self):

        self.welcome_message()
        self.create_game()
        print(self.__game)

        continue_flag = True
        while continue_flag:
            print("\n\n----- Collecting blinds -----\n\n")
            self.__game.collect_blinds()
            print(self.__game)

            print("\n\n----- Distributing hands -----\n\n")
            self.__game.distribute_hands()
            print(self.__game)

            if self.__game.state != "finished":
                print("\n\n----- Distributing flop -----\n\n")
                self.__game.flop()
                print(self.__game)

            if self.__game.state != "finished":
                print("\n\n----- Distributing turn -----\n\n")
                self.__game.turn()
                print(self.__game)

            if self.__game.state != "finished":
                print("\n\n----- Distributing river -----\n\n")
                self.__game.river()
                print(self.__game)

            print()
            print("Winners: ", self.__game.winner_ids)

            print("\n\n----- Game finished -----\n\n")

            continue_answer = input("Do you wanna play another game? (yes/no): \n> ")
            while continue_answer != "yes" and continue_answer != "no":
                print("Please answer by yes or no")
                continue_answer = input("Do you wanna play another game? (yes/no): \n> ")

            if continue_answer == "no":
                continue_flag = False
            else:
                print("\n\n----- Game restarting -----\n\n")
                self.__game.restart()
                print(self.__game)

        print("\n\n----- Game exiting -----\n\n")


    def welcome_message(self):
        print("Welcome to the pokerface emulator.")
        print("Follow the instructions to play through the terminal.")
        print("A GUI is in development.")
        print("You can see the project at https://github.com/adrienruault/pokerface.")
        print()

    def create_player(self):
        id_ = input("\tid: ")
        while id_ == '' or len(id_) > 12:
            print("Please provide an id with no more then 12 characters:")
            id_ = input("\tid: ")

        conversion_failed = False
        try:
            wallet = float(input("\twallet: "))
        except Exception:
            conversion_failed = True

        while conversion_failed or wallet < 0:
            print("Please provide a positive number for wallet")
            conversion_failed = False
            try:
                wallet = float(input("\twallet: "))
            except Exception:
                conversion_failed = True

        return TerminalPlayer(id_, wallet)

    def create_game(self):
        print("How many players are taking part?")
        nb_players = int(input("Please provide the number of players (can range from 2 to 8): "))

        while nb_players > 8 or nb_players < 2:
            print("The number of players is not valid.")
            nb_players = int(input("Please provide the number of players which can range from 2 to 8: "))


        players_list = []
        for i in range(nb_players):
            print("\nCreation of player " + str(i + 1) + ":")
            player = self.create_player()
            players_list += [player]

        self.__game = Game(players_list)

        print("\n\n----- Game created -----\n\n")


    def trigger_new_game(self):
        pass
