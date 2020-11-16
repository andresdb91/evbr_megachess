from game.strategies.base_strat import BaseStrategy
from game.strategies.random import RandomStrategy


class AIStrategyFactory:
    @staticmethod
    def get_strategy(name: str) -> BaseStrategy:
        if name == 'random':
            return RandomStrategy()
