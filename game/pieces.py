from game.move import Move


class Piece:
    points: int = -1
    character: str = ''

    @classmethod
    def update_moves(cls, x: int, y: int, board: list[list[str]], color: str) -> list[Move]:
        return [Move()]

    @classmethod
    def is_piece(cls, piece: str) -> bool:
        return piece.lower() == cls.character

    @classmethod
    def is_opponent(cls, piece: str, color: str) -> bool:
        return piece.isupper() if color == 'black' else piece.islower()

    @classmethod
    def get_piece(cls, char: str) -> tuple[type['Piece'], str]:
        if char.isupper():
            color = 'white'
        elif char.islower():
            color = 'black'
        else:
            color = ''
        return piece_charmap[char.lower()], color


class Pawn(Piece):
    points = 10
    character = 'p'

    promote: int = 500

    @classmethod
    def update_moves(cls, x: int, y: int, board: list[list[str]], color: str) -> list[Move]:
        if color == 'white':
            y0 = [12, 13]
            y1 = 8
            direction = -1
        else:
            y0 = [2, 3]
            y1 = 7
            direction = 1

        moves = []
        piece = None

        if Blank.is_piece(board[y + direction][x]):
            moves.append(Move(
                x,
                y,
                x,
                y + direction,
                cls,
                cls.points,
                color
            ))
            if y + direction == y1:
                moves[-1].points += cls.promote
            if y in y0 and Blank.is_piece(board[y + 2 * direction][x]):
                moves.append(Move(
                    x,
                    y,
                    x,
                    y + 2 * direction,
                    cls,
                    cls.points,
                    color,
                ))
        if x > 0 and cls.is_opponent(piece := board[y + direction][x - 1], color):
            moves.append(Move(
                x,
                y,
                x - 1,
                y + direction,
                cls,
                cls.points + cls.get_piece(piece)[0].points,
                color,
            ))
            if y + direction == y1:
                moves[-1].points += cls.promote
        if x < 15 and cls.is_opponent(piece := board[y + direction][x + 1], color):
            moves.append(Move(
                x,
                y,
                x + 1,
                y + direction,
                cls,
                cls.points + cls.get_piece(piece)[0].points,
                color,
            ))
            if y + direction == y1:
                moves[-1].points += cls.promote

        return moves


class Rook(Piece):
    points = 60
    character = 'r'

    @classmethod
    def update_moves(cls, x: int, y: int, board: list[list[str]], color: str) -> list[Move]:
        skip_l = False
        skip_r = False
        skip_t = False
        skip_d = False

        moves = []
        for z in range(1, 16):
            lcheck = x - z >= 0
            rcheck = x + z <= 15
            tcheck = y + z <= 15
            dcheck = y - z >= 0
            if lcheck and not skip_l:
                piece = board[y][x - z]
                if Blank.is_piece(piece) or Piece.is_opponent(piece, color):
                    moves.append(Move(
                        x,
                        y,
                        x - z,
                        y,
                        cls,
                        cls.points,
                        color,

                    ))
                if not Blank.is_piece(piece):
                    skip_l = True
                    if Piece.is_opponent(piece, color):
                        moves[-1].points += cls.get_piece(piece)[0].points * 10
            if rcheck and not skip_r:
                piece = board[y][x + z]
                if Blank.is_piece(piece) or Piece.is_opponent(piece, color):
                    moves.append(Move(
                        x,
                        y,
                        x + z,
                        y,
                        cls,
                        cls.points,
                        color,

                    ))
                if not Blank.is_piece(piece):
                    skip_r = True
                    if Piece.is_opponent(piece, color):
                        moves[-1].points += cls.get_piece(piece)[0].points * 10
            if tcheck and not skip_t:
                piece = board[y + z][x]
                if Blank.is_piece(piece) or Piece.is_opponent(piece, color):
                    moves.append(Move(
                        x,
                        y,
                        x,
                        y + z,
                        cls,
                        cls.points,
                        color,

                    ))
                if not Blank.is_piece(piece):
                    skip_t = True
                    if Piece.is_opponent(piece, color):
                        moves[-1].points += cls.get_piece(piece)[0].points * 10
            if dcheck and not skip_d:
                piece = board[y - z][x]
                if Blank.is_piece(piece) or Piece.is_opponent(piece, color):
                    moves.append(Move(
                        x,
                        y,
                        x,
                        y - z,
                        cls,
                        cls.points,
                        color,

                    ))
                if not Blank.is_piece(piece):
                    skip_d = True
                    if Piece.is_opponent(piece, color):
                        moves[-1].points += cls.get_piece(piece)[0].points * 10

        return moves


