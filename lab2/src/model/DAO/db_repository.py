import os.path
import sqlite3

from src.model.user import User
from src.exception.nothing_found_exception import NothingFoundException
from src.model.DAO.repository import Repository


class DBRepository(Repository):
    select_user = """SELECT 
            users.id, 
            users.name, 
            users.surname, 
            users.patronym,
            users.account, 
            users.address, 
            users.mobileNumber, 
            users.landlineNumber 
            FROM users
            """

    def __init__(self, file_name):
        if (ext := os.path.splitext(file_name)[1]) != ".sqlite":
            raise ValueError(f"Invalid file extension: {ext}")

        self._connection = sqlite3.connect(file_name)
        self._connection.enable_load_extension(True)
        self._connection.load_extension("libs/regexp.so")

    def __del__(self):
        self._connection.close()
        print("Connection closed")

    def save(self, user: User) -> None:
        cursor = self._connection.cursor()
        try:
            cursor.execute(
                f"UPDATE users SET "
                f"name ='{user.name}', "
                f"surname ='{user.surname}', "
                f"patronim ='{user.patronymic}' "
                f"account = '{user.account}' "
                f"address ='{user.address}' "
                f"mobileNumber ='{user.mobile_number}' "
                f"landlineNumber ='{user.landline_number}' "
                f"WHERE id ='{user.user_id}'"
            )
        except sqlite3.OperationalError:
            cursor.execute(
                f"""INSERT INTO users (name, surname, patronym, account, address, mobileNumber, landlineNumber) VALUES (
                '{user.name}', 
                '{user.surname}', 
                '{user.patronymic}',
                '{user.account}', 
                '{user.address}', 
                '{user.mobile_number}', 
                '{user.landline_number}')
                """
            )
        if cursor.rowcount == 0:
            cursor.close()
            raise NothingFoundException
        cursor.close()

    def get(self, idtf: str) -> User:
        cursor = self._connection.cursor()
        cursor.execute(self.select_user + f"WHERE users.id == {idtf}")
        user = cursor.fetchone()
        if not user:
            cursor.close()
            raise NothingFoundException
        cursor.close()
        return user

    def find(self, conditions: str, *parameters) -> list[User]:
        cursor = self._connection.cursor()
        cursor.execute(
            self.select_user +
            f"""WHERE {conditions}
            ORDER BY id 
            """,
            parameters
        )
        users = cursor.fetchall()
        if not users:
            cursor.close()
            raise NothingFoundException
        cursor.close()
        return list(map(lambda x: User(*x), users))

    def list(self, *, offset: int = 0, count: int | None = None) -> list[User]:
        cursor = self._connection.cursor()
        if count is None:
            cursor.execute(self.select_user + "ORDER BY id")
        else:
            cursor.execute(
                self.select_user +
                f"""ORDER BY id 
                LIMIT {offset}, {count}
                """
            )
        users = cursor.fetchall()
        if not users:
            cursor.close()
            raise NothingFoundException
        cursor.close()
        return list(map(lambda x: User(*x), users))

    def erase(self, user: User):
        cursor = self._connection.cursor()
        cursor.execute(
            f"DELETE FROM users WHERE id={user.user_id}"
        )
        cursor.close()

    def commit(self):
        self._connection.commit()

    def count(self) -> int:
        cursor = self._connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM users")
        count = cursor.fetchone()[0]
        cursor.close()
        return count

    def create_table(self):
        cursor = self._connection.cursor()
        cursor.execute("""
            CREATE TABLE "users" (
                "ID"	INTEGER NOT NULL,
                "Name"	TEXT NOT NULL,
                "Surname"	TEXT NOT NULL,
                "Patronym"	TEXT NOT NULL,
                "Account"	TEXT NOT NULL,
                "Address"	TEXT NOT NULL,
                "MobileNumber"	TEXT NOT NULL,
                "LandlineNumber"	TEXT NOT NULL,
                PRIMARY KEY("ID" AUTOINCREMENT)
            );
        """)
        cursor.close()
