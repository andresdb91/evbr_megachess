from game.pieces.piece import Piece


class Pawn(Piece):
    POINTS = 10

    def __init__(self, color, x, y):
        super(Pawn, self).__init__(color, x, y, Pawn.POINTS)

    def update_moves(self):
        if self.color == 'white':
            y0 = [2, 3]
            direction = 1
        else:
            y0 = [12, 13]
            direction = -1

        self.moves.append((self.x, self.y + direction))

        if self.y in y0:
            self.moves.append((self.x, self.y + 2*direction))
