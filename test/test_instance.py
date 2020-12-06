import unittest
from parameterized import parameterized

from game.instance import GameInstance
from config_manager import ConfigManager
from test.mock_server_adap import MockServerAdapter
from test.mock_strategies import MockAIStrategy


class TestInstance(unittest.IsolatedAsyncioTestCase):
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
        cls.opponent = 'test_opponent'
        cls.board_id = 'abcde12345'
        cls.color = 'white'
        ConfigManager({})
        ConfigManager.set('username', 'test_player')
        cls.server = MockServerAdapter()
        cls.strategy = MockAIStrategy()

    def setUp(self) -> None:
        self.instance = GameInstance(
            self.board_id,
            self.opponent,
            self.color,
            self.input_board,
            self.strategy,
        )

    @parameterized.expand([
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
            'black',
            (
                'move',
                {
                    'board_id': 'abcde12345',
                    'turn_token': '12345',
                    'from_row': 2,
                    'from_col': 2,
                    'to_row': 3,
                    'to_col': 2,
                }
            ),
        ),
        (
            '                '
            '                '
            'pppppp          '
            '      p         '
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
            (
                'move',
                {
                    'board_id': 'abcde12345',
                    'turn_token': '12345',
                    'from_row': 13,
                    'from_col': 2,
                    'to_row': 12,
                    'to_col': 2,
                }
            ),
        ),
        (
            '                '
            '                '
            'pppppp          '
            '      p         '
            '                '
            '                '
            '       p        '
            '                '
            '                '
            '       P        '
            '                '
            '                '
            '      P         '
            'PPPPPP          '
            '                '
            '                ',
            'black',
            (
                'move',
                {
                    'board_id': 'abcde12345',
                    'turn_token': '12345',
                    'from_row': 2,
                    'from_col': 2,
                    'to_row': 3,
                    'to_col': 2,
                }
            ),
        ),
        (
            '',
            'black',
            (
                'move',
                {
                    'board_id': 'abcde12345',
                    'turn_token': '12345',
                    'from_row': 2,
                    'from_col': 2,
                    'to_row': 3,
                    'to_col': 2,
                }
            ),
        ),
    ])
    async def test_play(self, board, color, expected_send):
        await self.instance.play('12345', self.server, color, board)
        self.assertEqual(self.server.test_send, expected_send)
