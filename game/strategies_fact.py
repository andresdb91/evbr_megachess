import game.strategies


class AIStrategyFactory:
    default_strategy = game.strategies.RandomLegal

    @staticmethod
    def get_strategy(name: str) -> game.strategies.BaseStrategy:
        if name == 'random_legal':
            return game.strategies.RandomLegal()
        else:
            return AIStrategyFactory.default_strategy()
