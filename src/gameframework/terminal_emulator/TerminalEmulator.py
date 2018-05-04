from gameframework import *
from .TerminalPlayer import TerminalPlayer

class TerminalEmulator:

    def launch(self):
        self.welcome_message()
        game_master = self.create_game_master()
        print(game_master)

        continue_flag = True
        while continue_flag:
            print("\n\n----- Collecting blinds -----\n\n")
            game_master.collect_blinds()
            print(game_master)

            print("\n\n----- Hands -----\n\n")
            game_master.distribute_hands()
            print(game_master)
            game_master.bet_round()
            print(game_master)

            print("\n\n----- Flop -----\n\n")
            game_master.flop()
            print(game_master)
            game_master.bet_round()
            print(game_master)

            print("\n\n----- Turn -----\n\n")
            game_master.turn()
            print(game_master)
            game_master.bet_round()
            print(game_master)

            print("\n\n----- River -----\n\n")
            game_master.river()
            print(game_master)
            game_master.bet_round()
            print(game_master)

            print("\n\n----- Game finished -----\n\n")

            continue_answer = input("Do you wanna play another dealer? (yes/no): \n> ")
            while continue_answer != "yes" and continue_answer != "no":
                print("Please answer by yes or no")
                continue_answer = input("Do you wanna play another dealer? (yes/no): \n> ")

            if continue_answer == "no":
                continue_flag = False
            else:
                print("\n\n----- Dealer restarting -----\n\n")
                game_master.restart()
                print(game_master)

        print("\n\n----- Dealer exiting -----\n\n")


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

    def create_game_master(self):
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

        return GameMaster(players_list)

        print("\n\n----- Dealer created -----\n\n")
