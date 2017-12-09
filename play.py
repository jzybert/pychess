import argparse
import time
from chess import *
from minimaxAgent import *
from randomAgent import *

parser = argparse.ArgumentParser(description="Options for a chess game.")
# show chess board after each move
parser.add_argument("-v", "--visual",
                    help="show the chess board when playing",
                    action="store_true")
# options for ai/testing
parser.add_argument("-a", "--ai",
                    help="an AI will choose the best move for you",
                    action="store_true")
parser.add_argument("--data1",
                    help="run tests to compare evaluation functions",
                    action="store_true")
parser.add_argument("--data2",
                    help="run tests to compare agents",
                    action="store_true")
# options for evaluation functions
parser.add_argument("-m", "--material",
                    help="evaluate moves purely based on material",
                    action="store_true")
parser.add_argument("-p", "--position",
                    help="evaluate moves purely based on position",
                    action="store_true")
parser.add_argument("-k", "--king",
                    help="evaluate moves purely based on king safety",
                    action="store_true")
parser.add_argument("-c", "--combined",
                    help="evaluate moves based on material, position, and "
                         "king safety",
                    action="store_true")
# options for agents
parser.add_argument("--random",
                    help="use a random agent to determine moves",
                    action="store_true")
parser.add_argument("--minimax",
                    help="use a minimax agent to determine moves",
                    action="store_true")
args = parser.parse_args()
# normal game of chess (no AI or tests)
if not args.ai and not args.data1 and not args.data2:
    game = ChessGame()

    startColor = input("Which color is starting first (white or black): ")
    colorsToMove = [Color.WHITE, Color.BLACK]
    colorIndex = 1
    if startColor == "white":
        colorIndex = 0

    colors = ["White", "Black"]
    while not game.isOver():
        if args.visual:
            game.printBoard()
        print(colors[colorIndex % 2] + ", it's your move.")
        moveFrom = tuple(
            int(x.strip()) for x in input(
                "Which piece would you like to move?: "
            ).split(",")
        )
        moveTo = tuple(
            int(x.strip()) for x in input(
                "Where would you like to move that piece?: "
            ).split(","))
        if game.movePiece(moveFrom, moveTo, colorsToMove[colorIndex % 2]):
            colorIndex += 1
        else:
            print("That was not a valid move. Try again.")
# an AI will tell you which move is the best
elif args.ai:
    game = ChessGame()
    userColor = input("Which color are you (white or black): ")
    color = Color.BLACK
    oppColor = Color.WHITE
    if userColor == "white":
        color = Color.WHITE
        oppColor = Color.BLACK

    agent = 0
    if args.random:
        agent = RandomAgent(game, color)
    elif args.material:
        agent = MinimaxAgent(game, color, "scoreEvaluationFunction")
    elif args.position:
        agent = MinimaxAgent(game, color, "positionEvaluationFunction")
    elif args.king:
        agent = MinimaxAgent(game, color, "kingEvaluationFunction")
    else:
        agent = MinimaxAgent(game, color)

    isFirst = input("Are you moving first (yes or no): ")
    if isFirst == "no":
        moveFrom = tuple(
            int(x.strip()) for x in input(
                "Where did your opponent move from: "
            ).split(",")
        )
        moveTo = tuple(
            int(x.strip()) for x in input(
                "Where did your opponent move to: "
            ).split(",")
        )
        agent.movePiece(moveFrom, moveTo, oppColor)

    while not game.isOver():
        if args.visual:
            agent.printBoard()
        print("Generating best move...")
        action = agent.getAction()
        print("Best action for you to take: %s" % (action,))
        agent.movePiece(action[0], action[1], color)
        if args.visual:
            agent.printBoard()
        moveFrom = tuple(
            int(x.strip()) for x in input(
                "Where did your opponent move from: "
            ).split(",")
        )
        moveTo = tuple(
            int(x.strip()) for x in input(
                "Where did your opponent move to: "
            ).split(",")
        )
        agent.movePiece(moveFrom, moveTo, oppColor)
# tests for evaluation functions
elif args.data1:
    game = ChessGame()

    eval1 = "scoreEvaluationFunction"
    eval2 = "positionEvaluationFunction"
    if args.material and args.king:
        eval2 = "kingEvaluationFunction"
    elif args.material and args.combined:
        eval2 = "combinedEvaluationFunction"
    elif args.position and args.king:
        eval1 = "kingEvaluationFunction"
    elif args.position and args.combined:
        eval1 = "combinedEvaluationFunction"
    elif args.king and args.combined:
        eval1 = "kingEvaluationFunction"
        eval2 = "combinedEvaluationFunction"

    print("Starting simulation for " + eval1 + " and " + eval2 + ".")
    agent1 = MinimaxAgent(game, Color.WHITE, eval1)
    agent2 = MinimaxAgent(game, Color.BLACK, eval2)

    print("Gathering data...")

    start1 = time.time()
    action1 = agent1.getAction()
    end1 = time.time()
    agent1.movePiece(action1[0], action1[1], Color.WHITE)
    print("First move for white took " + str(end1 - start1) + " seconds.")
    if args.visual:
        agent1.printBoard()

    start2 = time.time()
    action2 = agent2.getAction()
    end2 = time.time()
    agent2.movePiece(action2[0], action2[1], Color.BLACK)
    print("First move for black took: " + str(end2 - start2) + " seconds.")
    if args.visual:
        agent2.printBoard()
else:
    game = ChessGame()
