from random import randint
from random import shuffle
from game import pieces
from copy import deepcopy

from game.board import Board, WHITE_PROMOTE, BLACK_PROMOTE
from game.move import Move

PROMOTE_BONUS = 500
STARTING_POSITION_BONUS = 10
DEFENSE_BONUS = 500
CAPTURE_BONUS = {
    'p': 0,
    'r': 0,
    'h': 0,
    'b': 0,
    'q': 0,
    'k': 0,
}
MOVE_BONUS = {
    'p': 10,
    'r': 0,
    'h': 0,
    'b': 0,
    'q': 0,
    'k': -70,
}
MIN_MOVES_BEFORE_CUTLINE = 64


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
        start_move = moves.pop()
        best_move = (start_move, self.weight_move(board, color, start_move))

        for m in moves:
            if (w := self.weight_move(board, color, m)) > best_move[1]:
                best_move = (m, w)

        return best_move[0]

    def weight_move(self, board: Board, color: str, move: Move) -> int:
        return move.points


class MaximumWeight(BaseStrategy):
    def play(self, instance: 'GameInstance', board: Board, color: str) -> Move:
        moves = board.get_moves(color)
        if len(moves) == 0:
            raise SystemError()
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
        if move.piece == pieces.Pawn and move.to_y not in [WHITE_PROMOTE, BLACK_PROMOTE]:
            if color == 'white' and board.is_empty(move.to_x, WHITE_PROMOTE):
                w += PROMOTE_BONUS / (1 + abs(WHITE_PROMOTE - move.to_y))
            elif color == 'black' and board.is_empty(move.to_x, BLACK_PROMOTE):
                w += PROMOTE_BONUS / (1 + abs(BLACK_PROMOTE - move.to_y))
        return w


class ModifiedWeighting(MaximumWeight):
    def weight_move(self, board: Board, color: str, move: Move) -> int:
        w = move.piece.points / 2 + MOVE_BONUS[move.piece.character]
        square = board.get_piece(move.to_x, move.to_y)
        if move.piece == pieces.Pawn:
            w += STARTING_POSITION_BONUS / (1 + abs(randint(2, 5) - move.from_x))
            if color == 'white' and board.current[WHITE_PROMOTE][move.to_x] == ' ':
                w += PROMOTE_BONUS / (1 + abs(WHITE_PROMOTE - move.to_y))
            elif color == 'black' and board.current[BLACK_PROMOTE][move.to_x] == ' ':
                w += PROMOTE_BONUS / (1 + abs(BLACK_PROMOTE - move.to_y))
        if square != pieces.Blank:
            w += square.points * 10 + CAPTURE_BONUS[square.character]
            if (color == 'white' and move.to_y >= WHITE_PROMOTE) \
                    or (color == 'black' and move.to_y <= BLACK_PROMOTE):
                w += DEFENSE_BONUS
        return w


class OnlyPawnsAndQueensByWeight(MaximumWeight):
    def weight_move(self, board: Board, color: str, move: Move) -> int:
        if move.piece not in [pieces.Pawn, pieces.Queen]:
            return -1
        else:
            return super(OnlyPawnsAndQueensByWeight, self).weight_move(board, color, move)


class TwoMoveWeighting(MaximumWeight):
    def play(self, instance: 'GameInstance', board: Board, color: str) -> Move:
        opponent_color = 'white' if color != 'white' else 'black'

        # Weight own moves
        moves = board.get_moves(color)
        if len(moves) == 0:
            raise SystemError()
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

        for move, weight, influence in ranked_moves:
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


class MultiMoveWeight(MaximumWeight):
    def play(self, instance: 'GameInstance', board: Board, color: str) -> Move:
        opponent_color = 'white' if color != 'white' else 'black'

        # Set max amount of iterations
        max_iter = 2

        # Copy once, then exec/undo
        temp_board = deepcopy(board)

        # Setup initial board with no base weight
        # Move is set to [] to be populated on first iteration
        board_list: list[tuple[int, list[Move]]] = [(0, [])]

        for it in range(0, max_iter):
            # Hold board list for next iteration (breadth first search)
            next_board_list = []
            for board_weight, prev_moves in board_list:
                # Apply previous move chain
                for pm in prev_moves:
                    pm.execute(temp_board)
                moves = temp_board.get_moves(color)
                ranked_moves = []
                for m in moves:
                    # Weight move
                    w = board_weight + self.weight_move(temp_board, color, m)
                    # Calculate movement influence area
                    move_influence = [(m.from_x, m.from_y), (m.to_x, m.to_y)]
                    ranked_moves.append((m, w, move_influence))

                # Sort all moves by weight, best first
                ranked_moves.sort(key=lambda x: x[1], reverse=True)
                # Set a cutline to discard moves
                if len(moves) > MIN_MOVES_BEFORE_CUTLINE:
                    cut_line = ranked_moves[0][1] - (ranked_moves[0][1] - ranked_moves[-1][1]) / 2
                else:
                    cut_line = -1000

                for move, weight, influence in ranked_moves:
                    # Discard if under cutline
                    if weight < cut_line:
                        continue
                    # Apply new move on temporal board
                    move.execute(temp_board)
                    # Get opponent moves
                    opponent_moves = temp_board.get_moves(opponent_color)
                    # Pick best weighted response
                    best_opponent_move = {
                        'move': None,
                        'weight': -1000,
                    }
                    for om in opponent_moves:
                        # if (om.to_x, om.to_y) not in influence:
                        #     continue
                        ow = self.weight_move(temp_board, opponent_color, om)
                        if ow > best_opponent_move['weight']:
                            best_opponent_move = {
                                'move': om,
                                'weight': ow,
                            }
                    # Calculate new board weight
                    net_weight = weight - best_opponent_move['move'].points

                    # Undo last move to restore temp board
                    move.undo(temp_board)

                    # Add move sequence to next iteration
                    next_board_list.append((
                        net_weight,
                        prev_moves + [move, best_opponent_move['move']]
                    ))
                # Undo move sequence
                for pm in reversed(prev_moves):
                    pm.undo(temp_board)
            board_list = next_board_list

        # Return first move from best chain
        return sorted(board_list, key=lambda x: x[0], reverse=True)[0][1][0]
