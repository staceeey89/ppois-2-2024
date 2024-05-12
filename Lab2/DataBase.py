import sqlite3


class DataBase:
    def __init__(self, controller):
        self.db = sqlite3.connect(controller.open_file_name)
        self.cursor = self.db.cursor()

    # Функиця создания таблицы юзеров
    def create_table_users(self):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS users (
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            patronymic TEXT NOT NULL,
            user_group TEXT NOT NULL,
            term1 INTEGER,
            term2 INTEGER,
            term3 INTEGER,
            term4 INTEGER,
            term5 INTEGER,
            term6 INTEGER,
            term7 INTEGER,
            term8 INTEGER,
            term9 INTEGER,
            term10 INTEGER,
        """)
        self.db.commit()

    def add_new_user(self, first_name, last_name, patronymic, user_group,
                     term1, term2, term3, term4, term5, term6, term7, term8, term9, term10, controller):
        if first_name == "" and last_name == "" and patronymic == "" and user_group == "":
            return False

        if controller.check_empty_add_user(first_name, last_name, patronymic,
                                           user_group) and controller.check_empty_db_path():
            self.cursor.execute(
                "SELECT * FROM users WHERE first_name=? AND last_name=? AND patronymic=? AND user_group=?",
                (first_name, last_name, patronymic, user_group))

            if self.cursor.fetchone() is None:
                self.cursor.execute("INSERT INTO users (first_name, last_name, patronymic, user_group, term1,"
                                    " term2, term3, term4, term5, term6, term7, term8, term9, term10)"
                                    " VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                                    (first_name, last_name, patronymic, user_group,
                                     term1, term2, term3, term4, term5, term6, term7, term8, term9, term10))
                self.db.commit()
                return True
            else:
                return False
        else:
            return False

    def set_connection(self, open_file_name):
        self.db = sqlite3.connect(open_file_name)
        self.cursor = self.db.cursor()

    def set_open_file_name(self, controller, path=""):
        controller.open_file_name = path


    # Возвращает кол-во юзеров
    def find_num_watch_pages(self):
        self.cursor.execute("SELECT * FROM users")
        users = self.cursor.fetchall()

        return len(users)

    def get_users(self):
        self.cursor.execute("SELECT * FROM users")
        users = self.cursor.fetchall()

        return users

    def get_num_users(self):
        self.cursor.execute("SELECT * FROM users")
        users = self.cursor.fetchall()

        return len(users)

    def get_user_opt(self, num):
        self.cursor.execute("SELECT * FROM users")
        users = self.cursor.fetchall()
        opt = 0
        for i in range(4, 14):
            opt += int(users[num][i])
        return opt

    # Методы для страницы поиска по фамилии и группе
    def get_num_users_search_last_name_group(self, last_name, group):
        # Вычисляет кол-во найденных людей
        counter = 0
        self.cursor.execute("SELECT * FROM users")
        users = self.cursor.fetchall()
        for user in users:
            if user[1] == last_name and user[3] == group:
                counter += 1
        return counter

    def get_pos_users_last_name_group(self, num, last_name, group, last_user):
        # Вычисляет, сколько людей нужно убрать в переходе на страницу
        need_num = num
        counter = 0
        self.cursor.execute("SELECT * FROM users")
        users = self.cursor.fetchall()
        flag = False
        for user in reversed(users):
            if user == last_user:
                flag = True
            if flag:
                if need_num <= 0:
                    return counter
                if user[1] == last_name and user[3] == group:
                    need_num -= 1
                counter += 1
        return counter

    # Методы для страницы поиска по фамилии и кол-ву работы
    def get_num_users_search_last_name_opt(self, last_name, low_opt, high_opt):
        # Вычисляет кол-во найденных людей
        counter = 0
        self.cursor.execute("SELECT * FROM users")
        users = self.cursor.fetchall()
        for user in users:
            opt = sum([int(user[i]) for i in range(4, 14)])
            if user[1] == last_name and low_opt <= opt <= high_opt:
                counter += 1
        return counter

    def get_pos_users_last_name_opt(self, num, last_name, low_opt, high_opt, last_user):
        # Вычисляет, сколько людей нужно убрать в переходе на страницу
        need_num = num
        counter = 0
        self.cursor.execute("SELECT * FROM users")
        users = self.cursor.fetchall()
        flag = False
        for user in reversed(users):
            if user == last_user:
                flag = True
            if flag:
                opt = sum([int(user[i]) for i in range(4, 14)])
                if need_num <= 0:
                    return counter
                if user[1] == last_name and low_opt <= opt <= high_opt:
                    need_num -= 1
                counter += 1
        return counter

    # Методы для страницы поиска по группе и кол-ву работы
    def get_num_users_search_group_opt(self, group, low_opt, high_opt):
        # Вычисляет кол-во найденных людей
        counter = 0
        self.cursor.execute("SELECT * FROM users")
        users = self.cursor.fetchall()
        for user in users:
            opt = sum([int(user[i]) for i in range(4, 14)])
            if user[3] == group and low_opt <= opt <= high_opt:
                counter += 1
        return counter

    def get_pos_users_group_opt(self, num, group, low_opt, high_opt, last_user):
        # Вычисляет, сколько людей нужно убрать в переходе на страницу
        need_num = num
        counter = 0
        flag = False
        self.cursor.execute("SELECT * FROM users")
        users = self.cursor.fetchall()
        for user in reversed(users):
            if user == last_user:
                flag = True
            if flag:
                opt = sum([int(user[i]) for i in range(4, 14)])
                if need_num <= 0:
                    return counter
                if user[3] == group and low_opt <= opt <= high_opt:
                    need_num -= 1
                counter += 1
        return counter

    def delete_last_name_group(self, last_name, group):
        self.cursor.execute(f"DELETE FROM users WHERE last_name = '{last_name}' AND user_group = '{group}'")
        del_num = self.cursor.rowcount
        self.db.commit()
        return del_num

    def delete_last_name_opt(self, last_name, low_opt, high_opt):
        self.cursor.execute(f"DELETE FROM users WHERE last_name = '{last_name}' "
            f"AND (term1 + term2 + term3 + term4 + term5 + term6 + term7 + term8 + term9 + term10) >= {low_opt}"
            f" AND (term1 + term2 + term3 + term4 + term5 + term6 + term7 + term8 + term9 + term10) <= {high_opt}")
        del_num = self.cursor.rowcount
        self.db.commit()
        return del_num

    def delete_group_opt(self, group, low_opt, high_opt):
        self.cursor.execute(f"DELETE FROM users WHERE user_group = '{group}' "
            f"AND (term1 + term2 + term3 + term4 + term5 + term6 + term7 + term8 + term9 + term10) >= {low_opt}"
            f" AND (term1 + term2 + term3 + term4 + term5 + term6 + term7 + term8 + term9 + term10) <= {high_opt}")
        del_num = self.cursor.rowcount
        self.db.commit()
        return del_num

    def exist_users_table(self, controller):
        self.cursor.execute("PRAGMA table_info(users)")
        if self.cursor.fetchone() is not None:
            return True
        else:
            controller.set_open_file_name("")
            self.set_connection(controller.open_file_name)
            return False


