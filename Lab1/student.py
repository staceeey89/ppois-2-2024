# student.py
import re
from typing import Dict, List, Tuple
from exam import Exam
from learning_material import LearningMaterial
from additional_classes import AdditionalClasses
from teacher import Teacher
# from main import exam_system


def is_valid_name(name: str) -> bool:
    pattern = r'^[a-zA-Zа-яА-Я]+$'
    return bool(re.match(pattern, name))


def add_student(self) -> None:
    first_name = input("Введите имя студента: ")
    while not is_valid_name(first_name):
        print("Имя должно состоять только из букв.")
        first_name = input("Введите имя студента: ")
    last_name = input("Введите фамилию студента: ")
    while not is_valid_name(last_name):
        print("Фамилия должна состоять только из букв.")
        last_name = input("Введите фамилию студента: ")
    group = input("Введите группу студента (6 цифр): ")
    while not re.match(r"^\d{6}$", group):
        print("Номер группы должен состоять из 6 цифр.")
        group = input("Введите группу студента (6 цифр): ")
    student = Student(first_name, last_name, group)

    self.exam_system.add_student(student)
    print(f"Студент {first_name} {last_name} добавлен.")


class Student:
    def __init__(self, first_name: str, last_name: str, group: str):
        self.first_name = first_name
        self.last_name = last_name
        self.validate_group_number(group)
        self.group = group
        self.exams: Dict[str, Exam] = {}
        self.resits = 0  # Количество пересдач
        self.learning_materials: List[LearningMaterial] = []
        self.additional_classes: List[AdditionalClasses] = []
        self.consultations: List[Tuple[str, str]] = []

    def add_exam(self, exam: Exam):
        self.exams[exam.name] = exam

    @staticmethod
    def validate_group_number(group: str):
        if not re.match(r"^\d{6}$", group):
            raise ValueError("Номер группы должен состоять из 6 цифр.")

    def add_score(self, exam_name: str, score: int):
        if exam_name not in self.exams:
            raise ValueError(f"Экзамен '{exam_name}' не найден.")
        self.exams[exam_name].add_score(score)
        if score < 4:
            self.resits += 1

    def add_learning_material(self, material: LearningMaterial):
        self.learning_materials.append(material)

    def attend_additional_class(self, additional_class: AdditionalClasses):
        self.additional_classes.append(additional_class)

    def add_consultation(self, teacher_name: str, subject: str):
        self.consultations.append((subject, teacher_name))

    def analyze(self):

        # Создаем общий отчет о студенте
        report = [f"Студент: {self.first_name} {self.last_name}", f"Группа: {self.group}",
                  f"Количество пересдач: {self.resits}", "Экзамены:"]

        # Информация об экзаменах
        for exam_name, exam in self.exams.items():
            status = "сдан" if exam.has_passed() else "не сдан"
            report.append(f"  - {exam_name}: {exam.scores} (статус: {status})")

        # Информация об учебных материалах
        report.append("Учебные материалы:")
        if self.learning_materials:
            for material in self.learning_materials:
                report.append(f"  - {material.material_subject} ({material.title})")
        else:
            report.append("  - Нет учебных материалов.")

        # Информация о дополнительных занятиях
        report.append("Дополнительные занятия:")
        if self.additional_classes:
            for additional_class in self.additional_classes:
                report.append(f"  - {additional_class.title} (дата: {additional_class.date})")
        else:
            report.append("  - Нет дополнительных занятий.")

        # Информация о консультациях
        report.append("Консультации:")
        if self.consultations:
            for subject, teacher_name in self.consultations:
                report.append(f"  - {subject} с преподавателем {teacher_name}")
        else:
            report.append("  - Нет консультаций.")

            # Возвращаем полный отчет
        return "\n".join(report)

    def analyze_test(self, exam_name):
        report = [f"Студент: {self.first_name} {self.last_name}", f"Группа: {self.group}", f"Экзамен: {exam_name}",
                  "Учебные материалы:"]
        # Информация об учебных материалах
        l_m = 0
        if self.learning_materials:
            for material in self.learning_materials:
                if material.material_subject == exam_name:
                    report.append(f"  - {material.material_subject} ({material.title})")
                    l_m = l_m + 1
        else:
            report.append("  - Нет учебных материалов.")

        # Информация о дополнительных занятиях
        a_c = 0
        if self.additional_classes:
            for additional_class in self.additional_classes:
                if additional_class.title == exam_name:
                    report.append(f"  - {additional_class.title} (дата: {additional_class.date})")
                    a_c = a_c + 1
        else:
            report.append("  - Нет дополнительных занятий.")

        if l_m >= 1 or a_c >= 1:
            report.append(" Тест сдан!!!")
        else:
            report.append(" Тест не сдан:( ")
        return report

    def __str__(self):
        return f"{self.first_name} {self.last_name} из группы {self.group}"
