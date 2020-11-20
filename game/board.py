from game.move import Move
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
            # for x in range(0, 16):
            #     piece_char = board_char[16*y + x]
            #     if piece_char != ' ':
            #         color = 'white' if piece_char.isupper() else 'black'
            #         square = Board.piece_charmap[piece_char.lower()](color, x, y)
            #     else:
            #         square = Blank(x, y)
            #     board[y].append(square)
        return board

    def move(self, from_x: int, from_y: int, x: int, y: int):
        piece_char = self.current[from_y][from_x]
        piece = self.piece_charmap[piece_char.lower()]
        color = 'white' if piece_char.isupper() else 'black'
        self.current[from_y][from_x] = ' '
        # Promote pawns on 7(black)/8(white)
        if piece == Pawn:
            if y == WHITE_PROMOTE and color == 'white':
                # piece = Queen('white', x, y)
                self.current[y][x] = 'Q'
            elif y == BLACK_PROMOTE and color == 'black':
                # piece = Queen('black', x, y)
                self.current[y][x] = 'q'
        # else:
            # piece.move(x, y)

        self.current[y][x] = piece_char

    def to_char_array(self) -> list[str]:
        char_board = []
        for row in self.current:
            char_board.append(''.join(row))
            # for square in row:
            #     char_piece = self.piece_charmap_inv[square.__class__]
            #     if square.color == 'white':
            #         char_piece = char_piece.upper()
            #     char_board.append(char_piece)
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
                    return Move()

        if all([orig, dest]):
            piece = self.piece_charmap[self.current[orig[1]][orig[0]].lower()]
            square = self.piece_charmap[self.current[dest[1]][dest[0]].lower()]

            points = piece.points
            if piece == Pawn:
                if ((color == 'white' and dest[1] == WHITE_PROMOTE)
                        or (color == 'black' and dest[1] == BLACK_PROMOTE)):
                    points += 500
            if square != Blank:
                points += square.points * 10

            return Move(
                orig[0],
                orig[1],
                dest[0],
                dest[1],
                self,
                color,
                points,
            )
        else:
            return Move(
                board=self,
                color=color,
                points=-20,
            )

    def get_moves(self, color: str) -> list[Move]:
        moves = []
        for board_y in range(0, len(self.current)):
            row = self.current[board_y]
            for board_x in range(0, 16):
                piece_char = row[board_x]
                # if not isinstance(piece, Blank) and piece.color == color:
                if piece_char != ' ' and piece_char.isupper() if color == 'white' else piece_char.islower():
                    piece = self.piece_charmap[piece_char.lower()]
                    all_moves = piece.update_moves(board_x, board_y, color)
                    for move_group in all_moves:
                        for (x, y) in move_group:
                            square = self.piece_charmap[self.current[y][x].lower()]
                            square_color = 'white' if self.current[y][x].isupper() else 'black'
                            if not square == Blank and square_color == color:
                                break
                            if piece == Pawn:
                                if board_x == x and square != Blank:
                                    break
                                elif board_x != x and (square == Blank or square_color == color):
                                    break
                            new_move = Move(
                                board=self,
                                from_x=board_x,
                                from_y=board_y,
                                to_x=x,
                                to_y=y,
                                color=color,
                                points=piece.points,
                            )
                            moves.append(new_move)
                            if piece == Pawn:
                                if ((color == 'white' and y == WHITE_PROMOTE)
                                        or (color == 'black' and y == BLACK_PROMOTE)):
                                    new_move.points += 500
                            if square != Blank:
                                new_move.points += square.points * 10
                                break
        return moves

    def get_all_moves(self, color: str) -> tuple[list[Move], list[Move]]:
        if color == 'white':
            return self.get_moves('white'), self.get_moves('black')
        else:
            return self.get_moves('black'), self.get_moves('white')

    def get_piece(self, x: int, y: int):
        return self.piece_charmap[self.current[y][x].lower()]
