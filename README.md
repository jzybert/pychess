# pychess
**A game of chess in Python**

This is a work-in-progress chess game written in Python 3.6.

This was designed as my final project for CS 4100 Artificial 
Intelligence at Northeastern University in which we were 
tasked to apply our AI knowledge in some aspect that 
interested us. I chose to make a chess-playing minimax agent 
that compared various evaluation functions.

## How to run:
1. Clone this repository locally
2. Via command line, go to the repository
3. Type `python3 play.py -v` to begin the game

## Optional flags:
1. `-a, --ai` an AI will choose the best move for you
2. `-v, --visual` show the chess board after every move
3. `-m, --material` evaluate moves based on material
4. `-p, --position` evaluate moves based on board position
5. `-k, --king` evaluate moves based on king safety
6. `-d, --data` run two AIs against each other and see timing outputs