from pieces import *
from agent import Agent


def scoreEvaluationFunction(game, color):
    """
    Evaluation function which evaluates moves based on material.
    :param game: a ChessGame
    :param color: the color making the move
    :return: the evaluated score
    """
    score = 0
    if color == Color.WHITE:
        for blackPiece in game.capturedBlackPieces:
            score += blackPiece.getPointVal()
        for whitePiece in game.capturedWhitePieces:
            score -= whitePiece.getPointVal()
    else:
        for whitePiece in game.capturedWhitePieces:
            score += whitePiece.getPointVal()
        for blackPiece in game.capturedBlackPieces:
            score -= blackPiece.getPointVal()
    return score


def positionEvaluationFunction(game, color):
    """
    Evaluation function which evaluates moves based on board position.
    :param game: a ChessGame
    :param color: the color making the move
    :return: the evaluated score
    """
    score = 0
    for x in range(8):
        for y in range(8):
            piece = game.board[x][y]
            if piece != 0:
                if piece.getColor() == color:
                    # prioritize controlling the middle
                    if ((piece.canMoveTo((3, 3), game.board)
                         and game.isNothingBlocking((x, y), (3, 3)))
                        or (piece.canMoveTo((3, 4), game.board)
                            and game.isNothingBlocking((x, y), (3, 4)))
                        or (piece.canMoveTo((4, 3), game.board)
                            and game.isNothingBlocking((x, y), (4, 3)))
                        or (piece.canMoveTo((4, 4), game.board)
                            and game.isNothingBlocking((x, y), (4, 4)))):
                        score += 100
                    # control open squares
                    for px in range(8):
                        for py in range(8):
                            if (piece.canMoveTo((px, py), game.board)
                                and game.isNothingBlocking((x, y), (px, py))):
                                score += 1
    return score


def kingEvaluationFunction(game, color):
    """
    Evaluation function which evaluates moves based on king safety.
    :param game: a ChessGame
    :param color: the color making the move
    :return: the evaluated score
    """
    castleToY = 0
    oppColor = Color.BLACK
    if color == Color.BLACK:
        castleToY = 7
        oppColor = Color.WHITE

    score = 0
    # castle early
    if (game.board[2][castleToY].getPiece() == ChessPiece.KING
        or game.board[6][castleToY].getPiece() == ChessPiece.KING):
        score += 10
    # reduce the number of checks (encourage blocking)
    kx, ky = game.findPiece(ChessPiece.KING, color)
    king = game.board[kx][ky]
    numberOfChecks = 0
    for x in range(8):
        for y in range(8):
            opp = game.board[x][y]
            if (opp.getColor() == oppColor
                and opp.canMoveTo((kx, ky), game.board)
                and game.board.isNothingBlocking((x, y), (kx, ky))):
                numberOfChecks += 1
    if numberOfChecks != 0:
        score -= 100
    return score


def combinedEvaluationFunction(game, color):
    score = (kingEvaluationFunction(game, color)
             + positionEvaluationFunction(game, color)
             + scoreEvaluationFunction(game, color))
    return score


class MinimaxAgent(Agent):
    """
    A MinimaxAgent is an agent which uses the minimax algorithm with
    alpha-beta pruning that, given an evaluation function, determines the
    best move for a given color to make in a game of chess.

    :param game: a ChessGame to run the agent on
    :param startColor: the color that the agent will choose moves for
    :param evalFn: the evaluation function name
    :param depth: the depth to search moves
    """
    def __init__(self, game, startColor, evalFn='combinedEvaluationFunction',
                 depth='2'):
        super().__init__(game, startColor)
        self.evaluationFunction = globals()[evalFn]
        self.depth = int(depth)

    def getAction(self):
        """
        Gets the best action for the player to take.
        :return: the action
        """
        def maxValue(state, depth, alpha, beta, colorIndex):
            # max part of minimax
            color = colors[colorIndex % 2]
            if state.isWin(color) or state.isLose(color) or depth == maxDepth:
                return self.evaluationFunction(state, color)
            v = float("-inf")
            for move in state.getLegalMoves(color):
                v = max(v, minValue(state.generateSuccessor(color, move),
                                    depth, alpha, beta, colorIndex + 1))
                if v > beta:
                    return v
                alpha = max(alpha, v)
            return v

        def minValue(state, depth, alpha, beta, colorIndex):
            # min part of minimax
            color = colors[colorIndex % 2]
            if state.isWin(color) or state.isLose(color) or depth == maxDepth:
                return self.evaluationFunction(state, color)
            v = float("inf")
            legalMoves = state.getLegalMoves(color)
            for move in legalMoves:
                v = min(v, maxValue(state.generateSuccessor(color, move),
                                    depth + 1, alpha, beta, colorIndex + 1))
                if v < alpha:
                    return v
                beta = min(beta, v)
            return v

        colors = [Color.WHITE, Color.BLACK]
        cIndex = 1
        if self.startColor == Color.WHITE:
            cIndex = 0
        maxDepth = self.depth
        legalMoves = self.game.getLegalMoves(colors[cIndex])
        bestAction = ((0, 0), (0, 1))
        score = float("-inf")
        alpha = float("-inf")
        beta = float("inf")
        for move in legalMoves:
            previousScore = score
            score = max(score,
                        minValue(
                            self.game.generateSuccessor(colors[cIndex], move),
                            0, alpha, beta, cIndex + 1)
                        )
            if score > previousScore:
                bestAction = move
            alpha = max(alpha, score)
        return bestAction
