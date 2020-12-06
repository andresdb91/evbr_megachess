import unittest
from parameterized import parameterized

from game.pieces import *


class TestPieces(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.board = [
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', 'p', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'p', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'P', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', 'P', ' ', 'P', 'p', 'p', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', 'p', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', 'p', ' ', ' ', 'P', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', 'p', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', 'P', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', 'p', ' ', 'p', 'P', 'P', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        ]

    @parameterized.expand([
        # Black pawn
        # 00
        (
            Pawn,
            2,
            3,
            'black',
            [
                (2, 4),
                (2, 5),
            ],
        ),
        # 01
        (
            Pawn,
            2,
            4,
            'black',
            [
                (2, 5),
            ],
        ),
        # 02
        (
            Pawn,
            6,
            3,
            'black',
            [
                (6, 4),
                (5, 4),
                (7, 4),
            ],
        ),
        # 03
        (
            Pawn,
            7,
            3,
            'black',
            [],
        ),
        # 04
        (
            Pawn,
            8,
            3,
            'black',
            [
                (7, 4),
            ],
        ),
        # White pawn
        # 05
        (
            Pawn,
            2,
            12,
            'white',
            [
                (2, 11),
                (2, 10),
            ],
        ),
        # 06
        (
            Pawn,
            2,
            11,
            'white',
            [
                (2, 10),
            ],
        ),
        # 07
        (
            Pawn,
            6,
            12,
            'white',
            [
                (6, 11),
                (5, 11),
                (7, 11),
            ],
        ),
        # 08
        (
            Pawn,
            7,
            12,
            'white',
            [],
        ),
        # 09
        (
            Pawn,
            8,
            12,
            'white',
            [
                (7, 11),
            ],
        ),
        # Rook
        # 10
        (
            Rook,
            2,
            4,
            'white',
            [
                (2, 0),
                (2, 1),
                (2, 2),
                (2, 3),
                (2, 5),
                (2, 6),
                (2, 7),
                (0, 4),
                (1, 4),
                (3, 4),
                (4, 4),
            ],
        ),
        # 11
        (
            Rook,
            2,
            4,
            'black',
            [
                (2, 0),
                (2, 1),
                (2, 2),
                (2, 3),
                (2, 5),
                (2, 6),
                (0, 4),
                (1, 4),
                (3, 4),
                (4, 4),
                (5, 4),
            ],
        ),
        # Knight
        # 12
        (
            Knight,
            2,
            4,
            'black',
            [
                (0, 3),
                (0, 5),
                (4, 3),
                (4, 5),
                (1, 2),
                (3, 2),
                (1, 6),
                (3, 6),
            ],
        ),
        # 13
        (
            Knight,
            14,
            1,
            'black',
            [
                (12, 0),
                (15, 3),
                (13, 3),
            ],
        ),
        # 14
        (
            Knight,
            14,
            1,
            'white',
            [
                (12, 0),
                (15, 3),
                (12, 2),
            ],
        ),
        # Bishop
        # 15
        (
            Bishop,
            2,
            4,
            'black',
            [
                (1, 3),
                (0, 2),
                (3, 5),
                (4, 6),
                (5, 7),
                (3, 3),
                (4, 2),
                (1, 5),
                (0, 6),
            ],
        ),
        # 16
        (
            Bishop,
            2,
            4,
            'white',
            [
                (1, 3),
                (0, 2),
                (3, 5),
                (4, 6),
                (3, 3),
                (4, 2),
                (5, 1),
                (1, 5),
                (0, 6),
            ],
        ),
        # 17
        (
            Queen,
            2,
            4,
            'black',
            [
                (1, 3),
                (0, 2),
                (3, 5),
                (4, 6),
                (5, 7),
                (3, 3),
                (4, 2),
                (1, 5),
                (0, 6),
                (2, 0),
                (2, 1),
                (2, 2),
                (2, 3),
                (2, 5),
                (2, 6),
                (0, 4),
                (1, 4),
                (3, 4),
                (4, 4),
                (5, 4),
            ],
        ),
        # 18
        (
            Queen,
            2,
            4,
            'white',
            [
                (1, 3),
                (0, 2),
                (3, 5),
                (4, 6),
                (3, 3),
                (4, 2),
                (5, 1),
                (1, 5),
                (0, 6),
                (2, 0),
                (2, 1),
                (2, 2),
                (2, 3),
                (2, 5),
                (2, 6),
                (2, 7),
                (0, 4),
                (1, 4),
                (3, 4),
                (4, 4),
            ],
        ),
    ])
    def test_update_moves(self, piece, x, y, color, valid):
        moves = piece.update_moves(x, y, self.board, color)
        self.assertEqual(len(moves), len(valid))
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
