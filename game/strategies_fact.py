import game.strategies


class AIStrategyFactory:
    default_strategy = game.strategies.RandomLegal

    @staticmethod
    def get_strategy(name: str) -> game.strategies.BaseStrategy:
        if name == 'random_legal':
            return game.strategies.RandomLegal()
        elif name == 'maximum_points_move':
            return game.strategies.MaximumPointMove()
        elif name == 'maximum_weight':
            return game.strategies.MaximumWeight()
        else:
            return AIStrategyFactory.default_strategy()
