import json
import websockets
from config_manager import ConfigManager
import logging
logger = logging.getLogger(__name__)


class BaseServerAdapter:
    exception: Exception

    def exec_with_context(self, callback: callable):
        pass

    async def recv(self) -> dict:
        pass

    async def send(self, action: str, data: dict):
        pass


class ServerWebsocketAdap(BaseServerAdapter):

    websocket: websockets.WebSocketClientProtocol
    exception = websockets.WebSocketException

    def __init__(self, uri: str):
        self.uri = uri

    # TODO: Implement own context manager
    async def exec_with_context(self, callback: callable):
        while True:
            try:
                async with websockets.connect(self.uri) as self.websocket:
                    logger.info('Connected to websocket server')
                    await callback()
            except Exception as e:
                print(f'Error: {e}')
                logger.error(f'Error: {e}')
                print('Reconnecting...')
                logger.info('Reconnecting...')
                if ConfigManager.get('debug'):
                    raise

    async def recv(self) -> dict:
        response = await self.websocket.recv()
        logger.debug(f'Recv: {response}')
        return json.loads(response)

    async def send(self, action: str, data: dict):
        msg = json.dumps({
            'action': action,
            'data': data,
        })
        logger.debug(f'Sent: {msg}')
        await self.websocket.send(msg)