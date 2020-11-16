class Piece:
    color: str
    x: int
    y: int
    points: int
    moves: list[list[tuple[int, int]]]

    def __init__(self, color, x, y, points):
        self.color = color
        self.x = x
        self.y = y
        self.points = points
        if self.moves is None:
            self.moves = self.update_moves()
        else:
            self.moves = self.moves.copy()

    def move(self, x: int, y: int):
        self.x = x
        self.y = y
        self.moves = self.update_moves()

    def get_moves(self) -> list[list[tuple[int, int]]]:
        return self.moves

    def update_moves(self) -> list[list[tuple[int, int]]]:
        pass

    @classmethod
    def update_default_moves(cls):
        pass


class Pawn(Piece):
    POINTS = 10

    def __init__(self, color, x, y):
        super(Pawn, self).__init__(color, x, y, Pawn.POINTS)

    def update_moves(self):
        if self.color == 'white':
            y0 = [2, 3]
            direction = -1
        else:
            y0 = [12, 13]
            direction = 1

        moves = [(self.x, self.y + direction)]
        if self.y in y0:
            moves.append((self.x, self.y + 2*direction))

        return [moves]

    @classmethod
    def update_default_moves(cls):
        cls.moves = None


class Rook(Piece):
    pass


class Knight(Piece):
    pass


class Bishop(Piece):
    pass


class Queen(Piece):
    pass


class King(Piece):
    pass


class Blank(Piece):
    def __init__(self, x, y):
        super(Blank, self).__init__('', x, y, 0)
