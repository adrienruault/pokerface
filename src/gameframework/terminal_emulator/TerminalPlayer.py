import os
from gameframework import Dealer, Player, WrongTypeError


class TerminalPlayer(Player):


    def ask_action(self, game_master):
        """
        Method that triggers a prompt in the terminal to ask what the human player wants
        to do.

        Parameters
        ----------
        dealer : Dealer
            Dealer object representing the dealer the player is playing at.
            It is used as argument to inform the Player of its environment so
            that she can take a decision.

        Returns
        -------
        str
            A string defining the action that has been chosen.
            It has to be one of those: 'check', 'fold', 'call' or 'raise'
        """
        if not isinstance(game_master, Dealer):
            raise WrongTypeError("You have to provide a Dealer object when calling the Player's ask action method.")

        # Clear terminal and asking for taking turn
        os.system('cls' if os.name == 'nt' else 'tput reset')
        print("It's " + self.id + "'s turn.")
        print("Press enter when you want to take your turn...")
        input()

        # Clear terminal and asking for new action
        os.system('cls' if os.name == 'nt' else 'tput reset')

        print(game_master)
        print()
        print("Your turn:")
        print(self)
        next_action = input("Choose an action: ")
        while next_action not in self.ACTIONS:
            print("Please choose one of the following actions: 'check', 'fold', 'call' or 'raise'")
            next_action = input("Choose an action: ")

        while (next_action == "check"
                and abs(game_master.target_bet - self.current_bet) > 1e-3):
            print("It is not allowed to 'check' in this situation")
            next_action = input("Choose an action: ")

        self._played_action = next_action

        print()
        print("Your action has been taken into account.")
        print("Press enter to let your neighbor play...")
        input()
        return next_action
