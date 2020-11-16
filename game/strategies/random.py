from random import randint
from game.strategies.base_strat import BaseStrategy


class RandomStrategy(BaseStrategy):
    @staticmethod
    def play(board):
        return randint(0, 15), randint(0, 15), randint(0, 15), randint(0, 15)
