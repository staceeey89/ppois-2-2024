import psycopg2 as ps
from model.model import *
from view.view import *


def load_data_base():
    host = "localhost"
    dbname = "postgres"
    user = "postgres"
    password = "12345"
    port = 5432
    base = ModelBase(host, dbname, user, password, port)
    base.create_table()

    gui = Interface(base)
    base.close_connection()
