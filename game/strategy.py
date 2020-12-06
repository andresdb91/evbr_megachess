from game.board import Board
from game.move import Move


class AIStrategy:
    starting_depth: int = 2

    def play(self, board: Board, color: str) -> Move:
        moves = board.get_moves(color)
        return moves[0]
