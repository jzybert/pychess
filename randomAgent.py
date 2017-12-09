import random
from agent import Agent


class RandomAgent(Agent):
    """
    A RandomAgent is an agent that randomly chooses a legal move to make.

    :param game: a ChessGame to run the agent on
    :param startColor: the color that the agent will choose moves for
    """
    def __init__(self, game, startColor):
        super().__init__(game, startColor)

    def getAction(self):
        """
        Randomly chooses a legal action
        :return: the action
        """
        legalMoves = self.game.getLegalMoves(self.startColor)
        return random.choice(legalMoves)
