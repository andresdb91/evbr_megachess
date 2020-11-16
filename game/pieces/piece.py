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
        self.moves = []
        self.update_moves()

    def move(self, x: int, y: int):
        self.x = x
        self.y = y
        self.update_moves()

    def get_moves(self) -> [(int, int)]:
        return self.moves

    def update_moves(self):
        pass
