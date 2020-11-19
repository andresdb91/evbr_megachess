class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class ConfigManager(metaclass=Singleton):
    _instance: 'ConfigManager' = None
    config: dict

    def __init__(self, config):
        if ConfigManager._instance is None:
            ConfigManager._instance = self
            self.config = config.copy()

    def _get(self, attr):
        return self.config.get(attr)

    @classmethod
    def get(cls, attr):
        return cls._instance._get(attr)

    def _set(self, attr, val):
        self.config[attr] = val

    @classmethod
    def set(cls, attr, val):
        cls._instance._set(attr, val)
