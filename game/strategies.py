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
    @staticmethod
    def play(instance: 'GameInstance', board: Board, color: str) -> Move:
        pass


class RandomLegal(BaseStrategy):
    @staticmethod
    def play(instance: 'GameInstance', board: Board, color: str) -> Move:
        moves = board.get_moves(color)

        pick = moves[randint(0, len(moves)-1)]
        print(f'Move: x:{pick.from_x}->{pick.to_x}, y:{pick.from_y}->{pick.to_y}')
        return pick


class MaximumPointMove(BaseStrategy):
    @staticmethod
    def play(instance: 'GameInstance', board: Board, color: str) -> Move:
        moves = board.get_moves(color)
        if len(moves) == 0:
            raise SystemError()
        shuffle(moves)
        best_move = moves[0]

        for m in moves:
            if m.points > best_move.weight:
                best_move = m

        return best_move


class MaximumWeight(BaseStrategy):
    @staticmethod
    def play(instance: 'GameInstance', board: Board, color: str) -> Move:
        moves = board.get_moves(color)
        if len(moves) == 0:
            raise SystemError()
        shuffle(moves)
        best_move = {
            'move': moves[0],
            'weight': 0,
        }

        for m in moves:
            w = m.points
            if isinstance(m.piece, pieces.Pawn):
                w += CENTRAL_POSITION_BONUS / (1 + abs(8 - m.from_x))
                if color == 'white':
                    w += PROMOTE_BONUS / (1 + abs(WHITE_PROMOTE - m.to_y))
                else:
                    w += PROMOTE_BONUS / (1 + abs(BLACK_PROMOTE - m.to_y))
            if not isinstance(square := board.current[m.to_y][m.to_x], pieces.Blank):
                w += square.points * 10
            if w > best_move['weight']:
                best_move = {
                    'move': m,
                    'weight': w,
                }

        return best_move['move']


class OnlyPawnsAndQueensByWeight(BaseStrategy):
    @staticmethod
    def play(instance: 'GameInstance', board: Board, color: str) -> Move:
        moves = board.get_moves(color)
        if len(moves) == 0:
            raise SystemError()
        shuffle(moves)
        best_move = {
            'move': moves[0],
            'weight': 0,
        }

        for m in moves:
            if type(m.piece) not in [pieces.Pawn, pieces.Queen]:
                continue
            w = m.points
            if isinstance(m.piece, pieces.Pawn):
                w += CENTRAL_POSITION_BONUS / (1 + abs(8 - m.from_x))
                if color == 'white':
                    w += PROMOTE_BONUS / (1 + abs(WHITE_PROMOTE - m.to_y))
                else:
                    w += PROMOTE_BONUS / (1 + abs(BLACK_PROMOTE - m.to_y))
            if not isinstance(square := board.current[m.to_y][m.to_x], pieces.Blank):
                w += square.points * 10
            if w > best_move['weight']:
                best_move = {
                    'move': m,
                    'weight': w,
                }

        return best_move['move']
