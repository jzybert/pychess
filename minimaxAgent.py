from chess import *
from pieces import *

def scoreEvaluationFunction(game):
	return 0
	
class MinimaxAgent():
	
	def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2', game, startColor):
		self.evaluationFunction = globals().copy().update(locals()).get(evalFn)
		self.depth = int(depth)
		self.game = game
		self.startColor
		
	def maxValue(state, depth, alpha, beta, colorIndex):
		color = colors[colorIndex % 2]
        if state.isWin(color) or state.isLose(color) or depth == maxDepth:
            return self.evaluationFunction(state)
        v = float("-inf")
        for move in state.getLegalActions(color):
            v = max(v, minValue(state.generateSuccessor(color, move), depth, alpha, beta, colorIndex + 1))
            if v > beta:
                return v
            alpha = max(alpha, v)
        return v
        
    def minValue(state, depth, alpha, beta, colorIndex):
    	color = colors[colorIndex % 2]
        if state.isWin(color) or state.isLose(color) or depth == maxDepth:
            return self.evaluationFunction(state)
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
    legalMoves = game.getLegalMoves(colors[cIndex])
    bestAction = ((0, 0), (0, 1))
    score = float("-inf")
    alpha = float("-inf")
    beta = float("inf")
    for move in legalMoves:
        previousScore = score
        score = max(score, minValue(game.generateSuccessor(colors[cIndex], move), 0, alpha, beta, cIndex + 1))
        if score > previousScore:
            bestAction = move
        alpha = max(alpha, score)
    return bestAction
