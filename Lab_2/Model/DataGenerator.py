from Model.StudentsDB import StudentsDB
import random

class DataGenerator:
    russian_names = ["Александр", "Михаил", "Иван", "Артем", "Дмитрий", "Егор", "Андрей", "Никита", "Владимир", "Кирилл", "Максим", "Павел", "Роман", "Илья", "Сергей"]
    russian_surnames = ["Иванов", "Петров", "Сидоров", "Васильев", "Попов", "Алексеев", "Лебедев", "Семенов", "Егоров", "Федоров", "Никитин", "Соловьев", "Тимофеев", "Козлов", "Волков"]
    russian_patronymics = ["Александрович", "Михайлович", "Иванович", "Артемович", "Дмитриевич", "Егорович", "Андреевич", "Никитич", "Владимирович", "Кириллович", "Максимович", "Павлович", "Романович", "Ильич", "Сергеевич"]

    subjects = ["Математика", "Физика", "Химия", "Биология", "История", "Литература", "Информатика", "География", "Искусство", "Музыка", "Физкультура", "Экономика", "Психология", "Социология", "Ин.яз."]

    def __init__(self, n: int, data_base):
        self.data_base = data_base
        self.num_students = n
        self.num_groups = random.randint(n // 7, n // 3)
        self.generated_groups = {}
        self.generate_groups()
        self.generate_student_data()

    def generate_groups(self) -> None:
        while len(self.generated_groups) < self.num_groups:
            group_number = random.randint(100000, 999999)
            group_subjects = random.sample(DataGenerator.subjects, random.randint(3, len(DataGenerator.subjects)))
            self.generated_groups[group_number] = group_subjects
            self.data_base.add_group(group_number,group_subjects)
    @staticmethod
    def generate_full_name() -> str:
        return f"{random.choice(DataGenerator.russian_surnames)} {random.choice(DataGenerator.russian_names)} {random.choice(DataGenerator.russian_patronymics)}"

    def generate_student_data(self) -> None:
        if not self.generated_groups:
            return
        for _ in range(self.num_students):
            full_name = DataGenerator.generate_full_name()
            if not self.generated_groups is None:
                group_number = random.choice(list(self.generated_groups.keys()))
            grades = [(subject, random.randint(1, 10)) for subject in self.generated_groups[group_number]]
            self.data_base.add_student(full_name, group_number, grades)

