from pieces import *


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
                if ((piece.canMoveTo((3, 3), game.board[3][3])
                     and game.isNothingBlocking((x, y), (3, 3)))
                    or (piece.canMoveTo((3, 4), game.board[3][4])
                        and game.isNothingBlocking((x, y), (3, 4)))
                    or (piece.canMoveTo((4, 3), game.board[4][3])
                        and game.isNothingBlocking((x, y), (4, 3)))
                    or (piece.canMoveTo((4, 4), game.board[4][4])
                        and game.isNothingBlocking((x, y), (4, 4)))):
                    score += 10
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
                and opp.canMoveTo((kx, ky), king)
                and game.board.isNothingBlocking((x, y), (kx, ky))):
                numberOfChecks += 1
    if numberOfChecks != 0:
        score -= 100
    return score


class MinimaxAgent:
    """
    A MinimaxAgent is an agent which uses the minimax algorithm with
    alpha-beta pruning that, given an evaluation function, determines the
    best move for a given color to make in a game of chess.

    :param game: a ChessGame to run the agent on
    :param startColor: the color that the agent will choose moves for
    :param evalFn: the evaluation function name
    :param depth: the depth to search moves
    """
    def __init__(self, game, startColor, evalFn='scoreEvaluationFunction',
                 depth='2'):
        self.evaluationFunction = globals()[evalFn]
        self.depth = int(depth)
        self.game = game
        self.startColor = startColor

    def printBoard(self):
        """ Prints the game board. """
        self.game.printBoard()

    def movePiece(self, moveFrom, moveTo, oppColor):
        """
        Moves the piece at moveFrom to moveTo.

        :param moveFrom: the position of the piece to move
        :param moveTo: the position to move the piece to
        :param oppColor: the color of the opponent
        """
        self.game.movePiece(moveFrom, moveTo, oppColor)

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
