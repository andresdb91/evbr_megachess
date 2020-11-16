import websockets
import json


class ServerWebsocketAdap:

    websocket: websockets.WebSocketClientProtocol

    def __init__(self, uri):
        self.uri = uri

    # TODO: Implement own context manager
    async def exec_with_context(self, callback, condition):
        while condition:
            try:
                async with websockets.connect(self.uri) as self.websocket:
                    print('Connected to websocket server')
                    await callback()
            except Exception as e:
                print(f'Error: {e}')
                raise

    async def recv(self):
        response = await self.websocket.recv()
        print(f'Recv: {response}')
        return json.loads(response)

    async def send(self, action, data):
        msg = json.dumps({
            'action': action,
            'data': data,
        })
        print(f'Sent: {msg}')
        await self.websocket.send(msg)
