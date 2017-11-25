import argparse
from chess import *
from pieces import *
from minimaxAgent import *

parser = argparse.ArgumentParser(description="Options for a chess game.")
parser.add_argument("-p", "--play", help="play a game of chess", action="store_true")
parser.add_argument("-a", "--ai", help="an AI will choose the best move for you", action="store_true")
args = parser.parse_args()

if (args.play):
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

if (args.ai):
	game = ChessGame()
	userColor = input("Which color are you (white or black): ")
	color = Color.BLACK
	if userColor == "white":
		color = Color.WHITE
		
	agent = MinimaxAgent(game, color)