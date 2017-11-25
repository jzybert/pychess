from pieces import *

"""
The state of a chess game.
"""
class ChessGame:
	def __init__(self):
		self.board = self.generateBoard()
		self.capturedWhitePieces = []
		self.capturedBlackPieces = []
		self.whiteWins = False
		self.blackWins = False
		
	def isOver(self):
		if self.whiteWins:
			print("White wins!")
			return True
		if self.blackWins:
			print("Black wins!")
			return True
		return False
	
	def generateBoard(self):
		board = []
		
		for x in range(8):
			row = []
			for y in range(8):
				if (y == 1):
					row.append(Piece(ChessPiece.PAWN, Color.BLACK, (x, y), "BP"))
				elif (y == 6):
					row.append(Piece(ChessPiece.PAWN, Color.WHITE, (x, y), "WP"))
				else:
					row.append(0)
			board.append(row)
				
		board[0][0] = Piece(ChessPiece.ROOK, Color.BLACK, (0, 0), "BR1")
		board[1][0] = Piece(ChessPiece.KNIGHT, Color.BLACK, (1, 0), "BK1")
		board[2][0] = Piece(ChessPiece.BISHOP, Color.BLACK, (2, 0), "BB1")
		board[3][0] = Piece(ChessPiece.QUEEN, Color.BLACK, (3, 0), "BQ")
		board[4][0] = Piece(ChessPiece.KING, Color.BLACK, (4, 0), "BK")
		board[5][0] = Piece(ChessPiece.BISHOP, Color.BLACK, (5, 0), "BB2")
		board[6][0] = Piece(ChessPiece.KNIGHT, Color.BLACK, (6, 0), "BK2")
		board[7][0] = Piece(ChessPiece.ROOK, Color.BLACK, (7, 0), "BR2")
		
		board[0][7] = Piece(ChessPiece.ROOK, Color.WHITE, (0, 7), "WR1")
		board[1][7] = Piece(ChessPiece.KNIGHT, Color.WHITE, (1, 7), "WR1")
		board[2][7] = Piece(ChessPiece.BISHOP, Color.WHITE, (2, 7), "WB1")
		board[3][7] = Piece(ChessPiece.QUEEN, Color.WHITE, (3, 7), "WQ")
		board[4][7] = Piece(ChessPiece.KING, Color.WHITE, (4, 7), "WK")
		board[5][7] = Piece(ChessPiece.BISHOP, Color.WHITE, (5, 7), "WB2")
		board[6][7] = Piece(ChessPiece.KNIGHT, Color.WHITE, (6, 7), "WK2")
		board[7][7] = Piece(ChessPiece.ROOK, Color.WHITE, (7, 7), "WR2")
		
		return board
		
	def printBoard(self):
		for y in range(8):
			for x in range(8):
				if self.board[x][y] == 0:
					print (" 0 ", end=" ")
				else:
					name = self.board[x][y].getName()
					if len(name) == 2:
						print (name + " ", end=" ")
					else:
						print (self.board[x][y].getName(), end=" ")
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
					for x in range(newX, currX - 1):
						if self.board[x][i] != 0 and x != newX:
							return False
						i -= 1
					return True
				if currX > newX and currY > newY:
					i = currY - 1
					for x in range(newX, currX - 1):
						if self.board[x][i] != 0 and x != newX:
							return False
						i -= 1
					return True
				if currX < newX and currY > newY:
					i = currY - 1
					for x in range(currX + 1, newX):
						if self.board[x][i] != 0 and x != newX:
							return False
						i += 1
					return True
			if piece == ChessPiece.ROOK:
				if currX > newX:
					for x in range(newX, currX - 1):
						if self.board[x][currY] != 0 and x != newX:
							return False
					return True
				if currX < newX:
					for x in range(currX + 1, newX):
						if self.board[x][currY] != 0 and x != newX:
							return False
					return True
				if currY > newY:
					for y in range(newY, currY - 1):
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
						for x in range(newX, currX - 1):
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
						for y in range(newY, currY - 1):
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
						for x in range(newX, currX - 1):
							if self.board[x][i] != 0 and x != newX:
								return False
							i -= 1
						return True
					if currX > newX and currY > newY:
						i = currY - 1
						for x in range(newX, currX - 1):
							if self.board[x][i] != 0 and x != newX:
								return False
							i -= 1
						return True
					if currX < newX and currY > newY:
						i = currY - 1
						for x in range(currX + 1, newX):
							if self.board[x][i] != 0 and x != newX:
								return False
							i += 1
						return True
			else:
			    return True
		return False