class Knight(Piece):
    points = 30
    character = 'h'

    @classmethod
    def update_moves(cls, x: int, y: int, board: list[list[str]], color: str) -> list[Move]:
        moves = []
        if y + 2 <= 15:
            if x - 1 >= 0:
                piece = board[y + 2][x - 1]
                if Blank.is_piece(piece) or Piece.is_opponent(piece, color):
                    moves.append(Move(
                        x,
                        y,
                        x - 1,
                        y + 2,
                        cls,
                        cls.points,
                        color,
                    ))
                    if Piece.is_opponent(piece, color):
                        moves[-1].points += cls.get_piece(piece)[0].points * 10
            if x + 1 <= 15:
                piece = board[y + 2][x + 1]
                if Blank.is_piece(piece) or Piece.is_opponent(piece, color):
                    moves.append(Move(
                        x,
                        y,
                        x + 1,
                        y + 2,
                        cls,
                        cls.points,
                        color,
                    ))
                    if Piece.is_opponent(piece, color):
                        moves[-1].points += cls.get_piece(piece)[0].points * 10
        if y - 2 >= 0:
            if x - 1 >= 0:
                piece = board[y - 2][x - 1]
                if Blank.is_piece(piece) or Piece.is_opponent(piece, color):
                    moves.append(Move(
                        x,
                        y,
                        x - 1,
                        y - 2,
                        cls,
                        cls.points,
                        color,
                    ))
                    if Piece.is_opponent(piece, color):
                        moves[-1].points += cls.get_piece(piece)[0].points * 10
            if x + 1 <= 15:
                piece = board[y - 2][x + 1]
                if Blank.is_piece(piece) or Piece.is_opponent(piece, color):
                    moves.append(Move(
                        x,
                        y,
                        x + 1,
                        y - 2,
                        cls,
                        cls.points,
                        color,
                    ))
                    if Piece.is_opponent(piece, color):
                        moves[-1].points += cls.get_piece(piece)[0].points * 10
        if x + 2 <= 15:
            if y - 1 >= 0:
                piece = board[y - 1][x + 2]
                if Blank.is_piece(piece) or Piece.is_opponent(piece, color):
                    moves.append(Move(
                        x,
                        y,
                        x + 2,
                        y - 1,
                        cls,
                        cls.points,
                        color,
                    ))
                    if Piece.is_opponent(piece, color):
                        moves[-1].points += cls.get_piece(piece)[0].points * 10
            if y + 1 <= 15:
                piece = board[y + 1][x + 2]
                if Blank.is_piece(piece) or Piece.is_opponent(piece, color):
                    moves.append(Move(
                        x,
                        y,
                        x + 2,
                        y + 1,
                        cls,
                        cls.points,
                        color,
                    ))
                    if Piece.is_opponent(piece, color):
                        moves[-1].points += cls.get_piece(piece)[0].points * 10
        if x - 2 >= 0:
            if y - 1 >= 0:
                piece = board[y - 1][x - 2]
                if Blank.is_piece(piece) or Piece.is_opponent(piece, color):
                    moves.append(Move(
                        x,
                        y,
                        x - 2,
                        y - 1,
                        cls,
                        cls.points,
                        color,
                    ))
                    if Piece.is_opponent(piece, color):
                        moves[-1].points += cls.get_piece(piece)[0].points * 10
            if y + 1 <= 15:
                piece = board[y + 1][x - 2]
                if Blank.is_piece(piece) or Piece.is_opponent(piece, color):
                    moves.append(Move(
                        x,
                        y,
                        x - 2,
                        y + 1,
                        cls,
                        cls.points,
                        color,
                    ))
                    if Piece.is_opponent(piece, color):
                        moves[-1].points += cls.get_piece(piece)[0].points * 10

        return moves


