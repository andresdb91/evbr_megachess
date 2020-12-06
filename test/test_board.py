import unittest
from parameterized import parameterized

from game.board import Board


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
