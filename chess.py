import copy
from pieces import *


""" The state of a chess game. """
class ChessGame:
	"""
	Initialize the ChessGame.
	
	self.board -- a list of pieces on the board
	self.capturedWhitePieces -- a list of captured white pieces
	self.capturedBlackPieces -- a list of captured black pieces
	self.whiteWins -- True if white wins
	self.blackWins -- True if black wins
	"""
	def __init__(self):
		self.board = self.generateBoard()
		self.capturedWhitePieces = []
		self.capturedBlackPieces = []
		self.whiteWins = False
		self.blackWins = False
	
	"""
	Returns True if the given color won.
	
	color -- the color to be checked if it won
	"""
	def isWin(self, color):
		return (color == Color.WHITE and self.whiteWins) \
		            or (color == Color.BLACK and self.blackWins)
		
	"""
	Returns True if the given color lost.
	
	color -- the color to be check if it lost
	"""
	def isLose(self, color):
		return (color == Color.WHITE and self.blackWins) \
		            or (color == Color.BLACK and self.whiteWins)
		
	""" Returns True if the game is over (i.e. did a color win?). """
	def isOver(self):
		if self.whiteWins:
			print("White wins!")
			return True
		if self.blackWins:
			print("Black wins!")
			return True
		return False
		
	"""
	Returns a list of legal moves for the given color.
	
	color -- the color to find legal moves for
	"""
	def getLegalMoves(self, color):
		moves = []
		for x in range(8):
			for y in range(8):
				piece = self.board[x][y]
				if piece != 0 and piece.getColor() == color:
					for moveX in range(8):
						for moveY in range(8):
							if piece.canMoveTo((moveX, moveY), self.board[moveX][moveY]) \
							   and self.isNothingBlocking((x, y), (moveX, moveY)):
								moves.append(((x, y), (moveX, moveY)))
		return moves
		
	"""
	Returns the successor ChessGame based for the given color taking the given move.
	"""
	def generateSuccessor(self, color, move):
		nextState = copy.deepcopy(self)
		currPos = move[0]
		newPos = move[1]
		nextState.movePiece(currPos, newPos, color)
		return nextState
	
	def generateBoard(self):
		board = []
		
		for x in range(8):
			row = []
			for y in range(8):
				if (y == 1):
					row.append(Piece(ChessPiece.PAWN, Color.BLACK, (x, y), "♟"))
				elif (y == 6):
					row.append(Piece(ChessPiece.PAWN, Color.WHITE, (x, y), "♙"))
				else:
					row.append(0)
			board.append(row)
				
		board[0][0] = Piece(ChessPiece.ROOK, Color.BLACK, (0, 0), "♜")
		board[1][0] = Piece(ChessPiece.KNIGHT, Color.BLACK, (1, 0), "♞")
		board[2][0] = Piece(ChessPiece.BISHOP, Color.BLACK, (2, 0), "♝")
		board[3][0] = Piece(ChessPiece.QUEEN, Color.BLACK, (3, 0), "♛")
		board[4][0] = Piece(ChessPiece.KING, Color.BLACK, (4, 0), "♚")
		board[5][0] = Piece(ChessPiece.BISHOP, Color.BLACK, (5, 0), "♝")
		board[6][0] = Piece(ChessPiece.KNIGHT, Color.BLACK, (6, 0), "♞")
		board[7][0] = Piece(ChessPiece.ROOK, Color.BLACK, (7, 0), "♜")
		
		board[0][7] = Piece(ChessPiece.ROOK, Color.WHITE, (0, 7), "♖")
		board[1][7] = Piece(ChessPiece.KNIGHT, Color.WHITE, (1, 7), "♘")
		board[2][7] = Piece(ChessPiece.BISHOP, Color.WHITE, (2, 7), "♗")
		board[3][7] = Piece(ChessPiece.QUEEN, Color.WHITE, (3, 7), "♕")
		board[4][7] = Piece(ChessPiece.KING, Color.WHITE, (4, 7), "♔")
		board[5][7] = Piece(ChessPiece.BISHOP, Color.WHITE, (5, 7), "♗")
		board[6][7] = Piece(ChessPiece.KNIGHT, Color.WHITE, (6, 7), "♘")
		board[7][7] = Piece(ChessPiece.ROOK, Color.WHITE, (7, 7), "♖")
		
		return board
		
	def printBoard(self):
		for y in range(8):
			for x in range(8):
				if self.board[x][y] == 0:
					print (" 0", end=" ")
				else:
					name = self.board[x][y].getName()
					print (" " + name, end=" ")
			print (" ")
		print (" ")
	
	def movePiece(self, currPos, newPos, currColor):
		currX, currY = currPos
		newX, newY = newPos
		piece = self.board[currX][currY]
		if piece != 0 and piece.getColor() == currColor and piece.canMoveTo(newPos, self.board[newX][newY]) and self.isNothingBlocking(currPos, newPos):
			if self.board[newX][newY] != 0:
				if self.board[newX][newY].getColor() == Color.WHITE:
					self.capturedWhitePieces.append(self.board[newX][newY])
					if self.board[newX][newY].getPiece() == ChessPiece.KING:
						self.blackWins = True
				else:
					self.capturedBlackPieces.append(self.board[newX][newY])
					if self.board[newX][newY].getPiece() == ChessPiece.KING:
						self.whiteWins = True
			if piece.getPiece() == ChessPiece.KING:
				y = 0
				if piece.getColor() == Color.WHITE:
					y = 7
				if currPos == (4, y) and newPos == (2, y):
					rook = self.board[0][y]
					self.board[0][y].updatePos((3, y))
					self.board[0][y] = 0
					self.board[3][y] = rook
				if currPos == (4, y) and newPos == (6, y):
					rook = self.board[7][y]
					self.board[7][y].updatePos((5, y))
					self.board[7][y] = 0
					self.board[5][y] = rook
			piece.updatePos(newPos)
			self.board[currX][currY] = 0
			self.board[newX][newY] = piece
			return True
		else:
			return False
			
	def isNothingBlocking(self, currPos, newPos):
		currX, currY = currPos
		newX, newY = newPos
		currBoard = self.board[currX][currY]
		newBoard = self.board[newX][newY]
		if newBoard == 0 or newBoard.getColor() != currBoard.getColor():
			piece = currBoard.getPiece()
			if piece == ChessPiece.BISHOP:
				if currX < newX and currY < newY:
					i = currY + 1
					for x in range(currX + 1, newX):
						if self.board[x][i] != 0 and x != newX:
							return False
						i += 1
					return True
				if currX > newX and currY < newY:
					i = newY
					for x in range(newX, currX):
						if self.board[x][i] != 0 and x != newX:
							return False
						i -= 1
					return True
				if currX > newX and currY > newY:
					i = newY
					for x in range(newX, currX):
						if self.board[x][i] != 0 and x != newX:
							return False
						i += 1
					return True
				if currX < newX and currY > newY:
					i = currY - 1
					for x in range(currX + 1, newX):
						if self.board[x][i] != 0 and x != newX:
							return False
						i -= 1
					return True
			if piece == ChessPiece.ROOK:
				if currX > newX:
					for x in range(newX, currX):
						if self.board[x][currY] != 0 and x != newX:
							return False
					return True
				if currX < newX:
					for x in range(currX + 1, newX):
						if self.board[x][currY] != 0 and x != newX:
							return False
					return True
				if currY > newY:
					for y in range(newY, currY):
						if self.board[currX][y] != 0 and y != newY:
							return False
					return True
				if currY < newY:
					for y in range(currY + 1, newY):
						if self.board[currX][y] != 0 and y != newY:
							return False
					return True
			if piece == ChessPiece.QUEEN:
				if currY == newY:
					if currX > newX:
						for x in range(newX, currX):
							if self.board[x][currY] != 0 and x != newX:
								return False
						return True
					if currX < newX:
						for x in range(currX + 1, newX):
							if self.board[x][currY] != 0 and x != newX:
								return False
						return True
				elif currX == newX:
					if currY > newY:
						for y in range(newY, currY):
							if self.board[currX][y] != 0 and y != newY:
								return False
						return True
					if currY < newY:
						for y in range(currY + 1, newY):
							if self.board[currX][y] != 0 and y != newY:
								return False
						return True
				else:
					if currX < newX and currY < newY:
						i = currY + 1
						for x in range(currX + 1, newX):
							if self.board[x][i] != 0 and x != newX:
								return False
							i += 1
						return True
					if currX > newX and currY < newY:
						i = newY
						for x in range(newX, currX):
							if self.board[x][i] != 0 and x != newX:
								return False
							i -= 1
						return True
					if currX > newX and currY > newY:
						i = newY
						for x in range(newX, currX):
							if self.board[x][i] != 0 and x != newX:
								return False
							i += 1
						return True
					if currX < newX and currY > newY:
						i = currY - 1
						for x in range(currX + 1, newX):
							if self.board[x][i] != 0 and x != newX:
								return False
							i -= 1
						return True
			else:
			    return True
		return False