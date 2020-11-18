import sqlite3
from game.instance import GameInstance
from game.move import Move

MATCH_TABLE = 'match'
MOVE_TABLE = 'move'


class SavedData:
    connection: sqlite3.Connection
    next_match_id: int

    match_insert_query = f"INSERT INTO {MATCH_TABLE} VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"
    move_insert_query = f"INSERT INTO {MOVE_TABLE} VALUES (?, ?, ?, ?, ?, ?, ?, ?)"

    def __init__(self):
        self.connection = sqlite3.connect('megachess.db')
        self.init_db()

    def init_db(self):
        c = self.connection.cursor()
        try:
            c.execute(f'select * from {MATCH_TABLE}')
        except sqlite3.OperationalError:
            c.execute(f'CREATE TABLE {MATCH_TABLE} ('
                      'id int, '
                      'board_id text, '
                      'start text, '
                      'end text, '
                      'white_username text, '
                      'black_username text, '
                      'white_score int, '
                      'black_score int, '
                      'winner text'
                      ')')
        finally:
            self.next_match_id = c.lastrowid

        try:
            c.execute(f'select * from {MOVE_TABLE}')
        except sqlite3.OperationalError:
            c.execute(f'CREATE TABLE {MOVE_TABLE} ('
                      'move_number int, '
                      'move_color text, '
                      'is_valid boolean, '
                      'from_x int, '
                      'from_y int, '
                      'to_x int, '
                      'to_y int, '
                      'match_fk int'
                      ')')

    def store_match(self, match: GameInstance, score_white: int, score_black: int):
        if match.color == 'white':
            white_username = match.config.get('username', '')
            black_username = match.opponent
        else:
            black_username = match.config.get('username', '')
            white_username = match.opponent

        if white_username == black_username:
            winner = 'self-challenge'
        elif score_white > score_black:
            winner = 'white'
        elif score_black > score_white:
            winner = 'black'
        else:
            winner = 'tie'

        match_params = (
            self.next_match_id,
            match.board_id,
            match.start,
            match.end,
            white_username,
            black_username,
            score_white,
            score_black,
            winner,
        )
        match_id = self.next_match_id

        c = self.connection.cursor()
        c.execute(self.match_insert_query, match_params)
        self.next_match_id = c.lastrowid

        if match.save_history:
            self.store_moves(match_id, match.move_history)

    def store_moves(self, match_id: int, moves: list[Move]):
        move_params = [
            (
                i,
                moves[i].piece.color,
                moves[i].points > 0,
                moves[i].from_x,
                moves[i].from_y,
                moves[i].to_x,
                moves[i].to_y,
                match_id,
            )
            for i in range(0, len(moves))
        ]
        c = self.connection.cursor()
        c.executemany(self.move_insert_query, move_params)

    def store_match_no_instance(self):
        pass
