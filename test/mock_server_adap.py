from server.server_adap import BaseServerAdapter


class MockServerAdapter(BaseServerAdapter):
    test_recv: dict
    test_send: (str, dict)

    async def recv(self) -> dict:
        return self.test_recv

    async def send(self, action: str, data: dict):
        self.test_send = (action, data)
