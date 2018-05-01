


import gameframework


class TerminalPlayer(gameframework.Player):


    def ask_action(self, game):
        """
        Method that triggers a prompt in the terminal to ask what the human player wants
        to do.

        Parameters
        ----------
        game : Game
            Game object representing the game the player is playing at.
            It is used as argument to inform the Player of its environment so
            that she can take a decision.

        Returns
        -------
        str
            A string defining the action that has been chosen.
            It has to be one of those: 'check', 'fold', 'call' or 'raise'
        """

        if not isinstance(game, gameframework.Game):
            raise WrongTypeError("You have to provide a Game object when calling the Player's ask action method.")
        print(self)
        next_action = input("Choose an action: ")
        while next_action not in self.ACTIONS:
            print("Please choose one of the following actions: 'check', 'fold', 'call' or 'raise'")
            next_action = input("Choose an action: ")

        self.__next_action = next_action

        print()
        return next_action



    def verbose(self):
        raise Exception("Not implemented")
