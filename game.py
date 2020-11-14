import asyncio
import json
import sys
import websockets


class Game:

    config: {}

    def __init__(self, config):
        self.config = config.copy()

    async def main(self):
        while True:
            async with websockets.connect(self.config.get('uri'.format(self.config.get('auth_token')))) as websocket:
                await self.run(websocket)

    async def run(self, websocket):
        pass

    def play(self):
        pass
