from game.board import Board
from game.move import Move
from copy import deepcopy
from random import randint


class AIStrategy:
    starting_depth: int = 2
    randomized_center: int = None
    slowest_move: float = 0

    def play(self, board: Board, color: str, moves_left: int) -> Move:
        from datetime import datetime
        pre = datetime.now()
        try:
            temp_board = deepcopy(board)
            score, move = self.pick(temp_board, color, True, self.starting_depth, moves_left, 0)
        except Exception as e:
            print(e)
            raise
        post = datetime.now() - pre
        # print(f'Time to play: {post.seconds*1000+post.microseconds/1000} ms - Moves left: {moves_left}')
        # print(move.to_coords(), score)
        if (ply_time := post.seconds*1000+post.microseconds/1000) > self.slowest_move:
            self.slowest_move = ply_time
        if moves_left <= 2:
            print(f'Slowest move: {self.slowest_move}')

        return move

    def heuristic(self, board: Board, move: Move, color: str, left: int) -> int:
        white_promote = 8
        black_promote = 7
        central_bonus = 1
        defense_bonus = 25

        score = move.points
        if move.piece.is_piece('p') and left >= 5:
            if color == 'white' and board.get_piece(move.to_x, white_promote).is_piece(' '):
                if move.to_y == white_promote:
                    score -= 330
                elif move.to_y == white_promote + 1:
                    score += 165
                elif move.to_y == white_promote + 2:
                    if move.from_y == white_promote + 3:
                        score += 95
                    elif move.from_y == white_promote + 4:
                        score += 160
                elif move.to_y == white_promote + 3 and move.from_y == white_promote + 5:
                    score += 90
            elif color == 'black' and board.get_piece(move.to_x, black_promote).is_piece(' '):
                if move.to_y == black_promote:
                    score -= 330
                elif move.to_y == black_promote - 1:
                    score += 165
                elif move.to_y == black_promote - 2:
                    if move.from_y == black_promote - 3:
                        score += 95
                    elif move.from_y == black_promote - 4:
                        score += 160
                elif move.to_y == black_promote - 3 and move.from_y == black_promote - 5:
                    score += 60
            elif color == 'black':
                crown_target_left, target_color_left = board.get_piece_color(move.to_x - 1, black_promote)
                crown_target_right, target_color_right = board.get_piece_color(move.to_x + 1, black_promote)
                if (crown_target_left and target_color_left == 'white') \
                        or (crown_target_right and target_color_right == 'white'):
                    score += 10
            elif color == 'white':
                crown_target_left, target_color_left = board.get_piece_color(move.to_x - 1, white_promote)
                crown_target_right, target_color_right = board.get_piece_color(move.to_x + 1, white_promote)
                if (crown_target_left and target_color_left == 'black') \
                        or (crown_target_right and target_color_right == 'black'):
                    score += 10

        target = board.get_piece(move.to_x, move.to_y)
        if target.is_piece(' ') and not move.piece.is_piece('p'):
            return -1

        if target.is_piece('p'):
            if color == 'white':
                if move.to_y > 5:
                    score += (5 - abs(black_promote - move.to_y)) * 122
            elif color == 'black':
                if move.to_y < 10:
                    score += (5 - abs(white_promote - move.to_y)) * 122
        elif not target.is_piece(' '):
            if color == 'white' and move.to_y >= black_promote - 1:
                score += defense_bonus * move.to_y
            elif color == 'black' and move.to_y <= white_promote + 1:
                score += 15*defense_bonus - defense_bonus * move.to_y

        if self.randomized_center is None:
            self.randomized_center = randint(5, 10)
        score += central_bonus * (self.randomized_center / (1 + abs(self.randomized_center - move.to_x)))

        return score

    def invert_color(self, color) -> str:
        return 'white' if color != 'white' else 'black'

    def pick(self, board: Board, color: str, maximize: bool, depth: int,
             moves_left: int, alfa: int = None, beta: int = None):
        moves = board.get_moves(color)

        if len(moves) == 1:
            return moves[0].points, moves[0]
        elif len(moves) == 0:
            return float('inf') if maximize else float('-inf'), Move()

        moves.sort(key=lambda x: x.points, reverse=True)
        candidate = None
        max_score = float('-inf')
        min_score = float('+inf')
        min_points = 0
        max_points = 0

        if not alfa:
            alfa = float('-inf')
        if not beta:
            beta = float('+inf')

        for move in moves:
            move_heuristic = self.heuristic(board, move, color, moves_left)
            if move_heuristic < 0:
                continue
            if depth == 0 or moves_left == 1:
                if maximize:
                    if move_heuristic > max_score:
                        max_score = move_heuristic
                        candidate = move
                        max_points = move.points
                else:
                    if move_heuristic < min_score:
                        min_score = move_heuristic
                        candidate = move
                        min_points = - move.points
            else:
                move.execute(board)
                if maximize:
                    score, _ = self.pick(
                        board,
                        self.invert_color(color),
                        False,
                        depth - 1,
                        moves_left - 1,
                        alfa,
                        beta,
                    )
                    move.undo(board)
                    score += move_heuristic
                    if score > max_score:
                        max_score = score
                        candidate = move
                        max_points = score - move_heuristic + move.points
                    alfa = max(alfa, score)
                    if alfa >= beta:
                        break
                else:
                    score, _ = self.pick(
                        board,
                        self.invert_color(color),
                        True,
                        depth - 1,
                        moves_left - 1,
                        alfa,
                        beta,
                    )
                    move.undo(board)
                    score -= move_heuristic
                    if score < min_score:
                        min_score = score
                        candidate = move
                        min_points = score + move_heuristic - move.points
                    beta = min(beta, score)
                    if beta <= alfa:
                        break

        if candidate is None:
            if maximize:
                return moves[0].points, moves[0]
            else:
                return - moves[0].points, moves[0]

        if maximize:
            return max_points, candidate
        else:
            return min_points, candidate
