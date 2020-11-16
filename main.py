import asyncio
import argparse
import threading

from config.default import config
import instance.config

from game.client import GameClient
from ui import UI


if __name__ == '__main__':
    # Parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--token', help='Override token in configuration', type=str)

    cli = parser.add_mutually_exclusive_group()
    cli.add_argument('-i', '--interface', action='store_true', help='Enable command line interface')
    cli.add_argument('-n', '--no-interface', action='store_true', help='Disable command line interface')

    cmd_args = parser.parse_args()

    # Load and merge configuration files
    config.update(instance.config.config)

    # Override stored configuration with parameters
    if cmd_args.token:
        print('Using token from command line')
        config['auth_token'] = cmd_args.token
    if cmd_args.interface:
        print('Command line interface enabled')
        config['interface'] = True

    # Create game instance
    game = GameClient(config)

    # Start cli interface
    if config.get('interface'):
        ui = UI(game)
        print('Starting UI thread')
        T = threading.Thread(target=ui.cli, daemon=True)
        T.start()

    # Call event loop
    print('Starting game loop')
    asyncio.run(game.main())
