


from gameframework import Dealer, Player, WrongTypeError


class TerminalPlayer(Player):


    def ask_action(self, dealer):
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
        if not isinstance(dealer, Dealer):
            raise WrongTypeError("You have to provide a Dealer object when calling the Player's ask action method.")
        print(self)
        next_action = input("Choose an action: ")
        while next_action not in self.ACTIONS:
            print("Please choose one of the following actions: 'check', 'fold', 'call' or 'raise'")
            next_action = input("Choose an action: ")

        self._next_action = next_action
        return next_action
