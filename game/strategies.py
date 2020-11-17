from random import randint
from random import shuffle
from game import pieces

from game.board import Board
from game.move import Move

WHITE_PROMOTE = 8
BLACK_PROMOTE = 7

PROMOTE_BONUS = 500
CENTRAL_POSITION_BONUS = 50


class BaseStrategy:
    def play(self, instance: 'GameInstance', board: Board, color: str) -> Move:
        pass

    def weight_move(self, board: Board, color: str, move: Move) -> int:
        return 0


class RandomLegal(BaseStrategy):
    def play(self, instance: 'GameInstance', board: Board, color: str) -> Move:
        moves = board.get_moves(color)

        pick = moves[randint(0, len(moves)-1)]
        print(f'Move: x:{pick.from_x}->{pick.to_x}, y:{pick.from_y}->{pick.to_y}')
        return pick


class MaximumPointMove(BaseStrategy):
    def play(self, instance: 'GameInstance', board: Board, color: str) -> Move:
        moves = board.get_moves(color)
        if len(moves) == 0:
            raise SystemError()
        shuffle(moves)
        best_move = moves[0]

        for m in moves:
            if m.points > best_move.points:
                best_move = m

        return best_move


class MaximumWeight(BaseStrategy):
    def play(self, instance: 'GameInstance', board: Board, color: str) -> Move:
        moves = board.get_moves(color)
        if len(moves) == 0:
            raise SystemError()
        shuffle(moves)
        m = moves.pop()
        best_move = {
            'move': m,
            'weight': self.weight_move(board, color, m),
        }

        for m in moves:
            w = self.weight_move(board, color, m)
            if w > best_move['weight']:
                best_move = {
                    'move': m,
                    'weight': w,
                }

        return best_move['move']

    def weight_move(self, board: Board, color: str, move: Move) -> int:
        w = move.points
        if isinstance(move.piece, pieces.Pawn):
            w += CENTRAL_POSITION_BONUS / (1 + abs(randint(6, 9) - move.from_x))
            if color == 'white' and isinstance(board.current[WHITE_PROMOTE][move.to_x], pieces.Blank):
                w += PROMOTE_BONUS / (1 + abs(WHITE_PROMOTE - move.to_y))
            elif isinstance(board.current[BLACK_PROMOTE][move.to_x], pieces.Blank):
                w += PROMOTE_BONUS / (1 + abs(BLACK_PROMOTE - move.to_y))
        if not isinstance(square := board.current[move.to_y][move.to_x], pieces.Blank):
            w += square.points * 10
        return w


class OnlyPawnsAndQueensByWeight(MaximumWeight):
    def weight_move(self, board: Board, color: str, move: Move) -> int:
        if type(move.piece) not in [pieces.Pawn, pieces.Queen]:
            return -1
        else:
            return super(OnlyPawnsAndQueensByWeight, self).weight_move(board, color, move)
