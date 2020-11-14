import asyncio
import json
import sys
import websockets
import argparse

from config.default import config
import instance.config


async def main():
    while True:
        async with websockets.connect(config.get('uri'.format(config.get('auth_token')))) as websocket:
            await game_loop(websocket)


async def game_loop(websocket):
    pass


if __name__ == '__main__':
    # Parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('token', help='Override token in configuration', type=str)
    cmd_args = parser.parse_args()

    # Load and merge configuration files
    config.update(instance.config.config)

    # Override stored configuration with parameters
    if cmd_args.token:
        print("Using token from command line")
        config['auth_token'] = cmd_args.token

    # Call event loop
    asyncio.run(main())
