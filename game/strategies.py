from random import randint


class BaseStrategy:
    @staticmethod
    def play(instance, board, color):
        pass


class RandomLegal(BaseStrategy):
    @staticmethod
    def play(instance, board, color):
        moves = board.get_moves(color)

        pick = moves[randint(0, len(moves)-1)]
        print(f'Move: x:{pick.from_x}->{pick.to_x}, y:{pick.from_y}->{pick.to_y}')
        return pick


class MaximumWeight(BaseStrategy):
    @staticmethod
    def play(instance, board, color):
        moves = board.get_moves(color)
        best_move = None

        for m in moves:
            if best_move is None or m.weight > best_move.weight:
                best_move = m

        return best_move
