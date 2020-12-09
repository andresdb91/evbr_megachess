import asyncio
import queue
from random import randint

from datetime import datetime

from config_manager import ConfigManager
from game.instance import GameInstance
from server.server_adap import BaseServerAdapter
from server.server_fact import ServerAdapterFactory
from game.strategy import AIStrategy
from db_adap import SavedData

OLD_GAMES_CHECK_TIME = 20
GAME_TIMEOUT = 15


class GameClient:

    game_list: dict[GameInstance]
    game_results: dict
    user_list: [str]
    server: BaseServerAdapter
    saved_data: SavedData
    cli_commands: queue.Queue

    def __init__(self):
        self.user_list = []
        self.game_list = {}
        self.cli_commands = queue.Queue()
        self.saved_data = SavedData()

    async def main(self):
        print(f'Connecting to websocket server: {ConfigManager.get("websocket_uri").format("xxxxx")}')
        self.server = ServerAdapterFactory.get_adapter(
            ConfigManager.get('server_adapter'),
            ConfigManager.get('websocket_uri').format(ConfigManager.get('auth_token'))
        )
        await self.saved_data.init_db()
        await self.server.exec_with_context(self.run)

    async def cli_listener(self):
        while True:
            try:
                msg = self.cli_commands.get_nowait()
                command = msg.split(' ')
                if command[0] == 'users':
                    await self.server.send('get_connected_users', {})
                elif len(command) >= 2 and command[0] == 'challenge':
                    if len(command) > 2:
                        await self.server.send(
                            'challenge',
                            {
                                'username': command[1],
                                'message': command[2:],
                            }
                        )
                    else:
                        await self.server.send(
                            'challenge',
                            {'username': command[1]}
                        )
                elif command[0] == 'randomchallenge':
                    await self.server.send(
                        'challenge',
                        {
                            'username': self.user_list[randint(0, len(self.user_list)-1)],
                        }
                    )
                elif len(command) == 2 and command[0] == 'auto-accept':
                    if command[1] == 'on':
                        ConfigManager.set('accept_challenges', True)
                    elif command[1] == 'off':
                        ConfigManager.set('accept_challenges', False)
                elif command[0] == 'quit':
                    asyncio.get_event_loop().stop()
                elif command[0] == 'abort' and len(command) == 2:
                    await self.server.send('abort', {'board_id': command[1]})
                elif command[0] == 'config' and len(command) == 3:
                    value = command[2]
                    if value.isdigit():
                        value = int(value)
                    elif value.lower() in ['true', 'on']:
                        value = True
                    elif value.lower() in ['false', 'off']:
                        value = False
                    ConfigManager.set(command[1], value)
            except queue.Empty:
                await asyncio.sleep(0.5)

    async def run(self):
        if ConfigManager.get('interface'):
            asyncio.create_task(self.cli_listener())
        while True:
            try:
                response = await self.server.recv()
                if response['event'] == 'update_user_list':
                    if self.user_list != response['data']['users_list']:
                        self.user_list = response['data']['users_list']
                    print(f'Online users: {self.user_list}')
                elif response['event'] == 'gameover':
                    game_instance = self.game_list.pop(response['data']['board_id'], None)
                    white_score = int(response['data']['white_score'])
                    black_score = int(response['data']['black_score'])
                    if game_instance:
                        color = game_instance.color
                        opponent = game_instance.opponent
                        game_instance.end = datetime.now()
                        asyncio.create_task(self.saved_data.store_match(game_instance, white_score, black_score))
                    else:
                        if response['data']['white_username'] == ConfigManager.get('username') or '':
                            color = 'white'
                            opponent = response['data']['black_username']
                        else:
                            color = 'black'
                            opponent = response['data']['white_username']
                    print(f'Game results for board: {response["data"]["board_id"]}')
                    print(f'Opponent: {opponent}')
                    if response['data']['white_username'] == response['data']['black_username']:
                        print(f'Self-challenge: w -> {white_score} | b -> {black_score}')
                    else:
                        if white_score > black_score:
                            if color == 'white':
                                print(f'Victory as white: {white_score} to {black_score} points')
                            else:
                                print(f'Defeat as black: {black_score} to {white_score} points')
                        elif black_score > white_score:
                            if color == 'black':
                                print(f'Victory as black: {black_score} to {white_score} points')
                            else:
                                print(f'Defeat as white: {white_score} to {black_score} points')
                        else:
                            print(f'Tie: {white_score} points')
                elif response['event'] == 'ask_challenge':
                    if selfchallenge := response['data']['username'] == ConfigManager.get('username'):
                        print('Self-challenge requested')
                    else:
                        print(f'Challenger: {response["data"]["username"]}')
                    if (ConfigManager.get('accept_challenges')
                            or selfchallenge)\
                            and len(self.game_list) < (ConfigManager.get('max_games') or 1):
                        game_count = 0
                        for game in self.game_list.values():
                            if game.opponent == response["data"]["username"]:
                                game_count += 1
                        if not selfchallenge or game_count <= (ConfigManager.get('max_games_per_user') or 1):
                            await self.server.send(
                                action='accept_challenge',
                                data={'board_id': response['data']['board_id']}
                            )
                        print(f'Challenge accepted:\n'
                              f'Challenger: {response["data"]["username"]}\n'
                              f'Board ID: {response["data"]["board_id"]}')
                    else:
                        print(f'Challenge rejected:\n'
                              f'Challenger: {response["data"]["username"]}\n'
                              f'Board ID: {response["data"]["board_id"]}')
                elif response['event'] == 'your_turn':
                    if game_instance := self.game_list.get(response['data']['board_id']):
                        asyncio.create_task(game_instance.play(
                            turn_token=response['data']['turn_token'],
                            server=self.server,
                            board=response['data']['board'],
                            color=response['data']['actual_turn'],
                            moves_left=response['data']['move_left'],
                        ))
                    else:
                        new_instance = GameInstance(
                            board_id=response['data']['board_id'],
                            opponent=response['data']['opponent_username'],
                            color=response['data']['actual_turn'],
                            board=response['data']['board'],
                            strategy=AIStrategy(),
                        )
                        self.game_list[response['data']['board_id']] = new_instance
                        asyncio.create_task(new_instance.play(
                            turn_token=response['data']['turn_token'],
                            server=self.server,
                            color=response['data']['actual_turn'],
                            moves_left=response['data']['move_left'],
                        ))
                        print(f'New game - id: {new_instance.board_id} '
                              f'- color: {new_instance.color} '
                              f'- opponent: {new_instance.opponent}')
            except self.server.exception:
                raise
            except Exception as e:
                print(f'Error: {e}')
                if ConfigManager.get('debug'):
                    raise
