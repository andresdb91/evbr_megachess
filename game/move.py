class Move:
    from_x: int
    from_y: int
    to_x: int
    to_y: int
    # piece: 'Piece'
    board: 'Board'
    points: int

    def __init__(
            self,
            from_x: int = 0,
            from_y: int = 0,
            to_x: int = 0,
            to_y: int = 0,
            # piece: 'Piece' = None,
            board: 'Board' = None,
            points: int = 0,
    ):
        self.from_x = from_x
        self.from_y = from_y
        self.to_x = to_x
        self.to_y = to_y
        # self.piece = piece
        self.board = board
        self.points = points

    def execute(self, board=None):
        if board:
            board.move(self.from_x, self.from_y, self.to_x, self.to_y)
        else:
            self.board.move(self.from_x, self.from_y, self.to_x, self.to_y)

    def to_coords(self) -> tuple[int, int, int, int]:
        return self.from_x, self.from_y, self.to_x, self.to_y

    def get_piece(self):
        return self.board.current[self.from_y][self.from_x]