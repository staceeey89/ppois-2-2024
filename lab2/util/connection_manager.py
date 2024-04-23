import psycopg2
from util import properties_util as database_properties


class ConnectionManager:
    USER: str = database_properties.get_by_key("user")
    PASSWORD: str = database_properties.get_by_key("password")
    HOST: str = database_properties.get_by_key("host")
    PORT: str = database_properties.get_by_key("port")
    DATABASE = database_properties.get_by_key("database")

    @staticmethod
    def open():
        return psycopg2.connect(user=ConnectionManager.USER,
                                password=ConnectionManager.PASSWORD,
                                host=ConnectionManager.HOST,
                                port=ConnectionManager.PORT,
                                database=ConnectionManager.DATABASE)
