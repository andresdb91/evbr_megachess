from game.strategy import AIStrategy
from game.board import Board
from game.board import BoardDesyncException
from game.move import Move
from config_manager import ConfigManager
from datetime import datetime
from server.server_adap import BaseServerAdapter


class GameInstance:

    board_id: str
    player: str
    opponent: str
    color: str
    strategy: AIStrategy
    board: Board
    start: datetime
    end: datetime
    move_history: list[Move]
    save_history: bool

    last_move: datetime

    def __init__(
            self,
            board_id: str,
            opponent: str,
            color: str,
            board: str,
            strategy: AIStrategy,
    ):
        self.player = ConfigManager.get('username') or ''
        self.board_id = board_id
        self.opponent = opponent
        self.color = color
        self.strategy = strategy
        self.board = Board(board)
        self.start = datetime.now()
        self.save_history = True
        self.move_history = []

    async def play(self, turn_token: str, server: BaseServerAdapter, color: str, board: str = None):
        if board and self.player != self.opponent:
            opponent_color = 'white' if color != 'white' else 'black'
            try:
                opponent_move = self.board.update(board, opponent_color)
                if opponent_move.is_valid():
                    opponent_move.execute(self.board)
            except BoardDesyncException:
                if self.save_history:
                    print('Disabling move history for this game')
                    self.save_history = False
                    self.move_history = []
            else:
                if self.save_history:
                    self.move_history.append(opponent_move)

        # from datetime import datetime
        # pre = datetime.now()
        move = self.strategy.play(self.board, color)
        # post = datetime.now() - pre
        # print(f'Time to play: {post.microseconds/1000} ms')

        move.execute(self.board)
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

        if ConfigManager.get('print_match'):
            print(f'{color} vs {self.opponent}:')
            for row in self.board.current:
                print(row)
            print()
