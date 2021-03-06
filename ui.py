import asyncio
from game.client import GameClient


class UI:

    game: GameClient
    valid_commands = [
        'users',
        'challenge',
        'randomchallenge',
        'auto-accept',
        'config',
        'quit',
        'abort',
    ]

    def __init__(self, game: GameClient):
        self.game = game

    def cli(self):
        while True:
            command = input('MegaChess CLI: ')
            if command == 'help':
                print('users: Updates and shows current online users')
                print('challenge [<user>]: Sends a challenge to a specific user')
                print('randomchallenge: Sends a challenge to a random online user')
                print('abort <board_id>: Aborts selected game')
                print('auto-accept [on | off]: Enables or disables challenge autoaccept')
                print('self <key> <value>: Changes a configuration value')
                print('quit: Disconnects the websocket and exits the program')
            elif command.split(' ')[0] in self.valid_commands:
                self.game.cli_commands.put(command)
                if command.split(' ')[0] == 'quit':
                    return
            else:
                print('Invalid command, to view all commands type "help"')
