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
