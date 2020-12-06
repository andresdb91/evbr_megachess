import unittest
from parameterized import parameterized

from game.board import Board
from game.board import BoardDesyncException
from game import pieces


class TestBoard(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.input_board = '                ' \
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
        self.board = Board(self.input_board)

    def test_build_board(self):
        expected_board = [
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            ['p', 'p', 'p', 'p', 'p', 'p', 'p', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', 'p', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', 'P', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            ['P', 'P', 'P', 'P', 'P', 'P', 'P', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
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
            'ppp ppp         '
            '   p            '
            '                '
            '                '
            '       p        '
            '                '
            '                '
            '       P        '
            '                '
            '                '
            '                '
            'PPPPPPP         '
            '                '
            '                ',
            'black',
            (3, 2, 3, 3),
            10,
        ),
        (
            '                '
            '                '
            'ppppppp         '
            '                '
            '                '
            '                '
            '       p        '
            '                '
            '                '
            '       P        '
            '                '
            '                '
            '   P            '
            'PPP PPP         '
            '                '
            '                ',
            'white',
            (3, 13, 3, 12),
            10,
        ),
        (
            '                '
            '                '
            'ppppppp         '
            '                '
            '                '
            '                '
            '       p        '
            '                '
            '                '
            '       P        '
            '                '
            '                '
            '                '
            'PPPPPPP         '
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
                'ppp ppp         '
                '   p            '
                '                '
                '                '
                '       p        '
                '                '
                '                '
                '       P        '
                '                '
                '                '
                '   P            '
                'PPP PPP         '
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
                (7, 9, 7, 8),
                (0, 13, 0, 11),
                (1, 13, 1, 11),
                (2, 13, 2, 11),
                (3, 13, 3, 11),
                (4, 13, 4, 11),
                (5, 13, 5, 11),
                (6, 13, 6, 11),
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
                (7, 6, 7, 7),
                (0, 2, 0, 4),
                (1, 2, 1, 4),
                (2, 2, 2, 4),
                (3, 2, 3, 4),
                (4, 2, 4, 4),
                (5, 2, 5, 4),
                (6, 2, 6, 4),
            ]
        ),
    ])
    def test_get_moves(self, color, expected_moves):
        moves = self.board.get_moves(color)
        moves_as_coords = [m.to_coords() for m in moves]
        self.assertCountEqual(moves_as_coords, expected_moves)

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
                (7, 9, 7, 8),
                (0, 13, 0, 11),
                (1, 13, 1, 11),
                (2, 13, 2, 11),
                (3, 13, 3, 11),
                (4, 13, 4, 11),
                (5, 13, 5, 11),
                (6, 13, 6, 11),
            ],
            [
                (0, 2, 0, 3),
                (1, 2, 1, 3),
                (2, 2, 2, 3),
                (3, 2, 3, 3),
                (4, 2, 4, 3),
                (5, 2, 5, 3),
                (6, 2, 6, 3),
                (7, 6, 7, 7),
                (0, 2, 0, 4),
                (1, 2, 1, 4),
                (2, 2, 2, 4),
                (3, 2, 3, 4),
                (4, 2, 4, 4),
                (5, 2, 5, 4),
                (6, 2, 6, 4),
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
                (7, 6, 7, 7),
                (0, 2, 0, 4),
                (1, 2, 1, 4),
                (2, 2, 2, 4),
                (3, 2, 3, 4),
                (4, 2, 4, 4),
                (5, 2, 5, 4),
                (6, 2, 6, 4),
            ],
            [
                (0, 13, 0, 12),
                (1, 13, 1, 12),
                (2, 13, 2, 12),
                (3, 13, 3, 12),
                (4, 13, 4, 12),
                (5, 13, 5, 12),
                (6, 13, 6, 12),
                (7, 9, 7, 8),
                (0, 13, 0, 11),
                (1, 13, 1, 11),
                (2, 13, 2, 11),
                (3, 13, 3, 11),
                (4, 13, 4, 11),
                (5, 13, 5, 11),
                (6, 13, 6, 11),
            ]
        ),
    ])
    def test_get_all_moves(self, color, expected_player_moves, expected_opponent_moves):
        raw_player_moves, raw_opponent_moves = self.board.get_all_moves(color)
        player_moves = [m.to_coords() for m in raw_player_moves]
        opponent_moves = [m.to_coords() for m in raw_opponent_moves]
        self.assertCountEqual(player_moves, expected_player_moves)
        self.assertCountEqual(opponent_moves, expected_opponent_moves)

    @parameterized.expand([
        (2, 2, pieces.Pawn),
        (4, 4, pieces.Blank),
    ])
    def test_get_piece(self, x, y, expected_piece):
        piece = self.board.get_piece(x, y)
        self.assertEqual(piece, expected_piece)

    @parameterized.expand([
        (2, 2, False),
        (4, 4, True),
    ])
    def test_is_empty(self, x, y, expected):
        result = self.board.is_empty(x, y)
        self.assertEqual(result, expected)

    @parameterized.expand([
        (2, 2, 2, 4, False),
        (7, 6, 7, 7, True),
        (7, 9, 7, 8, True),
    ])
    def test_move(self, from_x, from_y, to_x, to_y, should_promote):
        from_piece_pre_move = self.board.get_piece(from_x, from_y)
        self.board.move(from_x, from_y, to_x, to_y)

        from_piece_post_move = self.board.get_piece(from_x, from_y)
        to_piece_post_move = self.board.get_piece(to_x, to_y)

        self.assertEqual(from_piece_post_move, pieces.Blank)
        if should_promote:
            self.assertEqual(from_piece_pre_move, pieces.Pawn)
            self.assertEqual(to_piece_post_move, pieces.Queen)
        else:
            self.assertEqual(from_piece_pre_move, to_piece_post_move)

    @parameterized.expand([
        (2, 2, 2, 4, False),
        (7, 6, 7, 7, True),
        (7, 9, 7, 8, True),
    ])
    def test_undo_move(self, from_x, from_y, to_x, to_y, should_unpromote):
        from_piece_pre_move = self.board.get_piece(from_x, from_y)
        to_piece_pre_move = self.board.get_piece(to_x, to_y)

        self.board.move(from_x, from_y, to_x, to_y)
        self.board.move(to_x, to_y, from_x, from_y, unpromote=should_unpromote)

        from_piece_post_move = self.board.get_piece(from_x, from_y)
        to_piece_post_move = self.board.get_piece(to_x, to_y)

        self.assertEqual(from_piece_pre_move, from_piece_post_move)
        self.assertEqual(to_piece_pre_move, to_piece_post_move)
