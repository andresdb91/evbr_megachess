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
    piece_charmap_inv = {v: k for k, v in piece_charmap.items()}

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
        # Promote pawns on 7(black)/8(white)
        if isinstance(piece, Pawn) and y == WHITE_PROMOTE and piece.color == 'white':
            piece = Queen('white', x, y)
        elif isinstance(piece, Pawn) and y == BLACK_PROMOTE and piece.color == 'black':
            piece = Queen('black', x, y)
        else:
            piece.move(x, y)

        self.current[y][x] = piece

    def to_char_array(self):
        char_board = []
        for row in self.current:
            for square in row:
                char_board.append(self.piece_charmap_inv[square.__class__])
        return char_board

    def update(self, board):
        old_board = self.to_char_array()
        new_board = list(board)

        orig: tuple[int, int] = (-1, -1)
        dest: tuple[int, int] = (-1, -1)

        for i in range(0, len(old_board)):
            if old_board[i] != new_board[i]:
                coord = (i % 16, int(i/16))
                if new_board[i] == ' ':
                    orig = coord
                else:
                    dest = coord

        if orig[0] >= 0 and dest[0] >= 0:
            piece = self.current[orig[1]][orig[0]]
            self.current[orig[1]][orig[0]] = Blank(orig[0], orig[1])
            self.current[dest[1]][dest[0]] = piece
            piece.move(dest[0], dest[1])

    def get_moves(self, color) -> [Move]:
        moves = []
        for row in self.current:
            for piece in row:
                if not isinstance(piece, Blank) and piece.color == color:
                    all_moves = piece.get_moves()
                    for move_group in all_moves:
                        for (x, y) in move_group:
                            square: Piece = self.current[y][x]
                            if not isinstance(square, Blank) and square.color == color:
                                break
                            if isinstance(piece, Pawn):
                                if piece.x == x and not isinstance(square, Blank):
                                    break
                                elif piece.x != x and (isinstance(square, Blank) or square.color == color):
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
                                    new_move.weight += PROMOTE_BONUS/(1 + abs(WHITE_PROMOTE - y))
                                else:
                                    new_move.weight += PROMOTE_BONUS/(1 + abs(BLACK_PROMOTE - y))
                            if not isinstance(square, Blank):
                                new_move.weight += square.points * 10
                                break
        return moves

    def get_all_moves(self, color):
        if color == 'white':
            return self.get_moves('white'), self.get_moves('black')
        else:
            return self.get_moves('black'), self.get_moves('white')