class Bishop(Piece):
    points = 40
    character = 'b'

    @classmethod
    def update_moves(cls, x: int, y: int, board: list[list[str]], color: str) -> list[Move]:
        skip_lt = False
        skip_ld = False
        skip_rt = False
        skip_rd = False

        moves = []
        for z in range(1, 16):
            lcheck = x - z >= 0
            rcheck = x + z <= 15
            tcheck = y + z <= 15
            dcheck = y - z >= 0
            if lcheck:
                if tcheck and not skip_lt:
                    piece = board[y + z][x - z]
                    if Blank.is_piece(piece) or Piece.is_opponent(piece, color):
                        moves.append(Move(
                            x,
                            y,
                            x - z,
                            y + z,
                            cls,
                            cls.points,
                            color,
                        ))
                    if not Blank.is_piece(piece):
                        skip_lt = True
                        if Piece.is_opponent(piece, color):
                            moves[-1].points += cls.get_piece(piece)[0].points * 10
                if dcheck and not skip_ld:
                    piece = board[y - z][x - z]
                    if Blank.is_piece(piece) or Piece.is_opponent(piece, color):
                        moves.append(Move(
                            x,
                            y,
                            x - z,
                            y - z,
                            cls,
                            cls.points,
                            color,
                        ))
                    if not Blank.is_piece(piece):
                        skip_ld = True
                        if Piece.is_opponent(piece, color):
                            moves[-1].points += cls.get_piece(piece)[0].points * 10
            if rcheck:
                if tcheck and not skip_rt:
                    piece = board[y + z][x + z]
                    if Blank.is_piece(piece) or Piece.is_opponent(piece, color):
                        moves.append(Move(
                            x,
                            y,
                            x + z,
                            y + z,
                            cls,
                            cls.points,
                            color,
                        ))
                    if not Blank.is_piece(piece):
                        skip_rt = True
                        if Piece.is_opponent(piece, color):
                            moves[-1].points += cls.get_piece(piece)[0].points * 10
                if dcheck and not skip_rd:
                    piece = board[y - z][x + z]
                    if Blank.is_piece(piece) or Piece.is_opponent(piece, color):
                        moves.append(Move(
                            x,
                            y,
                            x + z,
                            y - z,
                            cls,
                            cls.points,
                            color,
                        ))
                    if not Blank.is_piece(piece):
                        skip_rd = True
                        if Piece.is_opponent(piece, color):
                            moves[-1].points += cls.get_piece(piece)[0].points * 10

        return moves


class Queen(Piece):
    points = 5
    character = 'q'

    @classmethod
    def update_moves(cls, x: int, y: int, board: list[list[str]], color: str) -> list[Move]:
        skip_lt = False
        skip_ld = False
        skip_rt = False
        skip_rd = False
        skip_l = False
        skip_r = False
        skip_t = False
        skip_d = False

        moves = []
        for z in range(1, 16):
            lcheck = x - z >= 0
            rcheck = x + z <= 15
            tcheck = y + z <= 15
            dcheck = y - z >= 0
            if lcheck:
                if not skip_l:
                    piece = board[y][x - z]
                    if Blank.is_piece(piece) or Piece.is_opponent(piece, color):
                        moves.append(Move(
                            x,
                            y,
                            x - z,
                            y,
                            cls,
                            cls.points,
                            color,
                        ))
                    if not Blank.is_piece(piece):
                        skip_l = True
                        if Piece.is_opponent(piece, color):
                            moves[-1].points += cls.get_piece(piece)[0].points * 10
                if tcheck and not skip_lt:
                    piece = board[y + z][x - z]
                    if Blank.is_piece(piece) or Piece.is_opponent(piece, color):
                        moves.append(Move(
                            x,
                            y,
                            x - z,
                            y + z,
                            cls,
                            cls.points,
                            color,
                        ))
                    if not Blank.is_piece(piece):
                        skip_lt = True
                        if Piece.is_opponent(piece, color):
                            moves[-1].points += cls.get_piece(piece)[0].points * 10
                if dcheck and not skip_ld:
                    piece = board[y - z][x - z]
                    if Blank.is_piece(piece) or Piece.is_opponent(piece, color):
                        moves.append(Move(
                            x,
                            y,
                            x - z,
                            y - z,
                            cls,
                            cls.points,
                            color,
                        ))
                    if not Blank.is_piece(piece):
                        skip_ld = True
                        if Piece.is_opponent(piece, color):
                            moves[-1].points += cls.get_piece(piece)[0].points * 10
            if rcheck:
                if not skip_r:
                    piece = board[y][x + z]
                    if Blank.is_piece(piece) or Piece.is_opponent(piece, color):
                        moves.append(Move(
                            x,
                            y,
                            x + z,
                            y,
                            cls,
                            cls.points,
                            color,
                        ))
                    if not Blank.is_piece(piece):
                        skip_r = True
                        if Piece.is_opponent(piece, color):
                            moves[-1].points += cls.get_piece(piece)[0].points * 10
                if tcheck and not skip_rt:
                    piece = board[y + z][x + z]
                    if Blank.is_piece(piece) or Piece.is_opponent(piece, color):
                        moves.append(Move(
                            x,
                            y,
                            x + z,
                            y + z,
                            cls,
                            cls.points,
                            color,
                        ))
                    if not Blank.is_piece(piece):
                        skip_rt = True
                        if Piece.is_opponent(piece, color):
                            moves[-1].points += cls.get_piece(piece)[0].points * 10
                if dcheck and not skip_rd:
                    piece = board[y - z][x + z]
                    if Blank.is_piece(piece) or Piece.is_opponent(piece, color):
                        moves.append(Move(
                            x,
                            y,
                            x + z,
                            y - z,
                            cls,
                            cls.points,
                            color,
                        ))
                    if not Blank.is_piece(piece):
                        skip_rd = True
                        if Piece.is_opponent(piece, color):
                            moves[-1].points += cls.get_piece(piece)[0].points * 10
            if tcheck and not skip_t:
                piece = board[y + z][x]
                if Blank.is_piece(piece) or Piece.is_opponent(piece, color):
                    moves.append(Move(
                        x,
                        y,
                        x,
                        y + z,
                        cls,
                        cls.points,
                        color,
                    ))
                if not Blank.is_piece(piece):
                    skip_t = True
                    if Piece.is_opponent(piece, color):
                        moves[-1].points += cls.get_piece(piece)[0].points * 10
            if dcheck and not skip_d:
                piece = board[y - z][x]
                if Blank.is_piece(piece) or Piece.is_opponent(piece, color):
                    moves.append(Move(
                        x,
                        y,
                        x,
                        y - z,
                        cls,
                        cls.points,
                        color,
                    ))
                if not Blank.is_piece(piece):
                    skip_d = True
                    if Piece.is_opponent(piece, color):
                        moves[-1].points += cls.get_piece(piece)[0].points * 10

        return moves


