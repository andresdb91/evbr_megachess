import asyncio
from game.client import GameClient


class UI:

    game: GameClient
    valid_commands = [
        'users',
        'challenge',
        'auto-accept',
        'quit',
        'config',
    ]

    def __init__(self, game: GameClient):
        self.game = game

    def cli(self):
        while True:
            command = input('MegaChess CLI: ')
            if command == 'help':
                print('users: updates and shows current online users')
                print('challenge [<user>]: sends a challenge to a specific or random user')
                print('auto-accept [on | off]: Enables or disables challenge autoaccept')
                print('config <key> <value>: Changes a configuration value')
                print('quit: Disconnects the websocket and exits the program')
            elif command.split(' ')[0] in self.valid_commands:
                self.game.cli_commands.put(command)
            else:
                print('Invalid command, to view all commands type "help"')
