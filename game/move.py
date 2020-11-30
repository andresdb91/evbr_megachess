class Move:
    from_x: int
    from_y: int
    to_x: int
    to_y: int
    piece: 'Piece'
    points: int
    color: str

    def __init__(
            self,
            from_x: int = 0,
            from_y: int = 0,
            to_x: int = 0,
            to_y: int = 0,
            piece: 'Piece' = None,
            points: int = 0,
            color: str = '',
    ):
        self.from_x = from_x
        self.from_y = from_y
        self.to_x = to_x
        self.to_y = to_y
        self.piece = piece
        self.points = points
        self.color = color

    def execute(self, board):
        board.move(self.from_x, self.from_y, self.to_x, self.to_y)

    def undo(self, board):
        is_pawn = self.piece.is_piece_str('p')
        board.move(self.to_x, self.to_y, self.from_x, self.from_y, unpromote=is_pawn)

    def to_coords(self) -> tuple[int, int, int, int]:
        return self.from_x, self.from_y, self.to_x, self.to_y

    def is_valid(self) -> bool:
        return self.points > 0
