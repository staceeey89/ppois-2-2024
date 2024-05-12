import sqlite3
from sqlite3 import Connection
from model import Lecturer, Model


class SqlStorage(Model):
    def __init__(self, file: str):
        super().__init__()
        self.conn: Connection = sqlite3.connect(file)

    def __del__(self):
        self.conn.close()

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS lecturers (
                            id INTEGER PRIMARY KEY,
                            Faculty TEXT,
                            Department TEXT,
                            FullName TEXT,
                            AcademicTitle TEXT,
                            AcademicDegree TEXT,
                            YearsOfExperience INTEGER
                        )''')

    def insert(self, lecturer: Lecturer):
        cursor = self.conn.cursor()
        cursor.execute('''INSERT INTO lecturers (Faculty, Department, FullName, AcademicTitle, AcademicDegree, 
        YearsOfExperience) VALUES (?, ?, ?, ?, ?, ?)''', (lecturer.faculty,
                                                          lecturer.department,
                                                          lecturer.full_name,
                                                          lecturer.academic_title,
                                                          lecturer.academic_degree,
                                                          lecturer.years_of_experience))

    def get_len(self) -> int:
        return len(self.get_all_lecturers())

    def get_all_lecturers(self):
        cursor = self.conn.cursor()
        cursor.execute('''SELECT * FROM lecturers''')
        rows = cursor.fetchall()
        lecturers = []
        for row in rows:
            lecturer = Lecturer(*row)
            lecturers.append(lecturer)
        return lecturers

    def get_lecturers_by_index(self, offset, limit):
        cursor = self.conn.cursor()
        cursor.execute('''SELECT * FROM lecturers LIMIT (?) OFFSET (?)''', (limit, offset))
        rows = cursor.fetchall()
        lecturers = []
        for row in rows:
            lecturer = Lecturer(*row)
            lecturers.append(lecturer)
        return lecturers

    def search_by_name(self, name, offset=0, limit=None):
        cursor = self.conn.cursor()
        query = '''SELECT COUNT(*) FROM lecturers WHERE FullName LIKE ?'''
        cursor.execute(query, ('%' + name + '%',))
        total_count = cursor.fetchone()[0]

        query = '''SELECT * FROM lecturers WHERE FullName LIKE ? LIMIT ? OFFSET ?'''
        cursor.execute(query, ('%' + name + '%', limit, offset))
        rows = cursor.fetchall()

        lecturers = []
        for row in rows:
            lecturer = Lecturer(*row)
            lecturers.append(lecturer)

        return lecturers, total_count

    def delete_by_name(self, name):
        cursor = self.conn.cursor()
        cursor.execute('''DELETE FROM lecturers WHERE FullName LIKE ?''', ('%' + name + '%',))
        deleted_count = cursor.rowcount
        return deleted_count

    def collect(self, field):
        cursor = self.conn.cursor()
        cursor.execute(f"SELECT DISTINCT {field} FROM lecturers")
        rows = cursor.fetchall()
        results = []
        for row in rows:
            results.append(row[0])
        return results

    def search_by_department(self, department, offset=0, limit=None):
        cursor = self.conn.cursor()
        query = '''SELECT COUNT(*) FROM lecturers WHERE Department = ?'''
        cursor.execute(query, (department,))
        total_count = cursor.fetchone()[0]

        query = '''SELECT * FROM lecturers WHERE Department = ? LIMIT ? OFFSET ?'''
        cursor.execute(query, (department, limit, offset))
        rows = cursor.fetchall()

        lecturers = []
        for row in rows:
            lecturer = Lecturer(*row)
            lecturers.append(lecturer)

        return lecturers, total_count

    def delete_by_department(self, department):
        cursor = self.conn.cursor()
        cursor.execute('''DELETE FROM lecturers WHERE Department = ?''', (department,))
        deleted_count = cursor.rowcount
        return deleted_count

    def search_by_academic_title_and_faculty(self, academic_title, faculty, offset=0, limit=None):
        cursor = self.conn.cursor()
        query = '''SELECT COUNT(*) FROM lecturers WHERE AcademicTitle = ? AND Faculty = ?'''
        cursor.execute(query, (academic_title, faculty))
        total_count = cursor.fetchone()[0]

        query = '''SELECT * FROM lecturers WHERE AcademicTitle = ? AND Faculty = ? LIMIT ? OFFSET ?'''
        cursor.execute(query, (academic_title, faculty, limit, offset))
        rows = cursor.fetchall()

        lecturers = []
        for row in rows:
            lecturer = Lecturer(*row)
            lecturers.append(lecturer)

        return lecturers, total_count

    def delete_by_academic_title_and_faculty(self, academic_title, faculty):
        cursor = self.conn.cursor()
        cursor.execute('''DELETE FROM lecturers WHERE AcademicTitle = ? AND Faculty = ?''',
                       (academic_title, faculty))
        deleted_count = cursor.rowcount
        return deleted_count

    def search_by_experience(self, lower_limit, upper_limit, offset=0, limit=None):
        cursor = self.conn.cursor()
        query = '''SELECT COUNT(*) FROM lecturers WHERE YearsOfExperience BETWEEN ? AND ?'''
        cursor.execute(query, (lower_limit, upper_limit))
        total_count = cursor.fetchone()[0]

        query = '''SELECT * FROM lecturers WHERE YearsOfExperience BETWEEN ? AND ? LIMIT ? OFFSET ?'''
        cursor.execute(query, (lower_limit, upper_limit, limit, offset))
        rows = cursor.fetchall()

        lecturers = []
        for row in rows:
            lecturer = Lecturer(*row)
            lecturers.append(lecturer)

        return lecturers, total_count

    def delete_by_experience(self, lower_limit, upper_limit):
        cursor = self.conn.cursor()
        cursor.execute('''DELETE FROM lecturers WHERE YearsOfExperience BETWEEN ? AND ?''',
                       (lower_limit, upper_limit))
        deleted_count = cursor.rowcount
        return deleted_count

    def save(self):
        self.conn.commit()
