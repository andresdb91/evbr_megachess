from game.strategies import BaseStrategy
from game.strategies_fact import AIStrategyFactory
from game.board import Board


class GameInstance:

    config = {}
    board_id: str
    opponent: str
    move_left: str
    color: str
    strategy: BaseStrategy
    board: Board

    def __init__(self, config, board_id, opponent, move_left, color, board):
        self.config = config.copy()
        self.board_id = board_id
        self.opponent = opponent
        self.move_left = move_left
        self.color = color
        self.strategy = AIStrategyFactory.get_strategy(self.config.get('ai_strategy', 'random_legal'))
        self.board = Board(board)

    async def play(self, turn_token, server, color, board=None):
        if board:
            self.board.update(board)

        move = self.strategy.play(self, self.board, color)
        move.execute()
        x1, y1, x2, y2 = move.to_coords()

        await server.send(
            'move',
            {
                'board_id': self.board_id,
                'turn_token': turn_token,
                'from_row': y1,
                'from_col': x1,
                'to_row': y2,
                'to_col': x2,
            }
        )
