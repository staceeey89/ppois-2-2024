# cli.py
import sys
import re

from exam import Exam
from student import Student
from exam_system import ExamSystem
from learning_material import LearningMaterial
from teacher import Teacher
from additional_classes import AdditionalClasses
from student import add_student  # , check_expulsion


class CLI:
    def __init__(self):
        self.exam_system = ExamSystem()

    def run(self) -> None:
        while True:
            print("Доступные действия:")
            print("1. Добавить студента")
            print("2. Добавить оценку")
            print("3. Проверить сдачу экзамена")
            print("4. Тренировочные тесты")
            print("5. Проверить, отчислен ли студент")
            print("6. Консультация с преподавателем")
            print("7. Добавить учебный материал студенту")
            print("8. Добавить дополнительное занятие студенту")
            print("9. Анализ информации о студенте")
            print("10. Удалить студента")
            print("0. Выход")

            choice = input("Выберите действие: ")
            if choice == "1":
                add_student(self)
            elif choice == "2":
                self.add_score()
            elif choice == "3":
                self.check_passed()
            elif choice == "4":
                self.take_test()
            elif choice == "5":
                self.check_expulsion()
            elif choice == "6":
                self.consult_with_teacher()
            elif choice == "7":
                self.add_learning_material()
            elif choice == "8":
                self.add_additional_class()
            elif choice == "9":
                self.analyze_student()
            elif choice == "10":
                self.delete_student()
            elif choice == "0":
                print("Выход...")
                sys.exit(0)
            else:
                print("Неверный выбор. Попробуйте снова.")

    def take_test(self):
        first_name = input("Введите имя студента: ")
        while not self.is_valid_name(first_name):
            print("Имя должно состоять только из букв.")
            first_name = input("Введите имя студента: ")
        last_name = input("Введите фамилию студента: ")
        while not self.is_valid_name(last_name):
            print("Фамилия должна состоять только из букв.")
            last_name = input("Введите фамилию студента: ")
        student = self.exam_system.get_student(first_name, last_name)
        exam_name = input("Введите название экзамена: ")
        if not student:
            print(f"Студент {first_name} {last_name} не найден.")
            return
        report = student.analyze_test(exam_name)
        print("Результаты теста:")
        print(report)

    def consult_with_teacher(self):
        first_name = input("Введите имя студента: ")
        while not self.is_valid_name(first_name):
            print("Имя должно состоять только из букв.")
            first_name = input("Введите имя студента: ")
        last_name = input("Введите фамилию студента: ")
        while not self.is_valid_name(last_name):
            print("Фамилия должна состоять только из букв.")
            last_name = input("Введите фамилию студента: ")
        student = self.exam_system.get_student(first_name, last_name)
        if not student:
            print(f"Студент {first_name} {last_name} не найден.")
            return

        subject = input("Введите предмет: ")
        teacher = self.exam_system.get_teacher(subject)
        if not teacher:
            print(f"Предмет '{subject}' не найден.")
            return

        teacher.consult_with_student(f"{first_name} {last_name}")
        student.add_consultation(teacher.last_name, subject)

    def add_score(self) -> None:
        first_name = input("Введите имя студента: ")
        while not self.is_valid_name(first_name):
            print("Имя должно состоять только из букв.")
            first_name = input("Введите имя студента: ")
        last_name = input("Введите фамилию студента: ")
        while not self.is_valid_name(last_name):
            print("Фамилия должна состоять только из букв.")
            last_name = input("Введите фамилию студента: ")
        exam_name: str = input("Введите название экзамена: ")
        score = int(input("Введите оценку: "))
        student = self.exam_system.get_student(first_name, last_name)
        if not student:
            print(f"Студент {first_name} {last_name} не найден.")
            return
        if exam_name not in student.exams:
            student.add_exam(Exam(exam_name, 4))
        student.add_score(exam_name, score)
        print(f"Оценка {score} добавлена для экзамена '{exam_name}'.")

    def check_passed(self) -> None:
        first_name = input("Введите имя студента: ")
        while not self.is_valid_name(first_name):
            print("Имя должно состоять только из букв.")
            first_name = input("Введите имя студента: ")
        last_name = input("Введите фамилию студента: ")
        while not self.is_valid_name(last_name):
            print("Фамилия должна состоять только из букв.")
            last_name = input("Введите фамилию студента: ")
        exam_name = input("Введите название экзамена: ")
        student = self.exam_system.get_student(first_name, last_name)
        if not student:
            print(f"Студент {first_name} {last_name} не найден.")
            return
        exam = student.exams.get(exam_name)
        if not exam:
            print(f"Экзамен '{exam_name}' не найден у студента {first_name} {last_name}.")
            return

        passed = exam.has_passed()  # Используем метод has_passed() на объекте Exam
        result = "сдал" if passed else "не сдал"
        print(f"Студент {first_name} {last_name} {result} экзамен '{exam_name}'.")

    def check_expulsion(self) -> None:
        first_name = input("Введите имя студента: ")
        while not self.is_valid_name(first_name):
            print("Имя должно состоять только из букв.")
            first_name = input("Введите имя студента: ")
        last_name = input("Введите фамилию студента: ")
        while not self.is_valid_name(last_name):
            print("Фамилия должна состоять только из букв.")
            last_name = input("Введите фамилию студента: ")
        student = self.exam_system.get_student(first_name, last_name)
        if not student:
            print(f"Студент {first_name} {last_name} не найден.")
            return
        if student.resits > 2:
            print(f"Студент {first_name} {last_name} отчислен из-за болеечем 2 пересдач.")
        else:
            print(f"Студент {first_name} {last_name} не отчислен.")

    def add_learning_material(self):
        first_name = input("Введите имя студента: ")
        while not self.is_valid_name(first_name):
            print("Имя должно состоять только из букв.")
            first_name = input("Введите имя студента: ")
        last_name = input("Введите фамилию студента: ")
        while not self.is_valid_name(last_name):
            print("Фамилия должна состоять только из букв.")
            last_name = input("Введите фамилию студента: ")
        student = self.exam_system.get_student(first_name, last_name)
        if not student:
            print(f"Студент {first_name} {last_name} не найден.")
            return

        material_subject = input("Введите название предмета: ")
        material_title = input("Введите название: ")
        material = LearningMaterial(material_title, material_subject)
        student.add_learning_material(material)
        print(f"Учебный материал '{material_subject}' добавлен студенту {first_name} {last_name}.")

    def add_additional_class(self):
        first_name = input("Введите имя студента: ")
        while not self.is_valid_name(first_name):
            print("Имя должно состоять только из букв.")
            first_name = input("Введите имя студента: ")
        last_name = input("Введите фамилию студента: ")
        while not self.is_valid_name(last_name):
            print("Фамилия должна состоять только из букв.")
            last_name = input("Введите фамилию студента: ")
        student = self.exam_system.get_student(first_name, last_name)
        if not student:
            print(f"Студент {first_name} {last_name} не найден.")
            return

        class_title = input("Введите название занятия: ")
        class_date = input("Введите дату занятия(dd.mm.yyyy): ")
        while not re.match(r'^(0[1-9]|[12][0-9]|3[01])\.(0[1-9]|1[012])\.(19|20)\d{2}$', class_date):
            print("Введите дату в формате dd.mm.yyyy")
            class_date = input("Введите дату занятия(dd.mm.yyyy): ")
        additional_class = AdditionalClasses(class_title, class_date)
        student.attend_additional_class(additional_class)
        print(f"Дополнительное занятие '{class_title} {class_date}' добавлено студенту {first_name} {last_name}.")

    def analyze_student(self):
        first_name = input("Введите имя студента: ")
        while not self.is_valid_name(first_name):
            print("Имя должно состоять только из букв.")
            first_name = input("Введите имя студента: ")
        last_name = input("Введите фамилию студента: ")
        while not self.is_valid_name(last_name):
            print("Фамилия должна состоять только из букв.")
            last_name = input("Введите фамилию студента: ")
        student = self.exam_system.get_student(first_name, last_name)
        if not student:
            print(f"Студент {first_name} {last_name} не найден.")
            return
        report = student.analyze()
        print("Полный отчет о студенте:")
        print(report)

    def delete_student(self):
        first_name = input("Введите имя студента: ")
        while not self.is_valid_name(first_name):
            print("Имя должно состоять только из букв.")
            first_name = input("Введите имя студента: ")
        last_name = input("Введите фамилию студента: ")
        while not self.is_valid_name(last_name):
            print("Фамилия должна состоять только из букв.")
            last_name = input("Введите фамилию студента: ")
        self.exam_system.delete_student(first_name, last_name)

    @staticmethod
    def is_valid_name(name: str) -> bool:
        pattern = r'^[a-zA-Zа-яА-Я]+$'
        return bool(re.match(pattern, name))
