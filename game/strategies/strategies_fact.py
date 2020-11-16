from game.strategies.base_strat import BaseStrategy
from game.strategies.random_legal import RandomLegal


class AIStrategyFactory:
    default_strategy = RandomLegal

    @staticmethod
    def get_strategy(name: str) -> BaseStrategy:
        if name == 'random_legal':
            return RandomLegal()
        else:
            return AIStrategyFactory.default_strategy()
