from chess import *
from pieces import *

"""
Evaluation function which evaluates moves based on material gained/lost.
"""
def scoreEvaluationFunction(game, color):
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

"""
Evaluation function which evaluates moves based on board position.
"""
def positionEvaluationFunction(game, color):
	score = 0
	for x in range(8):
		for y in range(8):
			piece = game.board[x][y]
			if piece != 0:
				if (piece.canMoveTo((3, 3), game.board[3][3]) and game.isNothingBlocking((x, y), (3, 3))) \
				or (piece.canMoveTo((3, 4), game.board[3][4]) and game.isNothingBlocking((x, y), (3, 4))) \
				or (piece.canMoveTo((4, 3), game.board[4][3]) and game.isNothingBlocking((x, y), (4, 3))) \
				or (piece.canMoveTo((4, 4), game.board[4][4]) and game.isNothingBlocking((x, y), (4, 4))):
					score += 10
	return score

"""
Evaluation function which evaluates moves based on king safety.
"""
def kingEvaluationFunction(game, color):
	score = 0
	if color == Color.WHITE:
		if game.board[2][7].getPiece() == ChessPiece.KING \
		or game.board[6][7].getPiece() == ChessPiece.KING:
			score += 10
	else:
		if game.board[2][0].getPiece() == ChessPiece.KING \
		or game.board[6][0].getPiece() == ChessPiece.KING:
			score += 10
	return score

"""
Evaluation function which evaluates moves based on tempo.
"""
def tempoEvaluationFunction(game, color):
	return 0
	
class MinimaxAgent():
	def __init__(self, game, startColor, evalFn = 'scoreEvaluationFunction', depth = '2'):
		self.evaluationFunction = globals()[evalFn]
		self.depth = int(depth)
		self.game = game
		self.startColor = startColor
		
	def printBoard(self):
		self.game.printBoard()
		
	def movePiece(self, moveFrom, moveTo, oppColor):
		self.game.movePiece(moveFrom, moveTo, oppColor)
		
	def getAction(self):
		def maxValue(state, depth, alpha, beta, colorIndex):
			color = colors[colorIndex % 2]
			if state.isWin(color) or state.isLose(color) or depth == maxDepth:
				return self.evaluationFunction(state, color)
			v = float("-inf")
			for move in state.getLegalMoves(color):
				v = max(v, minValue(state.generateSuccessor(color, move), depth, alpha, beta, colorIndex + 1))
				if v > beta:
					return v
				alpha = max(alpha, v)
			return v
			
		def minValue(state, depth, alpha, beta, colorIndex):
			color = colors[colorIndex % 2]
			if state.isWin(color) or state.isLose(color) or depth == maxDepth:
				return self.evaluationFunction(state, color)
			v = float("inf")
			legalMoves = state.getLegalMoves(color)
			for move in legalMoves:
				v = min(v, maxValue(state.generateSuccessor(color, move), depth + 1, alpha, beta, colorIndex + 1))
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
		    score = max(score, minValue(self.game.generateSuccessor(colors[cIndex], move), 0, alpha, beta, cIndex + 1))
		    if score > previousScore:
		        bestAction = move
		    alpha = max(alpha, score)
		return bestAction
