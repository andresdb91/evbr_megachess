from game.strategies import BaseStrategy
from game.move import Move
from game import pieces


class MockAIStrategy(BaseStrategy):
    def play(self, instance, board, color):
        if color == 'black':
            return Move(
                2,
                2,
                2,
                3,
                pieces.Pawn,
                10,
                'black'
            )
        else:
            return Move(
                2,
                13,
                2,
                12,
                pieces.Pawn,
                10,
                'white'
            )
