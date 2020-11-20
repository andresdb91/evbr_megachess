from random import randint
from random import shuffle
from game import pieces
from copy import deepcopy

from game.board import Board, WHITE_PROMOTE, BLACK_PROMOTE
from game.move import Move

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
        w = move.get_piece().points
        square = board.get_piece(move.to_x, move.to_y)
        if move.get_piece() == pieces.Pawn:
            w += CENTRAL_POSITION_BONUS / (1 + abs(randint(6, 9) - move.from_x))
            if color == 'white' and board.current[WHITE_PROMOTE][move.to_x] == pieces.Blank:
                w += PROMOTE_BONUS / (1 + abs(WHITE_PROMOTE - move.to_y))
            elif board.current[BLACK_PROMOTE][move.to_x] == pieces.Blank:
                w += PROMOTE_BONUS / (1 + abs(BLACK_PROMOTE - move.to_y))
        if square != pieces.Blank:
            w += square.points * 10
        return w


class OnlyPawnsAndQueensByWeight(MaximumWeight):
    def weight_move(self, board: Board, color: str, move: Move) -> int:
        if type(move.get_piece()) not in [pieces.Pawn, pieces.Queen]:
            return -1
        else:
            return super(OnlyPawnsAndQueensByWeight, self).weight_move(board, color, move)


class TwoMoveWeighting(MaximumWeight):
    def play(self, instance: 'GameInstance', board: Board, color: str) -> Move:
        move_limit = 64
        opponent_color = 'white' if color != 'white' else 'black'

        # Weight own moves
        moves = board.get_moves(color)
        if len(moves) == 0:
            raise SystemError()
        shuffle(moves)
        best_move = {
            'move': Move(),
            'weight': -1000,
        }

        ranked_moves = []
        for m in moves:
            # Weight move
            w = self.weight_move(board, color, m)

            # Calculate movement influence area
            move_influence = [(m.from_x, m.from_y), (m.to_x, m.to_y)]

            ranked_moves.append((m, w, move_influence))

        ranked_moves.sort(key=lambda x: x[1], reverse=True)

        for move, weight, influence in ranked_moves[:move_limit]:
            # Apply on temporal board
            temp_board = deepcopy(board)
            move.execute(temp_board)

            # Get opponent moves
            opponent_moves = temp_board.get_moves(opponent_color)

            # Pick best weighted response
            best_opponent_move = {
                'move': Move(),
                'weight': -1000,
            }
            for om in opponent_moves:
                if (om.to_x, om.to_y) not in influence:
                    continue
                ow = self.weight_move(temp_board, opponent_color, om)
                if ow > best_opponent_move['weight']:
                    best_opponent_move = {
                        'move': om,
                        'weight': ow,
                    }

            total_weight = weight - best_opponent_move['weight']
            if total_weight > best_move['weight']:
                best_move = {
                    'move': move,
                    'weight': total_weight,
                }

        return best_move['move']
