import sqlite3


class ConnectionManager:
    def __init__(self, db_file):
        self.db_file = db_file

    def open(self):
        try:
            conn = sqlite3.connect(self.db_file)
            return conn
        except sqlite3.Error as e:
            return None
