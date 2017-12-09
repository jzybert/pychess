import argparse
import time
from chess import *
from minimaxAgent import *

parser = argparse.ArgumentParser(description="Options for a chess game.")
parser.add_argument("-a", "--ai",
                    help="an AI will choose the best move for you",
                    action="store_true")
parser.add_argument("-d", "--data",
                    help="run tests to get data",
                    action="store_true")
parser.add_argument("-v", "--visual",
                    help="show the chess board when playing",
                    action="store_true")
parser.add_argument("-m", "--material",
                    help="evaluate moves based on material",
                    action="store_true")
parser.add_argument("-p", "--position",
                    help="evaluate moves based on position",
                    action="store_true")
parser.add_argument("-k", "--king",
                    help="evaluate moves based on king safety",
                    action="store_true")
args = parser.parse_args()

if not args.ai and not args.data:
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
elif args.ai:
    game = ChessGame()
    userColor = input("Which color are you (white or black): ")
    color = Color.BLACK
    oppColor = Color.WHITE
    if userColor == "white":
        color = Color.WHITE
        oppColor = Color.BLACK

    agent = 0
    if args.material:
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
else:
    game = ChessGame()
    numOfGames = 0
    eval1 = "scoreEvaluationFunction"
    eval2 = "positionEvaluationFunction"
    if args.material and args.king:
        eval2 = "kingEvaluationFunction"
    elif args.position and args.king:
        eval1 = "kingEvaluationFunction"
    agent1 = MinimaxAgent(game, Color.WHITE, eval1)
    agent2 = MinimaxAgent(game, Color.BLACK, eval2)

    numOfWhiteWins = 0
    numOfBlackWins = 0
    times1 = []
    times2 = []
    for i in range(1):
        print("Running simulation " + str(i))
        while not game.isOver():
            start1 = time.time()
            action1 = agent1.getAction()
            end1 = time.time()
            agent1.movePiece(action1[0], action1[1], Color.WHITE)
            print("Move took: " + str(end1 - start1))
            if args.visual:
                agent1.printBoard()
            start2 = time.time()
            action2 = agent2.getAction()
            end2 = time.time()
            agent2.movePiece(action2[0], action2[1], Color.BLACK)
            print("Move took: " + str(end2 - start2))
            if args.visual:
                agent2.printBoard()
            times1.append(end1 - start1)
            times2.append(end2 - start2)
        if game.whiteWins:
            numOfWhiteWins += 1
        if game.blackWins:
            numOfBlackWins += 1
    averageTime1 = sum(times1) / len(times1)
    averageTime2 = sum(times2) / len(times2)
    print("Average time for white move: " + str(averageTime1))
    print("Average time for black move: " + str(averageTime2))
    print("White won: " + str(numOfWhiteWins))
    print("Black won: " + str(numOfBlackWins))
