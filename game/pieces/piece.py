class Piece:
    color: str
    x: int
    y: int
    points: int
    moves: [(int, int)]

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
        self.update_moves()

    def get_moves(self) -> [(int, int)]:
        return self.moves

    def update_moves(self):
        pass

    @classmethod
    def update_default_moves(cls):
        pass
