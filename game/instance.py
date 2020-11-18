from game.strategies import BaseStrategy
from game.strategies_fact import AIStrategyFactory
from game.board import Board
from game.move import Move

from datetime import datetime
from server_websocket import ServerWebsocketAdap


class GameInstance:

    config = {}
    board_id: str
    player: str
    opponent: str
    color: str
    strategy: BaseStrategy
    board: Board
    start: datetime
    end: datetime
    move_history: list[Move]
    save_history: bool

    last_move: datetime

    def __init__(
            self,
            config: dict,
            board_id: str,
            opponent: str,
            color: str,
            board: str
    ):
        self.config = config.copy()
        self.board_id = board_id
        self.opponent = opponent
        self.color = color
        self.strategy = AIStrategyFactory.get_strategy(self.config.get('ai_strategy', 'random_legal'))
        self.board = Board(board)
        self.start = datetime.now()
        self.save_history = True
        self.move_history = []

    async def play(self, turn_token: str, server: ServerWebsocketAdap, color: str, board: str = None):
        if board:
            opponent_move = self.board.update(board, color)
            if self.save_history:
                if opponent_move.points != 0:
                    self.move_history.append(opponent_move)
                else:
                    self.save_history = False
                    self.move_history = []

        move = self.strategy.play(self, self.board, color)
        move.execute()
        if self.save_history:
            self.move_history.append(move)

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
