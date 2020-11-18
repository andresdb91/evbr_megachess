import websockets
import json
import asyncio


class ServerWebsocketAdap:

    websocket: websockets.WebSocketClientProtocol

    def __init__(self, uri: str):
        self.uri = uri

    # TODO: Implement own context manager
    async def exec_with_context(self, callback: callable):
        while True:
            try:
                async with websockets.connect(self.uri) as self.websocket:
                    print('Connected to websocket server')
                    await callback()
            except Exception as e:
                print(f'Error: {e}')
                await asyncio.sleep(3)
                # raise

    async def recv(self) -> dict:
        response = await self.websocket.recv()
        print(f'Recv: {response}')
        return json.loads(response)

    async def send(self, action: str, data: dict):
        msg = json.dumps({
            'action': action,
            'data': data,
        })
        print(f'Sent: {msg}')
        await self.websocket.send(msg)
