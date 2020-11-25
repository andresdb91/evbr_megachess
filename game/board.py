from game.pieces import *

WHITE_PROMOTE = 8
BLACK_PROMOTE = 7
PROMOTE_BONUS = 500


class Board:
    current: list[list[str]]
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
    def build_board(board_char: str) -> list[list[str]]:
        board = []
        for y in range(0, 16):
            board.append(list(board_char[y*16:y*16+16]))
        return board

    def move(self, from_x: int, from_y: int, x: int, y: int):
        piece_char = self.current[from_y][from_x]
        piece = self.piece_charmap[piece_char.lower()]
        color = 'white' if piece_char.isupper() else 'black'
        self.current[from_y][from_x] = ' '
        # Promote pawns on 7(black)/8(white)
        if piece == Pawn:
            if y == WHITE_PROMOTE and color == 'white':
                piece_char = 'Q'
            elif y == BLACK_PROMOTE and color == 'black':
                piece_char = 'q'
        self.current[y][x] = piece_char

    def to_char_array(self) -> list[str]:
        char_board = []
        for row in self.current:
            char_board += row
        return char_board

    def update(self, board: str, color: str) -> Move:
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
                    raise Exception('Board desync detected')

        if all([orig, dest]):
            piece = self.piece_charmap[self.current[orig[1]][orig[0]].lower()]

            return Move(
                orig[0],
                orig[1],
                dest[0],
                dest[1],
                piece,
                color,
            )
        else:
            return Move(
                color=color,
            )

    def get_moves(self, color: str) -> list[Move]:
        moves = []
        for board_y, row in enumerate(self.current):
            for board_x, piece_char in enumerate(row):
                if piece_char != ' ' and piece_char.isupper() if color == 'white' else piece_char.islower():
                    piece = self.piece_charmap[piece_char.lower()]
                    moves += piece.update_moves(board_x, board_y, self.current, color)
        return moves

    def get_all_moves(self, color: str) -> tuple[list[Move], list[Move]]:
        if color == 'white':
            return self.get_moves('white'), self.get_moves('black')
        else:
            return self.get_moves('black'), self.get_moves('white')

    def get_piece(self, x: int, y: int):
        return self.piece_charmap[self.current[y][x].lower()]
