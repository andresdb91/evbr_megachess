import unittest
from parameterized import parameterized

from game.board import Board
from game.board import BoardDesyncException


class TestBoard(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.input_board = '                ' \
                          '                ' \
                          'pppppppp        ' \
                          '                ' \
                          '                ' \
                          '                ' \
                          '                ' \
                          '                ' \
                          '                ' \
                          '                ' \
                          '                ' \
                          '                ' \
                          '                ' \
                          'PPPPPPPP        ' \
                          '                ' \
                          '                '

    def setUp(self) -> None:
        self.board = Board(self.input_board)

    def test_build_board(self):
        expected_board = [
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        ]

        board = Board.build_board(self.input_board)
        self.assertEqual(board, expected_board)

    def test_to_char_array(self):
        expected = list(self.input_board)
        self.assertEqual(self.board.to_char_array(), expected)

    @parameterized.expand([
        (
            '                '
            '                '
            'ppp pppp        '
            '   p            '
            '                '
            '                '
            '                '
            '                '
            '                '
            '                '
            '                '
            '                '
            '                '
            'PPPPPPPP        '
            '                '
            '                ',
            'black',
            (3, 2, 3, 3),
            10,
        ),
        (
            '                '
            '                '
            'pppppppp        '
            '                '
            '                '
            '                '
            '                '
            '                '
            '                '
            '                '
            '                '
            '                '
            '   P            '
            'PPP PPPP        '
            '                '
            '                ',
            'white',
            (3, 13, 3, 12),
            10,
        ),
        (
            '                '
            '                '
            'pppppppp        '
            '                '
            '                '
            '                '
            '                '
            '                '
            '                '
            '                '
            '                '
            '                '
            '                '
            'PPPPPPPP        '
            '                '
            '                ',
            'white',
            (0, 0, 0, 0),
            -20,
        ),
    ])
    def test_update_board(self, modified_board, color, expected_move, points):
        move = self.board.update(modified_board, color)
        self.assertEqual(move.to_coords(), expected_move)
        self.assertEqual(move.points, points)

    @parameterized.expand([
        (
                '                '
                '                '
                'ppp pppp        '
                '   p            '
                '                '
                '                '
                '                '
                '                '
                '                '
                '                '
                '                '
                '                '
                '   P            '
                'PPP PPPP        '
                '                '
                '                ',
        ),
    ])
    def test_update_board_exception(self, desynchronized_board):
        self.assertRaises(
            BoardDesyncException,
            self.board.update,
            desynchronized_board,
            'white',
        )

    @parameterized.expand([
        (
            'white',
            [
                (0, 13, 0, 12),
                (1, 13, 1, 12),
                (2, 13, 2, 12),
                (3, 13, 3, 12),
                (4, 13, 4, 12),
                (5, 13, 5, 12),
                (6, 13, 6, 12),
                (7, 13, 7, 12),
                (0, 13, 0, 11),
                (1, 13, 1, 11),
                (2, 13, 2, 11),
                (3, 13, 3, 11),
                (4, 13, 4, 11),
                (5, 13, 5, 11),
                (6, 13, 6, 11),
                (7, 13, 7, 11),
            ]
        ),
        (
            'black',
            [
                (0, 2, 0, 3),
                (1, 2, 1, 3),
                (2, 2, 2, 3),
                (3, 2, 3, 3),
                (4, 2, 4, 3),
                (5, 2, 5, 3),
                (6, 2, 6, 3),
                (7, 2, 7, 3),
                (0, 2, 0, 4),
                (1, 2, 1, 4),
                (2, 2, 2, 4),
                (3, 2, 3, 4),
                (4, 2, 4, 4),
                (5, 2, 5, 4),
                (6, 2, 6, 4),
                (7, 2, 7, 4),
            ]
        ),
    ])
    def test_get_moves(self, color, expected_moves):
        moves = self.board.get_moves(color)
        moves_as_coords = [m.to_coords() for m in moves]
        self.assertCountEqual(moves_as_coords, expected_moves)
