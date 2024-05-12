import sqlite3
from typing import List, Tuple, Optional
import xml.etree.ElementTree as ET


class StudentsDB:
    def __init__(self, db_path: str):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS Students (
                                   student_id INTEGER PRIMARY KEY,
                                   full_name TEXT,
                                   group_number INTEGER,
                                   average_grade REAL
                                   )''')

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS Exams (
                                   exam_id INTEGER PRIMARY KEY,
                                   exam_name TEXT
                                   )''')

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS Exam_Groups (
                                   group_id INTEGER,
                                   exam_id INTEGER,
                                   FOREIGN KEY (group_id) REFERENCES Students(group_number),
                                   FOREIGN KEY (exam_id) REFERENCES Exams(exam_id),
                                   PRIMARY KEY (group_id, exam_id)
                                   )''')

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS Grades (
                                   grade_id INTEGER PRIMARY KEY,
                                   student_id INTEGER,
                                   exam_id INTEGER,
                                   grade INTEGER,
                                   FOREIGN KEY (student_id) REFERENCES Students(student_id),
                                   FOREIGN KEY (exam_id) REFERENCES Exams(exam_id)
                                   )''')
        self.conn.commit()

    def get_unique_exam_names(self) -> List[str]:
        self.cursor.execute("SELECT DISTINCT exam_name FROM Exams")
        return [row[0] for row in self.cursor.fetchall()]

    def check_exam_exist(self, exam_name: str) -> bool:
        self.cursor.execute("SELECT COUNT(*) FROM Exams WHERE exam_name = ?", (exam_name,))
        count: int = self.cursor.fetchone()[0]
        return count > 0

    def get_students_name_and_group(self, student_ids: List[int]) -> List[Tuple[str, int]]:
        results = []

        query = '''SELECT full_name, group_number
                    FROM Students
                    WHERE student_id = ?'''

        for student_id in student_ids:
            self.cursor.execute(query, (student_id,))
            student_info = self.cursor.fetchone()
            if student_info:
                results.append(student_info)

        return results

    def get_student_info(self, student_id: int) -> Optional[Tuple[str, int, int, List[Tuple[str, int]]]]:
        self.cursor.execute('''SELECT full_name, group_number, average_grade FROM Students WHERE student_id = ?''',
                            (student_id,))
        student_info = self.cursor.fetchone()
        if student_info:
            full_name: str
            group_number: int
            average_grade: int
            full_name, group_number, average_grade = student_info

            # Retrieve exam grades for the student
            self.cursor.execute('''SELECT Exams.exam_name, Grades.grade FROM Exams
                                   JOIN Grades ON Exams.exam_id = Grades.exam_id
                                   WHERE Grades.student_id = ?''', (student_id,))
            exam_grades: List[Tuple[str, int]] = self.cursor.fetchall()

            return full_name, group_number, average_grade, exam_grades
        else:
            return None

    def get_exam_names(self) -> List[str]:
        self.cursor.execute("SELECT DISTINCT exam_name FROM Exams")
        unique_exam_names = self.cursor.fetchall()
        return [row[0] for row in unique_exam_names]

    def get_students_in_group(self, group_number: int) -> List[int]:
        self.cursor.execute('''SELECT student_id FROM Students WHERE group_number = ?''', (group_number,))
        student_ids = self.cursor.fetchall()
        return [student[0] for student in student_ids]

    def get_group_number_by_student_id(self, student_id: int) -> Optional[int]:
        query = "SELECT group_number FROM Students WHERE student_id = ?"
        self.cursor.execute(query, (student_id,))
        result = self.cursor.fetchone()
        return result[0] if result else None

    def get_students_by_group_number(self, group_number: int) -> List[int]:
        query = "SELECT student_id FROM Students WHERE group_number = ?"
        self.cursor.execute(query, (group_number,))
        return [row[0] for row in self.cursor.fetchall()]

    def get_exam_id_by_name(self, exam_name: str) -> Optional[int]:
        query = "SELECT exam_id FROM Exams WHERE exam_name = ?"
        self.cursor.execute(query, (exam_name,))
        result = self.cursor.fetchone()
        return result[0] if result else None

    def get_students_by_average_grade_range(self, min_average_grade: float, max_average_grade: float, exam_name: str) ->List[int]:
        exam_id = self.get_exam_id_by_name(exam_name)
        if exam_id is None:
            return []


        query = """SELECT S.student_id
                   FROM Students S
                   JOIN Grades G ON G.student_id = S.student_id
                   WHERE S.average_grade BETWEEN ? AND ? AND G.exam_id = ?"""
        self.cursor.execute(query, (min_average_grade, max_average_grade, exam_id))
        return [row[0] for row in self.cursor.fetchall()]

    def get_students_by_score_range(self, exam_name: str, min_score: float, max_score: float) -> List[int]:
        query = """
               SELECT s.student_id
               FROM Students s
               JOIN Grades g ON s.student_id = g.student_id
               JOIN Exams e ON g.exam_id = e.exam_id
               WHERE e.exam_name = ? AND g.grade BETWEEN ? AND ?
           """
        self.cursor.execute(query, (exam_name, min_score, max_score))
        rows = self.cursor.fetchall()
        return [row[0] for row in rows]

    def delete_students_and_grades_by_ids(self, student_ids: List[int]) -> None:
        for student_id in student_ids:
            group_number = \
            self.cursor.execute("SELECT group_number FROM Students WHERE student_id = ?", (student_id,)).fetchone()[0]
            count = \
            self.cursor.execute("SELECT COUNT(*) FROM Students WHERE group_number = ?", (group_number,)).fetchone()[0]

            self.cursor.execute("DELETE FROM Grades WHERE student_id=?", (student_id,))
            self.cursor.execute("DELETE FROM Students WHERE student_id=?", (student_id,))
            if count == 1:
                self.cursor.execute("DELETE FROM Exam_Groups WHERE group_id=?", (group_number,))

        self.conn.commit()

    def add_student(self, full_name: str, group_number: int, grades: List[Tuple[str, int]]) -> None:
        total_grades = sum(grade for _, grade in grades)
        average_grade = total_grades / len(grades) if grades else 0  # предотвращаем деление на ноль

        query_student = """INSERT INTO Students (full_name, group_number, average_grade)
                           VALUES (?, ?, ?)"""
        self.cursor.execute(query_student, (full_name, group_number, average_grade))
        student_id = self.cursor.lastrowid

        for exam_name, grade in grades:
            exam_id = self.get_exam_id_by_name(exam_name)
            if exam_id is None:
                continue

            query_grade = "INSERT INTO Grades (student_id, exam_id, grade) VALUES (?, ?, ?)"
            self.cursor.execute(query_grade, (student_id, exam_id, grade))
        self.conn.commit()

    def add_group(self, group_number: int, exam_names: List[str]) -> None:
        for exam_name in exam_names:
            if not self.check_exam_exists(exam_name):
                self.cursor.execute("INSERT INTO Exams (exam_name) VALUES (?)", (exam_name,))
                exam_id = self.cursor.lastrowid
            else:
                exam_id = self.get_exam_id_by_name(exam_name)

            self.cursor.execute("INSERT INTO Exam_Groups (group_id, exam_id) VALUES (?, ?)", (group_number, exam_id))

        self.conn.commit()

    def get_subjects_by_group_number(self, group_number: int) -> List[str]:
        self.cursor.execute('''SELECT exam_id FROM Exam_Groups WHERE group_id = ?''', (group_number,))
        exam_ids = self.cursor.fetchall()

        subjects = []
        for exam_id in exam_ids:
            exam_id = exam_id[0]
            self.cursor.execute('''SELECT exam_name FROM Exams WHERE exam_id = ?''', (exam_id,))
            subject = self.cursor.fetchone()
            if subject:
                subjects.append(subject[0])

        return subjects

    def get_all_group_numbers(self) -> List[int]:
        query = "SELECT DISTINCT group_id FROM Exam_Groups"
        self.cursor.execute(query)
        return [row[0] for row in self.cursor.fetchall()]

    def check_group_exists(self, group_number: int) -> bool:
        query = "SELECT EXISTS(SELECT 1 FROM Exam_Groups WHERE group_id = ?)"
        self.cursor.execute(query, (group_number,))
        result = self.cursor.fetchone()
        return bool(result[0])

    def check_exam_exists(self, exam_name: str) -> bool:
        query = "SELECT EXISTS(SELECT 1 FROM Exams WHERE exam_name = ?)"
        self.cursor.execute(query, (exam_name,))
        result = self.cursor.fetchone()
        return bool(result[0])

    def check_student_exists_in_group(self, full_name: str, group_number: int) -> bool:
        query = "SELECT EXISTS(SELECT 1 FROM Students WHERE full_name = ? AND group_number = ?)"
        self.cursor.execute(query, (full_name, group_number))
        result = self.cursor.fetchone()
        return bool(result[0])

    def export_all_tables_to_xml(self, file_path: str):
        root = ET.Element("database")

        self.cursor.execute('''SELECT * FROM Students''')
        students_data = self.cursor.fetchall()
        students_element = ET.SubElement(root, "students")
        for student in students_data:
            student_element = ET.SubElement(students_element, "student")
            for index, column in enumerate(["student_id", "full_name", "group_number", "average_grade"]):
                ET.SubElement(student_element, column).text = str(student[index])

        self.cursor.execute('''SELECT * FROM Exams''')
        exams_data = self.cursor.fetchall()
        exams_element = ET.SubElement(root, "exams")
        for exam in exams_data:
            exam_element = ET.SubElement(exams_element, "exam")
            for index, column in enumerate(["exam_id", "exam_name"]):
                ET.SubElement(exam_element, column).text = str(exam[index])

        self.cursor.execute('''SELECT * FROM Exam_Groups''')
        exam_groups_data = self.cursor.fetchall()
        exam_groups_element = ET.SubElement(root, "exam_groups")
        for group in exam_groups_data:
            group_element = ET.SubElement(exam_groups_element, "exam_group")
            for index, column in enumerate(["group_id", "exam_id"]):
                ET.SubElement(group_element, column).text = str(group[index])

        self.cursor.execute('''SELECT * FROM Grades''')
        grades_data = self.cursor.fetchall()
        grades_element = ET.SubElement(root, "grades")
        for grade in grades_data:
            grade_element = ET.SubElement(grades_element, "grade")
            for index, column in enumerate(["grade_id", "student_id", "exam_id", "grade"]):
                ET.SubElement(grade_element, column).text = str(grade[index])

        tree = ET.ElementTree(root)
        tree.write(file_path)

    def import_all_tables_from_xml(self, file_path: str):
        tree = ET.parse(file_path)
        root = tree.getroot()

        students_element = root.find("students")
        if students_element is not None:
            self.cursor.execute('''DELETE FROM Students''')
            for student_element in students_element.findall("student"):
                student_data = [int(student_element.find("student_id").text),
                                student_element.find("full_name").text,
                                int(student_element.find("group_number").text),
                                float(student_element.find("average_grade").text)]
                self.cursor.execute('''INSERT INTO Students (student_id, full_name, group_number, average_grade) 
                                       VALUES (?, ?, ?, ?)''', student_data)

        # Загружаем данные таблицы Exams
        exams_element = root.find("exams")
        if exams_element is not None:
            self.cursor.execute('''DELETE FROM Exams''')
            for exam_element in exams_element.findall("exam"):
                exam_data = [int(exam_element.find("exam_id").text),
                             exam_element.find("exam_name").text]
                self.cursor.execute('''INSERT INTO Exams (exam_id, exam_name) VALUES (?, ?)''', exam_data)

        # Загружаем данные таблицы Exam_Groups
        exam_groups_element = root.find("exam_groups")
        if exam_groups_element is not None:
            self.cursor.execute('''DELETE FROM Exam_Groups''')
            for group_element in exam_groups_element.findall("exam_group"):
                group_data = [int(group_element.find("group_id").text),
                              int(group_element.find("exam_id").text)]
                self.cursor.execute('''INSERT INTO Exam_Groups (group_id, exam_id) VALUES (?, ?)''', group_data)

        # Загружаем данные таблицы Grades
        grades_element = root.find("grades")
        if grades_element is not None:
            self.cursor.execute('''DELETE FROM Grades''')
            for grade_element in grades_element.findall("grade"):
                grade_data = [int(grade_element.find("grade_id").text),
                              int(grade_element.find("student_id").text),
                              int(grade_element.find("exam_id").text),
                              int(grade_element.find("grade").text)]
                self.cursor.execute(
                    '''INSERT INTO Grades (grade_id, student_id, exam_id, grade) VALUES (?, ?, ?, ?)''', grade_data)

        self.conn.commit()


