import unittest
from parameterized import parameterized

from game.board import Board
from game.board import BoardDesyncException


class TestBoard(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.input_board = 'r h b q k       ' \
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
                          'R H B Q K       '

    def setUp(self) -> None:
        self.board = Board(self.input_board)

    def test_build_board(self):
        expected_board = [
            ['r', ' ', 'h', ' ', 'b', ' ', 'q', ' ', 'k', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
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
            ['R', ' ', 'H', ' ', 'B', ' ', 'Q', ' ', 'K', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        ]

        board = Board.build_board(self.input_board)
        self.assertEqual(board, expected_board)

    def test_to_char_array(self):
        expected = list(self.input_board)
        self.assertEqual(self.board.to_char_array(), expected)

    @parameterized.expand([
        (
            'r h b q k       '
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
            'R H B Q K       ',
            'black',
            (3, 2, 3, 3),
        ),
        (
            'r h b q k       '
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
            'R H B Q K       ',
            'white',
            (3, 13, 3, 12),
        ),
    ])
    def test_update_board(self, modified_board, color, expected_move):
        move = self.board.update(modified_board, color)
        move_coords = move.to_coords()
        self.assertEqual(move_coords, expected_move)

    @parameterized.expand([
        (
                'r h b q k       '
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
                'R H B Q K       ',
        ),
    ])
    def test_update_board_exception(self, desynchronized_board):
        self.assertRaises(
            BoardDesyncException,
            self.board.update,
            desynchronized_board,
            'white',
        )
