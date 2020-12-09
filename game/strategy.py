from game.board import Board
from game.move import Move
from copy import deepcopy
from random import randint


class AIStrategy:
    starting_depth: int = 2

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
        print(f'Time to play: {post.seconds*1000+post.microseconds/1000} ms - Moves left: {moves_left}')
        print(move.to_coords(), score)
        if (ply_time := post.seconds*1000+post.microseconds/1000) > self.slowest_move:
            self.slowest_move = ply_time
        if moves_left <= 2:
            print(f'Slowest move: {self.slowest_move}')

        return move

    def heuristic(self, board: Board, move: Move, color: str) -> int:
        # 170
        # 165
        # 95 | 160
        # 60
        white_promote = 8
        black_promote = 7
        central_bonus = 4
        queen_defense = 25

        score = move.points
        if move.piece.is_piece('p'):
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

        target = board.get_piece(move.to_x, move.to_y)
        if not (move.piece.is_piece('p') or move.piece.is_piece('k')) and target.is_piece(' '):
            return -1

        if target.is_piece('p'):
            if color == 'white':
                score += (5 - abs(black_promote - move.to_y)) * 122
            elif color == 'black':
                score += (5 - abs(white_promote - move.to_y)) * 122
        elif target.is_piece('q'):
            if color == 'white':
                score += queen_defense * move.to_y
            elif color == 'black':
                score += 15*queen_defense - queen_defense * move.to_y

        randomized_center = randint(6, 9)
        score += central_bonus * (randomized_center / (1 + abs(randomized_center - move.to_x)))

        return score

    def invert_color(self, color) -> str:
        return 'white' if color != 'white' else 'black'

    def pick(self, board: Board, color: str, maximize: bool, depth: int,
             moves_left: int, acc: int, alfa: int = None, beta: int = None):
        moves = board.get_moves(color)
        sorted(moves, key=lambda x: x.points)
        candidate = None
        max_score = float('-inf')
        min_score = float('+inf')
        if not alfa:
            alfa = float('-inf')
        if not beta:
            beta = float('+inf')
        for move in moves:
            move_heuristic = self.heuristic(board, move, color)
            if move_heuristic < 0:
                continue
            if depth == 0 or moves_left == 1:
                if maximize:
                    score = acc + move_heuristic
                    if score > max_score:
                        max_score = score
                        candidate = move
                else:
                    score = acc - move_heuristic
                    if score < min_score:
                        min_score = score
                        candidate = move
            else:
                move.execute(board)
                if maximize:
                    score, subcandidate = self.pick(
                        board,
                        self.invert_color(color),
                        False,
                        depth - 1,
                        moves_left - 1,
                        acc + move_heuristic,
                        alfa,
                        beta,
                    )
                    move.undo(board)
                    if score > max_score:
                        max_score = score
                        candidate = move
                    alfa = max(alfa, score)
                    if alfa >= beta:
                        break
                else:
                    score, subcandidate = self.pick(
                        board,
                        self.invert_color(color),
                        True,
                        depth - 1,
                        moves_left - 1,
                        acc - move_heuristic,
                        alfa,
                        beta,
                    )
                    move.undo(board)
                    if score < min_score:
                        min_score = score
                        candidate = move
                    beta = min(beta, score)
                    if beta <= alfa:
                        break

        if candidate is None and len(moves) > 0:
            return -1, moves[randint(0, len(moves)-1)] if len(moves) > 1 else moves[0]

        if maximize:
            return max_score, candidate
        else:
            return min_score, candidate
