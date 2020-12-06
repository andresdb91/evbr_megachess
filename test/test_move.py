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

    @parameterized.expand([
        ((2, 2, 2, 3, pieces.Pawn, 10, 'black'), False),
        ((2, 13, 2, 12, pieces.Pawn, 10, 'white'), False),
        ((7, 6, 7, 7, pieces.Pawn, 510, 'black'), True),
        ((7, 9, 7, 8, pieces.Pawn, 510, 'white'), True),
    ])
    def test_execute(self, move_data, should_promote):
        move = Move(*move_data)
        from_piece_pre_move = self.test_board.get_piece(move.from_x, move.from_y)
        move.execute(self.test_board)
        from_piece_post_move = self.test_board.get_piece(move.from_x, move.from_y)
        to_piece_post_move = self.test_board.get_piece(move.to_x, move.to_y)
        self.assertEqual(from_piece_post_move, pieces.Blank)

        if should_promote:
            self.assertEqual(from_piece_pre_move, pieces.Pawn)
            self.assertEqual(to_piece_post_move, pieces.Queen)
        else:
            self.assertEqual(from_piece_pre_move, to_piece_post_move)
