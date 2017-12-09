

class Agent:
    """
    An Agent that can return a legal chess action for the user or AI to take.

    :param game: a ChessGame to run the agent on
    :param startColor: the color that the agent will choose moves for
    """
    def __init__(self, game, startColor):
        self.game = game
        self.startColor = startColor

    def printBoard(self):
        """ Prints the game board. """
        self.game.printBoard()

    def movePiece(self, moveFrom, moveTo, color):
        """
        Moves the piece at moveFrom to moveTo.

        :param moveFrom: the position of the piece to move
        :param moveTo: the position to move the piece to
        :param oppColor: the color of the opponent
        """
        self.game.movePiece(moveFrom, moveTo, color)

    def getAction(self):
        """
        Gets the best action for the player to take.
        :return: the action
        """
        return (0, 0), (0, 0)
