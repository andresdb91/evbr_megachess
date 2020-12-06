import game.strategies


class AIStrategyFactory:
    default_strategy: str = 'random_legal'

    strategies = {
        'random_legal': game.strategies.RandomLegal,
        'maximum_points': game.strategies.MaximumPointMove,
        'maximum_weight': game.strategies.MaximumWeight,
        'pawns_and_queens': game.strategies.OnlyPawnsAndQueensByWeight,
        '2_move_weight': game.strategies.TwoMoveWeighting,
        'multi_move_weight': game.strategies.MultiMoveWeight,
    }

    @staticmethod
    def get_strategy(name: str) -> game.strategies.BaseStrategy:
        if name not in AIStrategyFactory.strategies.keys():
            name = AIStrategyFactory.default_strategy
        print(f'Using strategy: {name}')

        return AIStrategyFactory.strategies[name]()
