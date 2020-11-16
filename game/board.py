from game.move import Move
from game.pieces import *

WHITE_PROMOTE = 8
BLACK_PROMOTE = 7
PROMOTE_BONUS = 100


class Board:

    current: list[list[Piece]]
    piece_charmap = {
        'p': Pawn,
        'r': Rook,
        'h': Knight,
        'b': Bishop,
        'q': Queen,
        'k': King,
        ' ': Blank,
    }

    def __init__(self, board):
        self.current = []
        for y in range(0, 16):
            self.current.append([])
            for x in range(0, 16):
                piece_char = board[16*y + x]
                if piece_char != ' ':
                    color = 'white' if piece_char.isupper() else 'black'
                    square = Board.piece_charmap[piece_char.lower()](color, x, y)
                else:
                    square = Blank(x, y)
                self.current[y].append(square)

    def move(self, piece: Piece, x: int, y: int):
        self.current[piece.y][piece.x] = Blank(piece.x, piece.y)
        self.current[y][x] = piece
        piece.move(x, y)

    def update(self, board):
        pass

    def get_moves(self, color) -> [Move]:
        moves = []
        for row in self.current:
            for piece in row:
                if piece is not None and piece.color == color:
                    all_moves = piece.get_moves()
                    for move_group in all_moves:
                        for (x, y) in move_group:
                            square: Piece = self.current[y][x]
                            if square is not None and square.color == color:
                                break
                            new_move = Move(
                                board=self,
                                piece=piece,
                                from_x=piece.x,
                                from_y=piece.y,
                                to_x=x,
                                to_y=y,
                                weight=piece.points
                            )
                            moves.append(new_move)
                            if isinstance(piece, Pawn):
                                if color == 'white':
                                    new_move.weight += PROMOTE_BONUS/(1 + (WHITE_PROMOTE - y))
                                else:
                                    new_move.weight += PROMOTE_BONUS/(1 + (BLACK_PROMOTE - y))
                            if square is not None:
                                new_move.weight += square.points * 10
                                break
        return moves

    def get_all_moves(self, color):
        if color == 'white':
            return self.get_moves('white'), self.get_moves('black')
        else:
            return self.get_moves('black'), self.get_moves('white')
