import unittest
from parameterized import parameterized

from game.pieces import *


class TestPieces(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.board = [
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', 'P', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'p', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'P', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', 'p', ' ', 'p', 'P', 'P', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', 'p', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', 'P', ' ', ' ', 'p', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', 'P', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', 'p', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', 'P', ' ', 'P', 'p', 'p', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        ]

    @parameterized.expand([
        (
            Pawn,
            7,
            3,
            'black',
            [
                (7, 4),
                (7, 5),
            ],
        ),
        (
            Pawn,
            7,
            12,
            'white',
            [
                (7, 11),
                (7, 10),
            ],
        ),
    ])
    def test_update_moves(self, piece, x, y, color, valid):
        moves = piece.update_moves(x, y, self.board, color)
        for move in moves:
            self.assertIn((move.to_x, move.to_y), valid)

    @parameterized.expand(
        [
            (
                Pawn,
                'p',
                True,
            ),
            (
                Pawn,
                'P',
                True,
            ),
        ] + [(Pawn, p, False) for p in [
            'r', 'h', 'b', 'q', 'k',
            'R', 'H', 'B', 'Q', 'K',
        ]],
    )
    def test_is_piece(self, piece, piece_char, expected):
        result = piece.is_piece(piece_char)
        self.assertEqual(result, expected)

    @parameterized.expand([
        ('p', 'white', True),
        ('r', 'black', False),
        ('Q', 'white', False),
        ('B', 'black', True),
    ])
    def test_is_opponent(self, piece, color, expected):
        result = Piece.is_opponent(piece, color)
        self.assertEqual(result, expected)

    @parameterized.expand([
        ('p', (Pawn, 'black')),
        ('P', (Pawn, 'white')),
        ('r', (Rook, 'black')),
        ('R', (Rook, 'white')),
        ('q', (Queen, 'black')),
        ('Q', (Queen, 'white')),
        ('k', (King, 'black')),
        ('K', (King, 'white')),
        (' ', (Blank, '')),
    ])
    def test_get_piece(self, piece_char, expected):
        result = Piece.get_piece(piece_char)
        self.assertEqual(result, expected)
