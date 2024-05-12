from typing import List
import re
from tkinter import messagebox

class Controller:
    def __init__(self):
        self.open_pages = set()
        self.database=None

    def open_page(self, page_name):
        if page_name not in self.open_pages:
            self.open_pages.add(page_name)
            return True
        return False

    def close_page(self, page_name):
        if page_name in self.open_pages:
            self.open_pages.remove(page_name)

    def get_all_data(self):
        if self.database is None:return
        groups = self.database.get_all_group_numbers()
        all_students_id = []
        for group_number in groups:
            all_students_id.append(self.database.get_students_in_group(group_number))
        return all_students_id

    def validate_student_data(self, full_name):
        error_messages = []

        pattern = r'^[А-ЯЁа-яёA-Za-z]+ [А-ЯЁа-яёA-Za-z]+ [А-ЯЁа-яёA-Za-z]+$'
        if not re.match(pattern, full_name):
            error_messages.append("ФИО студента содержит недопустимые символы.")

        if not full_name:
            error_messages.append("ФИО студента не должно быть пустым.")

        if len(full_name.split()) != 3:
            error_messages.append("ФИО студента должно содержать три слова: фамилия, имя и отчество.")

        if error_messages:
            raise ValueError("\n".join(error_messages))

    def validate_exam_name(self, input_string):
        error_messages = []
        if not input_string:
            error_messages.append("Строка не должна быть пустой.")
        if len(input_string) > 10:
            error_messages.append("Строка должна содержать не более 10 символов.")
        if not all(char.isalpha() or char.isspace() for char in input_string):
            error_messages.append("Строка должна содержать только буквы и пробелы.")
        if error_messages:
            raise ValueError("\n".join(error_messages))

    def validate_group_number(self, group_number):
        error_messages = []
        if not group_number:
            error_messages.append("Номер группы не должен быть пустым.")
        if not isinstance(group_number, str):
            group_number = str(group_number)
        if not group_number.isdigit():
            error_messages.append("Номер группы должен быть целым числом.")
        if not len(group_number) == 6:
            error_messages.append("Номер группы должен состоять из 6 цифр.")
        if error_messages:
            raise ValueError("\n".join(error_messages))

    def validate_grade_input(self,subject, grade_str):
        if not grade_str:  # Проверка на пустое поле
            raise ValueError(f"Введите оценку для предмета: {subject}")
        elif not grade_str.isdigit():
            raise ValueError(f"Оценка для предмета '{subject}' должна быть числом")
        elif not 1 <= int(grade_str) <= 10:  # Проверка на диапазон
            raise ValueError(f"Оценка для предмета '{subject}' должна быть числом от 1 до 10")

    def validate_grades(self, min_score_str, max_score_str):
        try:
            min_score = float(min_score_str)
            max_score = float(max_score_str)
        except ValueError as e:
            raise ValueError("Баллы должны быть числами") from e

        if not min_score_str:
            raise ValueError("Введите значения для минимального балла.")
        if not max_score_str:
            raise ValueError("Введите значения для максимального балла.")
        if not (1 <= min_score <= 10):
            raise ValueError("Минимальный бал должен быть числом от 1 до 10")
        if not (1 <= max_score <= 10):
            raise ValueError("Максимальный бал должен быть числом от 1 до 10")
        if max_score <= min_score:
            raise ValueError("Максимального бал должен быть больше минимального балла")
        return True


    def add_student(self, full_name, group_id):
        self.database.add_student(full_name, group_id)


    def delete_student(self, full_name):
        if self.database.check_student_exists(full_name):
            self.database.delete_student(full_name)
            messagebox.showinfo("Success", "Студент успешно удален")
        else:
            messagebox.showerror("Error", "Студента с таким ФИО не существует")

    def add_group(self,group_name:str, exame_name_list:List[str]):
        self.database.add_group(group_name,exame_name_list)

    def process_list_of_strings(self,strings):
        if len(strings) < 10:
            # Если количество строк меньше 10, разделить список по переводу строки
            return '\n'.join(strings)
        else:
            # Если количество строк больше или равно 10, склеить каждые 4 элемента пробелом
            # и разделить по переводу строки
            result = ''
            for i in range(0, len(strings), 4):
                result += ' '.join(strings[i:i + 4]) + '\n'
            return result

    def delete_student(self,list_id, parent):
        list_info = self.database.get_students_name_and_group(list_id)
        deleted_students_info = self.process_list_of_strings([" ".join(map(str, item)) for item in list_info])
        result = messagebox.askquestion("Внимание", f"Вы уверены что хотите удалить {len(list_id)} студентов?",
                            parent=parent)
        if result == "yes":
            self.database.delete_students_and_grades_by_ids(list_id)
            messagebox.showinfo("Внимание","Студенты удалены",parent=parent)

