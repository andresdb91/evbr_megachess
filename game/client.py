import asyncio
import queue

# Temporary fix for missing board_id in gameover event
from datetime import datetime, timedelta

from game.instance import GameInstance
from server_websocket import ServerWebsocketAdap


class GameClient:

    config: {}
    game_list: {}
    game_results: {}
    user_list: [str]
    server: ServerWebsocketAdap
    cli_commands: queue.Queue
    execute: bool

    def __init__(self, config):
        self.config = config.copy()
        self.game_results = {
            'victories': {
                'count': 0,
                'points': [],
            },
            'defeats': {
                'count': 0,
                'points': [],
            },
            'ties': {
                'count': 0,
                'points': [],
            }
        }
        self.user_list = []
        self.game_list = {}
        self.cli_commands = queue.Queue()
        self.execute = True

    async def main(self):
        print(f'Connecting to websocket server: {self.config.get("websocket_uri").format("xxxxx")}')
        self.server = ServerWebsocketAdap(self.config.get('websocket_uri').format(self.config.get('auth_token')))
        await self.server.exec_with_context(self.run, self.execute)

    async def cli_listener(self):
        while self.execute:
            try:
                msg = self.cli_commands.get_nowait()
                command = msg.split(' ')
                if command[0] == 'users':
                    await self.server.send('get_connected_users', {})
                elif len(command) >= 2 and command[0] == 'challenge':
                    if type(command[1]) == str:
                        if len(command) > 2 and type(command[2]) == str:
                            await self.server.send(
                                'challenge',
                                {
                                    'username': command[1],
                                    'message': command[2],
                                }
                            )
                        else:
                            await self.server.send(
                                'challenge',
                                {'username': command[1]}
                            )
                elif len(command) == 2 and command[0] == 'auto-accept':
                    if command[1] == 'on':
                        self.config['accept_challenges'] = True
                    elif command[1] == 'off':
                        self.config['accept_challenges'] = False
                elif command[0] == 'quit':
                    self.execute = False
            except queue.Empty:
                await asyncio.sleep(0.5)

    # Temp fix for missing board_in in gameover event
    async def clean_game_list(self):
        while self.execute:
            current = datetime.now()
            old_games = []
            for board_id, game in self.game_list.items():
                if current - game.last_move > timedelta(seconds=20):
                    old_games.append(board_id)
            if len(old_games) > 0:
                [self.game_list.pop(bid) for bid in old_games]
                print(f'Game instances removed: {old_games}')
            await asyncio.sleep(30)

    async def run(self):
        asyncio.create_task(self.cli_listener())
        # Temp fix for missing board_in in gameover event
        asyncio.create_task(self.clean_game_list())
        while self.execute:
            try:
                response = await self.server.recv()
                if response['event'] == 'update_user_list':
                    if self.user_list != response['data']['users_list']:
                        self.user_list = response['data']['users_list'].copy()
                # elif response['event'] == 'gameover':
                #     if game_instance := self.game_list.get(response['data']['board_id']):
                #         white_score = int(response['data']['white_score'])
                #         black_score = int(response['data']['black_score'])
                #         print(f'Game results:')
                #         if white_score > black_score:
                #             if game_instance.color == 'white':
                #                 print(f'Victory: {white_score} to {black_score} points')
                #                 self.game_results['victories']['count'] += 1
                #                 self.game_results['victories']['points'].append((white_score, black_score))
                #             else:
                #                 print(f'Defeat: {black_score} to {white_score} points')
                #                 self.game_results['defeats']['count'] += 1
                #                 self.game_results['defeats']['points'].append((white_score, black_score))
                #         elif black_score > white_score:
                #             if game_instance.color == 'black':
                #                 print(f'Victory: {black_score} to {white_score} points')
                #                 self.game_results['victories']['count'] += 1
                #                 self.game_results['victories']['points'].append((black_score, white_score))
                #             else:
                #                 print(f'Defeat: {white_score} to {black_score} points')
                #                 self.game_results['defeats']['count'] += 1
                #                 self.game_results['defeats']['points'].append((black_score, white_score))
                #         else:
                #             print(f'Tie: {white_score} points')
                #             self.game_results['ties']['count'] += 1
                #             self.game_results['ties']['points'].append(white_score)
                elif response['event'] == 'ask_challenge':
                    print(f'Challenger: {response["data"]["username"]}')
                    if (self.config.get('accept_challenges')
                            or response['data']['username'] == self.config['username'])\
                            and len(self.game_list) < self.config.get('max_games', 1):
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
                        await game_instance.play(
                            turn_token=response['data']['turn_token'],
                            server=self.server,
                            board=response['data']['board'],
                        )
                        game_instance.last_move = datetime.now()
                    else:
                        new_instance = GameInstance(
                            config=self.config,
                            board_id=response['data']['board_id'],
                            opponent=response['data']['opponent_username'],
                            move_left=response['data']['move_left'],
                            color=response['data']['actual_turn'],
                            board=response['data']['board'],
                        )
                        self.game_list[response['data']['board_id']] = new_instance
                        await new_instance.play(
                            turn_token=response['data']['turn_token'],
                            server=self.server,
                        )
                        print(f'New game - id: {new_instance.board_id} - color: {new_instance.color}')
                        new_instance.last_move = datetime.now()
            except Exception as e:
                print(f'Error: {e}')
                print('Attempting reconnection...')
                return
