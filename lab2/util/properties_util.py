import configparser

APPLICATION_PROPERTIES_PATH = 'resources/application.properties'

config = configparser.ConfigParser()
config.read(APPLICATION_PROPERTIES_PATH)


def get_by_key(key: str) -> str:
    return config.get('database', key)

