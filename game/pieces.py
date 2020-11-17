class Piece:
    color: str
    x: int
    y: int
    points: int
    moves: list[list[tuple[int, int]]] = None

    def __init__(self, color: str, x: int, y: int, points: int):
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
    def update_moves(x: int, y: int, color: str) -> list[list[tuple[int, int]]]:
        return [[]]


class Pawn(Piece):
    POINTS = 10

    def __init__(self, color: str, x: int, y: int):
        super(Pawn, self).__init__(color, x, y, Pawn.POINTS)

    @staticmethod
    def update_moves(x: int, y: int, color: str) -> list[list[tuple[int, int]]]:
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
    POINTS = 60

    def __init__(self, color: str, x: int, y: int):
        super(Rook, self).__init__(color, x, y, Rook.POINTS)

    @staticmethod
    def update_moves(x: int, y: int, color: str) -> list[list[tuple[int, int]]]:
        move = [
            l := [],
            t := [],
            r := [],
            d := [],
        ]

        for z in range(1, 16):
            if x - z >= 0:
                l.append((x - z, y))
            if x + z <= 15:
                r.append((x + z, y))
            if y + z <= 15:
                t.append((x, y + z))
            if y - z >= 0:
                d.append((x, y - z))

        return move


class Knight(Piece):
    POINTS = 30

    def __init__(self, color: str, x: int, y: int):
        super(Knight, self).__init__(color, x, y, Knight.POINTS)

    @staticmethod
    def update_moves(x: int, y: int, color: str) -> list[list[tuple[int, int]]]:
        move = [
            tl := [],
            tr := [],
            rt := [],
            rd := [],
            dr := [],
            dl := [],
            ld := [],
            lt := [],
        ]

        if y + 2 <= 15:
            if x - 1 >= 0:
                tl.append((x - 1, y + 2))
            if x + 1 <= 15:
                tr.append((x + 1, y + 2))
        if y - 2 >= 0:
            if x - 1 >= 0:
                dl.append((x - 1, y - 2))
            if x + 1 <= 15:
                dr.append((x + 1, y - 2))
        if x + 2 <= 15:
            if y - 1 >= 0:
                rd.append((x + 2, y - 1))
            if y + 1 <= 15:
                rt.append((x + 2, y + 1))
        if x - 2 >= 0:
            if y - 1 >= 0:
                ld.append((x - 2, y - 1))
            if y + 1 <= 15:
                lt.append((x - 2, y + 1))

        return move


class Bishop(Piece):
    POINTS = 40

    def __init__(self, color: str, x: int, y: int):
        super(Bishop, self).__init__(color, x, y, Bishop.POINTS)

    @staticmethod
    def update_moves(x: int, y: int, color: str) -> list[list[tuple[int, int]]]:
        move = [
            lt := [],
            rt := [],
            rd := [],
            ld := [],
        ]

        for z in range(1, 16):
            lcheck = x - z >= 0
            rcheck = x + z <= 15
            tcheck = y + z <= 15
            dcheck = y - z >= 0
            if lcheck:
                if tcheck:
                    lt.append((x - z, y + z))
                if dcheck:
                    ld.append((x - z, y - z))
            if rcheck:
                if tcheck:
                    rt.append((x + z, y + z))
                if dcheck:
                    rd.append((x + z, y - z))

        return move


class Queen(Piece):
    POINTS = 70

    def __init__(self, color: str, x: int, y: int):
        super(Queen, self).__init__(color, x, y, Queen.POINTS)

    @staticmethod
    def update_moves(x: int, y: int, color: str) -> list[list[tuple[int, int]]]:
        move = [
            l := [],
            lt := [],
            t := [],
            rt := [],
            r := [],
            rd := [],
            d := [],
            ld := [],
        ]

        for z in range(1, 16):
            lcheck = x - z >= 0
            rcheck = x + z <= 15
            tcheck = y + z <= 15
            dcheck = y - z >= 0
            if lcheck:
                l.append((x - z, y))
                if tcheck:
                    lt.append((x - z, y + z))
                if dcheck:
                    ld.append((x - z, y - z))
            if rcheck:
                r.append((x + z, y))
                if tcheck:
                    rt.append((x + z, y + z))
                if dcheck:
                    rd.append((x + z, y - z))
            if tcheck:
                t.append((x, y + z))
            if dcheck:
                d.append((x, y - z))

        return move


class King(Piece):
    POINTS = 100

    def __init__(self, color: str, x: int, y: int):
        super(King, self).__init__(color, x, y, King.POINTS)

    @staticmethod
    def update_moves(x: int, y: int, color: str) -> list[list[tuple[int, int]]]:
        move = [
            l := [],
            lt := [],
            t := [],
            rt := [],
            r := [],
            rd := [],
            d := [],
            ld := [],
        ]

        lcheck = x - 1 >= 0
        rcheck = x + 1 <= 15
        tcheck = y + 1 <= 15
        dcheck = y - 1 >= 0
        if lcheck:
            l.append((x - 1, y))
            if tcheck:
                lt.append((x - 1, y + 1))
            if dcheck:
                ld.append((x - 1, y - 1))
        if rcheck:
            r.append((x + 1, y))
            if tcheck:
                rt.append((x + 1, y + 1))
            if dcheck:
                rd.append((x + 1, y - 1))
        if tcheck:
            t.append((x, y + 1))
        if dcheck:
            d.append((x, y - 1))

        return move


class Blank(Piece):
    def __init__(self, x, y):
        super(Blank, self).__init__('', x, y, 0)
