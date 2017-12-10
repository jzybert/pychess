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
1. `-v, --visual` show the chess board after every move
2. `-a, --ai` an AI will choose the best move for you
3. `--data1` run tests that compare the time of each evaluation function finding a move
4. `--data2` run tests that compare a random agent against a minimax agent
5. `-m, --material` evaluate moves based on material
6. `-p, --position` evaluate moves based on board position
7. `-k, --king` evaluate moves based on king safety
8. `-c, --combined` evaluate moves with a combination of material, position, and king safety
