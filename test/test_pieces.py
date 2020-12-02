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

    @parameterized.expand(
        [
            (
                  'p',
                  True,
            ),
            (
                  'P',
                  True,
            ),
        ] + [(p, False) for p in [
            'r', 'h', 'b', 'q', 'k',
            'R', 'H', 'B', 'Q', 'K',
        ]],
    )
    def test_is_piece(self, piece, expected):
        result = game.pieces.Pawn.is_piece(piece)
        self.assertEqual(result, expected)

    @parameterized.expand([
        ('p', 'white', True),
        ('p', 'black', False),
        ('P', 'white', False),
        ('P', 'black', True),
    ])
    def test_is_opponent(self, piece, color, expected):
        result = game.pieces.Pawn.is_opponent(piece, color)
        self.assertEqual(result, expected)
