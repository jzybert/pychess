from enum import Enum

"""
Enumeration representing the six pieces of a chess game and their point values.
"""
class ChessPiece(Enum):	
	KING = 1
	QUEEN = 2
	ROOK = 3
	BISHOP = 4
	KNIGHT = 5
	PAWN = 6
	
class Color(Enum):
	WHITE = 1
	BLACK = 2

class Piece():
	def __init__(self, piece, color, startPos, name):
		self.piece = piece
		self.color = color
		self.position = startPos
		self.name = name
		self.hasMoved = False
	
	def getPointVal(self):
		if (self.piece.name == KING):
			return float(inf)
		if (self.piece.name == QUEEN):
			return 9
		if (self.piece.name == ROOK):
			return 5
		if (self.piece.name == BISHOP or self.name == KNIGHT):
			return 3
		if (self.piece.name == PAWN):
			return 1
			
	def getPiece(self):
		return self.piece
		
	def getColor(self):
		return self.color
		
	def getPosition(self):
		return self.startPos
	
	def updatePos(self, newPos):
		self.position = newPos
		self.hasMoved = True
	
	def getName(self):
		return self.name
		
	def canMoveTo(self, newPos, pieceAtNewPos):
		currX, currY = self.position
		newX, newY = newPos
		if newX < 0 or newX > 7 or newY < 0 or newY > 7:
			return False
		if self.piece == ChessPiece.PAWN:
			if self.color == Color.BLACK:
				if pieceAtNewPos != 0 and pieceAtNewPos.getColor() != Color.BLACK:
					return (currX - 1 == newX or currX + 1 == newX) and currY + 1 == newY
				if not self.hasMoved:
					return currX == newX and (currY + 1 == newY or currY + 2 == newY)
				else:
					return currX == newX and currY + 1 == newY
			else:
				if pieceAtNewPos != 0 and pieceAtNewPos.getColor() != Color.WHITE:
					return (currX - 1 == newX or currX + 1 == newX) and currY - 1 == newY
				if not self.hasMoved:
					return currX == newX and (currY - 1 == newY or currY - 2 == newY)
				else:
					return currX == newX and currY - 1 == newY
		if self.piece == ChessPiece.BISHOP:
			return abs(currX - newX) == abs(currY - newY)
		if self.piece == ChessPiece.KING:
			if self.color == Color.BLACK:
				return (not self.hasMoved and self.position == (4, 0) and (newPos == (2, 0) or newPos == (6, 0))) or abs(currX - newX) < 2 and abs(currY - newY) < 2
			else:
				return (not self.hasMoved and self.position == (4, 7) and (newPos == (2, 7) or newPos == (6, 7))) or abs(currX - newX) < 2 and abs(currY - newY) < 2
		if self.piece == ChessPiece.QUEEN:
			return currX == newX or currY == newY or abs(currX - newX) == abs(currY - newY)
		if self.piece == ChessPiece.ROOK:
			return currX == newX or currY == newY
		if self.piece == ChessPiece.KNIGHT:
			return abs(currX - newX)**2 + abs(currY - newY)**2 == 5