class King(Piece):
    points = 100
    character = 'k'

    @classmethod
    def update_moves(cls, x: int, y: int, board: list[list[str]], color: str) -> list[Move]:
        moves = []
        lcheck = x - 1 >= 0
        rcheck = x + 1 <= 15
        tcheck = y + 1 <= 15
        dcheck = y - 1 >= 0
        if lcheck:
            piece = board[y][x - 1]
            if Blank.is_piece(piece) or Piece.is_opponent(piece, color):
                moves.append(Move(
                    x,
                    y,
                    x - 1,
                    y,
                    cls,
                    cls.points,
                    color,
                ))
                if Piece.is_opponent(piece, color):
                    moves[-1].points += cls.get_piece(piece)[0].points * 10
            if tcheck:
                piece = board[y + 1][x - 1]
                if Blank.is_piece(piece) or Piece.is_opponent(piece, color):
                    moves.append(Move(
                        x,
                        y,
                        x - 1,
                        y + 1,
                        cls,
                        cls.points,
                        color
                    ))
                    if Piece.is_opponent(piece, color):
                        moves[-1].points += cls.get_piece(piece)[0].points * 10
            if dcheck:
                piece = board[y - 1][x - 1]
                if Blank.is_piece(piece) or Piece.is_opponent(piece, color):
                    moves.append(Move(
                        x,
                        y,
                        x - 1,
                        y - 1,
                        cls,
                        cls.points,
                        color,
                    ))
                    if Piece.is_opponent(piece, color):
                        moves[-1].points += cls.get_piece(piece)[0].points * 10
        if rcheck:
            piece = board[y][x + 1]
            if Blank.is_piece(piece) or Piece.is_opponent(piece, color):
                moves.append(Move(
                    x,
                    y,
                    x + 1,
                    y,
                    cls,
                    cls.points,
                    color,
                ))
                if Piece.is_opponent(piece, color):
                    moves[-1].points += cls.get_piece(piece)[0].points * 10
            if tcheck:
                piece = board[y + 1][x + 1]
                if Blank.is_piece(piece) or Piece.is_opponent(piece, color):
                    moves.append(Move(
                        x,
                        y,
                        x + 1,
                        y + 1,
                        cls,
                        cls.points,
                        color,
                    ))
                    if Piece.is_opponent(piece, color):
                        moves[-1].points += cls.get_piece(piece)[0].points * 10
            if dcheck:
                piece = board[y - 1][x + 1]
                if Blank.is_piece(piece) or Piece.is_opponent(piece, color):
                    moves.append(Move(
                        x,
                        y,
                        x + 1,
                        y - 1,
                        cls,
                        cls.points,
                        color,
                    ))
                    if Piece.is_opponent(piece, color):
                        moves[-1].points += cls.get_piece(piece)[0].points * 10
        if tcheck:
            piece = board[y + 1][x]
            if Blank.is_piece(piece) or Piece.is_opponent(piece, color):
                moves.append(Move(
                    x,
                    y,
                    x,
                    y + 1,
                    cls,
                    cls.points,
                    color,
                ))
                if Piece.is_opponent(piece, color):
                    moves[-1].points += cls.get_piece(piece)[0].points * 10
        if dcheck:
            piece = board[y - 1][x]
            if Blank.is_piece(piece) or Piece.is_opponent(piece, color):
                moves.append(Move(
                    x,
                    y,
                    x,
                    y - 1,
                    cls,
                    cls.points,
                    color,
                ))
                if Piece.is_opponent(piece, color):
                    moves[-1].points += cls.get_piece(piece)[0].points * 10

        return moves


class Blank(Piece):
    points = 0
    character = ' '


piece_charmap: dict[str, type[Piece]] = {
        'p': Pawn,
        'r': Rook,
        'h': Knight,
        'b': Bishop,
        'q': Queen,
        'k': King,
        ' ': Blank,
}
