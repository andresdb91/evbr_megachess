from game.strategy import AIStrategy
from game.move import Move
from game import pieces


class MockAIStrategy(AIStrategy):
    def play(self, board, color, moves_left):
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
