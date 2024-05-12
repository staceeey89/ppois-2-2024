import sqlite3


class StudentModel:
    def __init__(self, db_file_path):
        self.db_conn = sqlite3.connect(db_file_path)
        self.create_tables()

    def create_tables(self):
        cursor = self.db_conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS students (
                            id INTEGER PRIMARY KEY,
                            fio TEXT NOT NULL,
                            group_num TEXT NOT NULL,
                            sick_absent INTEGER,
                            other_absent INTEGER,
                            unexcused_absent INTEGER
                        )''')
        self.db_conn.commit()

    def fetch_students(self):
        cursor = self.db_conn.cursor()
        cursor.execute("SELECT * FROM students")
        return cursor.fetchall()

    def count_students(self):
        cursor = self.db_conn.cursor()
        cursor.execute('''SELECT COUNT(*) FROM students''')
        return cursor.fetchone()[0]

    def insert_student(self, fio, group_num, sick_absent, other_absent, unexcused_absent):
        cursor = self.db_conn.cursor()
        cursor.execute(
            "INSERT INTO students (fio, group_num, sick_absent, other_absent, unexcused_absent) "
            "VALUES (?, ?, ?, ?, ?)",
            (fio, group_num, sick_absent, other_absent, unexcused_absent))
        self.db_conn.commit()

    def update_students(self, students_data):
        cursor = self.db_conn.cursor()
        for student in students_data:
            cursor.execute("""UPDATE students 
                                   SET fio=?, group_num=?, sick_absent=?, other_absent=?, unexcused_absent=? 
                                   WHERE id=?""",
                           (student['fio'], student['group'], student['sick_absent'],
                            student['other_absent'], student['unexcused_absent'], student['id']))
        self.db_conn.commit()

    def close_connection(self):
        self.db_conn.close()
