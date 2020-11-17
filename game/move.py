class Move:
    from_x: int
    from_y: int
    to_x: int
    to_y: int
    # piece: Piece
    # board: Board
    weight: float

    def __init__(
            self,
            from_x,
            from_y,
            to_x,
            to_y,
            piece,
            board,
            points,
    ):
        self.from_x = from_x
        self.from_y = from_y
        self.to_x = to_x
        self.to_y = to_y
        self.piece = piece
        self.board = board
        self.weight = points

    def execute(self):
        self.board.move(self.piece, self.to_x, self.to_y)

    def to_coords(self):
        return self.from_y, self.from_x, self.to_y, self.to_x
