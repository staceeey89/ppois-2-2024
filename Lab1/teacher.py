# teacher.py
class Teacher:
    def __init__(self, first_name: str, last_name: str):
        self.first_name = first_name
        self.last_name = last_name

    def consult_with_student(self, student_name: str):
        print(f"Преподаватель {self.first_name} {self.last_name} консультирует студента {student_name}")

