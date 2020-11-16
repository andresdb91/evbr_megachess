from game.strategies.base_strat import BaseStrategy

from random import randint


class RandomLegal(BaseStrategy):

    @staticmethod
    def play(instance, board, color):
        moves = board.get_moves(color)

        pick = moves[randint(0, len(moves)-1)]
        print(f'Move: x:{pick.from_x}->{pick.to_x}, y:{pick.from_y}->{pick.to_y}')
        return pick
