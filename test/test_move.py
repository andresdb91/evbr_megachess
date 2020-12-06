import unittest
from parameterized import parameterized

from game import board
from game import pieces
from game.move import Move


class TestMove(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.test_board_str = '                ' \
                             '                ' \
                             'ppppppp         ' \
                             '                ' \
                             '                ' \
                             '                ' \
                             '       p        ' \
                             '                ' \
                             '                ' \
                             '       P        ' \
                             '                ' \
                             '                ' \
                             '                ' \
                             'PPPPPPP         ' \
                             '                ' \
                             '                '

    def setUp(self) -> None:
        self.test_board = board.Board(self.test_board_str)
