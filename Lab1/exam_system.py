# exam_system.py
from typing import List, Optional
from student import Student
from teacher import Teacher

SUBJECTS = {
    "матанализ": Teacher("Людмила", "Мартынюк"),
    "физика": Teacher("Василий", "Соловей"),
    "оаип": Teacher("Алексей", "Рыков"),
    "тмоис": Teacher("Алина", "Марченко"),
}


class ExamSystem:
    def __init__(self):
        self.students: List[Student] = []
        self.teachers: List[Teacher] = list(SUBJECTS.values())

    def add_student(self, student: Student):
        self.students.append(student)

    def get_student(self, first_name: str, last_name: str) -> Optional[Student]:
        for student in self.students:
            if student.first_name == first_name and student.last_name == last_name:
                return student
        return None

    def delete_student(self, first_name: str, last_name: str) -> None:
        for i, student in enumerate(self.students):
            if student.first_name == first_name and student.last_name == last_name:
                del self.students[i]
                print(f"Студент {first_name} {last_name} удален.")
                return
        print(f"Студент {first_name} {last_name} не найден.")

    @staticmethod
    def get_teacher(subject: str) -> Optional[Teacher]:
        return SUBJECTS.get(subject)

