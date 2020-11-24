import aiosqlite
from game.instance import GameInstance
from game.move import Move
from datetime import date
from config_manager import ConfigManager

MATCH_TABLE = 'match'
MOVE_TABLE = 'move'


class SavedData:
    conn: aiosqlite.Connection
    next_match_id: int

    match_check_query = f"SELECT * FROM {MATCH_TABLE} WHERE board_id=?"
    match_insert_query = f"INSERT INTO {MATCH_TABLE} VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"
    move_insert_query = f"INSERT INTO {MOVE_TABLE} VALUES (?, ?, ?, ?, ?, ?, ?, ?)"

    async def init_db(self):
        self.conn = await aiosqlite.connect(f'db/megachess-{date.today().isoformat()}.db', isolation_level=None)
        print(f'Opened database: db/megachess-{date.today().isoformat()}.db')
        try:
            await self.conn.execute(
                f'CREATE TABLE {MATCH_TABLE} ('
                'id int, '
                'board_id text, '
                'start text, '
                'end text, '
                'white_username text, '
                'black_username text, '
                'white_score int, '
                'black_score int, '
                'winner text'
                ')'
            )
        except aiosqlite.OperationalError:
            pass
        finally:
            cursor = await self.conn.execute(f'select * from {MATCH_TABLE}')
            count = len(await cursor.fetchall())
            self.next_match_id = count

        try:
            await self.conn.execute(
                f'CREATE TABLE {MOVE_TABLE} ('
                'move_number int, '
                'move_color text, '
                'is_valid boolean, '
                'from_x int, '
                'from_y int, '
                'to_x int, '
                'to_y int, '
                'match_fk int'
                ')'
            )
        except aiosqlite.OperationalError:
            pass

    async def store_match(self, match: GameInstance, score_white: int, score_black: int):
        if match.color == 'white':
            white_username = ConfigManager.get('username') or ''
            black_username = match.opponent
        else:
            black_username = ConfigManager.get('username') or ''
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

        cursor = await self.conn.execute(self.match_check_query, (match.board_id,))
        if await cursor.fetchone():
            print(f'Duplicate match: {match.board_id}')
            return

        cursor = await self.conn.execute(self.match_insert_query, match_params)
        print(f'Saved match: {match.board_id} as {match_id}')
        self.next_match_id = cursor.lastrowid

        if match.save_history:
            await self.store_moves(match_id, match.move_history)
        else:
            print(f'Moves not available for match {match_id}')

    async def store_moves(self, match_id: int, moves: list[Move]):
        move_params = [
            (
                i,
                moves[i].color,
                moves[i].is_valid(),
                moves[i].from_x,
                moves[i].from_y,
                moves[i].to_x,
                moves[i].to_y,
                match_id,
            )
            for i in range(0, len(moves))
        ]
        await self.conn.executemany(self.move_insert_query, move_params)
        print(f'Saved {len(move_params)} moves to match [{match_id}]')

    async def store_match_no_instance(self):
        pass
