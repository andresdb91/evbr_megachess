import unittest
from parameterized import parameterized

import game.pieces


class TestPawn(unittest.TestCase):

    @parameterized.expand([
        (
            7,
            3,
            [['p' if x == 7 else ' ' for x in range(16)] if y == 3 else [' ' for x in range(16)] for y in range(16)],
            'black',
            [
                (7, 4),
                (7, 5),
            ],
            [
                (7, 6),
                (7, 3),
                (7, 2),
                (6, 4),
                (8, 4),
            ],
        ),
    ])
    def test_update_moves(self, x, y, board, color, valid, invalid):
        moves = game.pieces.Pawn.update_moves(x, y, board, color)
        for move in moves:
            self.assertIn((move.to_x, move.to_y), valid)
            self.assertNotIn((move.to_x, move.to_y), invalid)
