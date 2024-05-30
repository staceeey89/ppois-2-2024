# модуль learning_material.py
class LearningMaterial:
    def __init__(self, title: str, material_subject: str):
        self.title = title
        self.material_subject = material_subject  # название предмета

    def use_for_preparation(self):
        print(f"Используется учебный материал: {self.title} ({self.material_subject})")

