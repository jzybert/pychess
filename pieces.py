from enum import Enum


class ChessPiece(Enum):
    """ ChessPiece enum representing the possible chess pieces. """
    KING = 1
    QUEEN = 2
    ROOK = 3
    BISHOP = 4
    KNIGHT = 5
    PAWN = 6


class Color(Enum):
    """ Color enum representing the possible colors in chess. """
    WHITE = 1
    BLACK = 2


class Piece:
    """
    A Piece is a piece in a chess game.

    :param piece: a ChessPiece
    :param color: a Color
    :param startPos: the starting position of this chess piece
    :param name: the name (or icon) representing this piece
    """
    def __init__(self, piece, color, startPos, name):
        self.piece = piece
        self.color = color
        self.position = startPos
        self.name = name
        self.hasMoved = False

    def getPointVal(self):
        """
        Get the point value for a piece.
        :return: the point value
        """
        if self.piece == ChessPiece.KING:
            return float("inf")
        if self.piece == ChessPiece.QUEEN:
            return 9
        if self.piece == ChessPiece.ROOK:
            return 5
        if self.piece == ChessPiece.BISHOP or self.piece == ChessPiece.KNIGHT:
            return 3
        if self.piece == ChessPiece.PAWN:
            return 1

    def getPiece(self):
        return self.piece

    def getColor(self):
        return self.color

    def getPosition(self):
        return self.position

    def updatePos(self, newPos):
        """
        Update the position of a piece and indicate that it has moved.
        :param newPos: the new position
        """
        self.position = newPos
        self.hasMoved = True

    def getName(self):
        return self.name

    def canMoveTo(self, newPos, board):
        """
        Determines if a piece can move to newPos.
        :param newPos: the position to move to
        :param board: the game board
        :return: True if the piece can move to newPos
        """
        currX, currY = self.position
        newX, newY = newPos
        pieceAtNewPos = board[newX][newY]
        if (newX < 0 or newX > 7 or newY < 0 or newY > 7
            or (pieceAtNewPos != 0
                and pieceAtNewPos.getColor() == self.color)):
            return False
        if self.piece == ChessPiece.PAWN:
            if self.color == Color.BLACK:
                if (pieceAtNewPos != 0
                    and pieceAtNewPos.getColor() != Color.BLACK):
                    return ((currX - 1 == newX or currX + 1 == newX)
                            and currY + 1 == newY)
                if not self.hasMoved:
                    return (currX == newX
                            and (currY + 1 == newY or currY + 2 == newY))
                else:
                    return currX == newX and currY + 1 == newY
            else:
                if (pieceAtNewPos != 0
                    and pieceAtNewPos.getColor() != Color.WHITE):
                    return ((currX - 1 == newX or currX + 1 == newX)
                            and currY - 1 == newY)
                if not self.hasMoved:
                    return (currX == newX
                            and (currY - 1 == newY or currY - 2 == newY))
                else:
                    return currX == newX and currY - 1 == newY
        if self.piece == ChessPiece.BISHOP:
            return abs(currX - newX) == abs(currY - newY)
        if self.piece == ChessPiece.KING:
            if self.color == Color.BLACK:
                return ((not self.hasMoved
                         and self.position == (4, 0)
                         and ((newPos == (2, 0)
                               and not board[0][0].hasMoved
                               and board[0][0].getPiece() == ChessPiece.ROOK)
                              or (newPos == (6, 0)
                                  and not board[7][0].hasMoved
                                  and board[7][0].getPiece() == ChessPiece.ROOK
                                  )))
                        or abs(currX - newX) < 2 and abs(currY - newY) < 2)
            else:
                return ((not self.hasMoved
                         and self.position == (4, 7)
                         and ((newPos == (2, 7)
                               and not board[0][7].hasMoved
                               and board[0][7].getPiece() == ChessPiece.ROOK)
                              or (newPos == (6, 7)
                                  and not board[7][7].hasMoved
                                  and board[7][7].getPiece() == ChessPiece.ROOK
                                  )))
                        or abs(currX - newX) < 2 and abs(currY - newY) < 2)
        if self.piece == ChessPiece.QUEEN:
            return (currX == newX or currY == newY
                    or abs(currX - newX) == abs(currY - newY))
        if self.piece == ChessPiece.ROOK:
            return currX == newX or currY == newY
        if self.piece == ChessPiece.KNIGHT:
            return abs(currX - newX)**2 + abs(currY - newY)**2 == 5
