import game.strategies


class AIStrategyFactory:
    default_strategy: game.strategies.BaseStrategy = game.strategies.RandomLegal

    @staticmethod
    def get_strategy(name: str) -> game.strategies.BaseStrategy:
        print(f'Using strategy: {name}')
        if name == 'random_legal':
            return game.strategies.RandomLegal()
        elif name == 'maximum_points_move':
            return game.strategies.MaximumPointMove()
        elif name == 'maximum_weight':
            return game.strategies.MaximumWeight()
        elif name == 'pawns_and_queens':
            return game.strategies.OnlyPawnsAndQueensByWeight()
        elif name == '2_move_weight':
            return game.strategies.TwoMoveWeighting()
        elif name == 'multi_move_weight':
            return game.strategies.MultiMoveWeight()
        else:
            return AIStrategyFactory.default_strategy()
