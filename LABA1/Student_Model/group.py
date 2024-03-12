from .student import Student
from .exam import Exam


class Group:

    def __init__(self, name):
        self.__name: str = name
        self.__students: list[Student] = []
        self.__exams: list[Exam] = []

    def get_name(self):
        return self.__name

    def add_exam(self, exam: Exam) -> None:
        self.__exams.append(exam)

    def get_list_of_exams(self) -> list[Exam]:
        return self.__exams

    def add_student(self, student: Student) -> None:
        self.__students.append(student)

    def expel_student(self, index: int) -> None:
        del self.__students[index]

    def get_list_of_students(self) -> list[Student]:
        return self.__students

