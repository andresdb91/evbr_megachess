from server import server_adap


class ServerAdapterFactory:
    default_adapter: str = 'websocket'

    @staticmethod
    def get_adapter(name: str, *args) -> server_adap.BaseServerAdapter:
        adapters = {
            'websocket': server_adap.ServerWebsocketAdap,
        }

        if name not in adapters.keys():
            name = ServerAdapterFactory.default_adapter
        print(f'Using server adapter: {name}')

        return adapters[name](*args)
