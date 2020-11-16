class Piece:
    color: str
    x: int
    y: int
    points: int
    moves: list[list[tuple[int, int]]] = None

    def __init__(self, color, x, y, points):
        self.color = color
        self.x = x
        self.y = y
        self.points = points
        if self.moves is None:
            self.moves = self.update_moves(self.x, self.y, self.color)
        else:
            self.moves = self.moves.copy()

    def move(self, x: int, y: int):
        self.x = x
        self.y = y
        self.moves = self.update_moves(self.x, self.y, self.color)

    def get_moves(self) -> list[list[tuple[int, int]]]:
        return self.moves

    @staticmethod
    def update_moves(x, y, color) -> list[list[tuple[int, int]]]:
        return [[]]


class Pawn(Piece):
    POINTS = 10

    def __init__(self, color, x, y):
        super(Pawn, self).__init__(color, x, y, Pawn.POINTS)

    @staticmethod
    def update_moves(x, y, color):
        if color == 'white':
            y0 = [12, 13]
            direction = -1
        else:
            y0 = [2, 3]
            direction = 1

        move = [(x, y + direction)]
        if y in y0:
            move.append((x, y + 2 * direction))

        eat_left = []
        if x > 0:
            eat_left = [(x - 1, y + direction)]

        eat_right = []
        if x < 15:
            eat_right = [(x + 1, y + direction)]

        return [
            move,
            eat_left,
            eat_right,
        ]


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
