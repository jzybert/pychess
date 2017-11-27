import argparse
from chess import *
from pieces import *
from minimaxAgent import *

parser = argparse.ArgumentParser(description="Options for a chess game.")
parser.add_argument("-a", "--ai", help="an AI will choose the best move for you", action="store_true")
parser.add_argument("-m", "--material", help="evaluate moves based on material", action="store_true")
args = parser.parse_args()

evalFns = ["scoreEvaluationFunction"]

if not args.ai:
	game = ChessGame()
	
	startColor = input("Which color is starting first (white or black): ")
	colorsToMove = [Color.WHITE, Color.BLACK]
	colorIndex = 1
	if startColor == "white":
		colorIndex = 0
	
	colors = ["White", "Black"]
	while not game.isOver():
		game.printBoard()
		print(colors[colorIndex % 2] + ", it's your move.")
		moveFrom = tuple(int(x.strip()) for x in input("Which piece would you like to move?: ").split(","))
		moveTo = tuple(int(x.strip()) for x in input("Where would you like to move that piece?: ").split(","))
		if game.movePiece(moveFrom, moveTo, colorsToMove[colorIndex]):
			colorIndex += 1
		else:
			print("That was not a vailid move. Try again.")
else:
	game = ChessGame()
	userColor = input("Which color are you (white or black): ")
	color = Color.BLACK
	oppColor = Color.WHITE
	if userColor == "white":
		color = Color.WHITE
		oppColor = Color.BLACK
	
	agent = 0
	if args.material:
		print ("here")
		agent = MinimaxAgent(game, color, "scoreEvaluationFunction")
	else:
	    agent = MinimaxAgent(game, color)
	
	isFirst = input("Are you moving first (yes or no): ")
	if isFirst == "no":
		moveFrom = tuple(int(x.strip()) for x in input("Where did your opponent move from: ").split(","))
		moveTo = tuple(int(x.strip()) for x in input("Where did your opponent move to: ").split(","))
		agent.movePiece(moveFrom, moveTo, oppColor)
	
	while True:
		agent.printBoard()
		print("Generating best move...")
		action = agent.getAction()
		print ("Best action for you to take: %s" % (action,))
		agent.movePiece(action[0], action[1], color)
		agent.printBoard()
		moveFrom = tuple(int(x.strip()) for x in input("Where did your opponent move from: ").split(","))
		moveTo = tuple(int(x.strip()) for x in input("Where did your opponent move to: ").split(","))
		agent.movePiece(moveFrom, moveTo, oppColor)