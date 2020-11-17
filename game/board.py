from game.move import Move
from game.pieces import *

WHITE_PROMOTE = 8
BLACK_PROMOTE = 7
PROMOTE_BONUS = 500


class Board:
    current: list[list[Piece]]
    piece_charmap: dict[str, type[Piece]] = {
        'p': Pawn,
        'r': Rook,
        'h': Knight,
        'b': Bishop,
        'q': Queen,
        'k': King,
        ' ': Blank,
    }
    piece_charmap_inv: dict[type[Piece]: str] = {v: k for k, v in piece_charmap.items()}

    def __init__(self, board: str):
        self.current = Board.build_board(board)

    @staticmethod
    def build_board(board_char: str) -> list[list[Piece]]:
        board = []
        for y in range(0, 16):
            board.append([])
            for x in range(0, 16):
                piece_char = board_char[16*y + x]
                if piece_char != ' ':
                    color = 'white' if piece_char.isupper() else 'black'
                    square = Board.piece_charmap[piece_char.lower()](color, x, y)
                else:
                    square = Blank(x, y)
                board[y].append(square)
        return board

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

    def to_char_array(self) -> list[str]:
        char_board = []
        for row in self.current:
            for square in row:
                char_piece = self.piece_charmap_inv[square.__class__]
                if square.color == 'white':
                    char_piece = char_piece.upper()
                char_board.append(char_piece)
        return char_board

    def update(self, board: str):
        old_board = self.to_char_array()
        new_board = list(board)

        orig = None
        dest = None

        for i in range(0, len(old_board)):
            if old_board[i] != new_board[i]:
                coord = (i % 16, int(i/16))
                if new_board[i] == ' ' and orig is None:
                    orig = coord
                elif dest is None:
                    dest = coord
                else:
                    print('Board desync, rebuilding')
                    self.current = Board.build_board(board)
                    return

        if all([orig, dest]):
            piece = self.current[orig[1]][orig[0]]
            self.current[orig[1]][orig[0]] = Blank(orig[0], orig[1])
            self.current[dest[1]][dest[0]] = piece
            self.move(piece, dest[0], dest[1])

    def get_moves(self, color: str) -> list[Move]:
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
                            moves.append(Move(
                                board=self,
                                piece=piece,
                                from_x=piece.x,
                                from_y=piece.y,
                                to_x=x,
                                to_y=y,
                                points=piece.points
                            ))
                            if not isinstance(square, Blank):
                                break
        return moves

    def get_all_moves(self, color: str) -> tuple[list[Move], list[Move]]:
        if color == 'white':
            return self.get_moves('white'), self.get_moves('black')
        else:
            return self.get_moves('black'), self.get_moves('white')
