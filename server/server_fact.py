from server import server_adap


class ServerAdapterFactory:
    default_adapter: str = 'websocket'

    adapters = {
        'websocket': server_adap.ServerWebsocketAdap,
    }

    @staticmethod
    def get_adapter(name: str, *args) -> server_adap.BaseServerAdapter:
        if name not in ServerAdapterFactory.adapters.keys():
            name = ServerAdapterFactory.default_adapter
        print(f'Using server adapter: {name}')

        return ServerAdapterFactory.adapters[name](*args)
