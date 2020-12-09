import unittest
from parameterized import parameterized

from game import board
from game.strategy import AIStrategy


class TestAIStrategy(unittest.IsolatedAsyncioTestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.input_board = 'r h b qqkk b h r' \
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
                          'R H B QQKK B H R'

    def setUp(self) -> None:
        self.test_board = board.Board(self.input_board)
        self.strategy = AIStrategy()

    @parameterized.expand([
        ('white', 1),
        ('black', 1),
    ])
    def test_play(self, color, moves_left):
        move = self.strategy.play(self.test_board, color, moves_left)
        self.assertTrue(move.is_valid())
