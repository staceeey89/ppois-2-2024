from .source_code import SourceCode
class Person:
    def __init__(self, full_name: str = "unknown unknown", age: int = 18):
        self.__check_full_name(full_name)
        self.__check_age(age)
        self.full_name = full_name
        self.age = age

    def __check_full_name(self, full_name: str):
        word_list = full_name.split()
        if len(word_list) > 3 or len(word_list) < 2:
            print(f"ФИО должно содержать от 2 до 3 слов")
        for word in word_list:
            if not self.__is_valid_words(word):
                print(f"ФИО должно использовать только буквы и дефисы")

    def __is_valid_words(self, word: str) -> bool:
        word_without_hyphens = word.replace('-', '')
        return word_without_hyphens.isalpha()

    def __check_age(self, age: int):
        if age < 18 or age > 120:
            print(f"Возраст введён неверно")

    def get_person_info(self) -> str:
        return f"{self.full_name} \nAge: {self.age}"


class Programmer(Person):
    def set_personal_data(self, full_name: str, age: int, experience: int = 0):
        super().__init__(full_name, age)
        self.experience = experience
        self.source_code: SourceCode = SourceCode()

    def __str__(self):
        str = self.get_person_info()
        return f"{str} \nExperience: {self.experience} age"

    def write_source_code(self,file_extension: str, source_code: str ="",descriprion: str = ""):
        self.source_code = SourceCode(source_code,descriprion)
        self.source_code.file_extension = file_extension

    def change_source_code(self,source_code: str):
        self.source_code.change_source_code(source_code)

    def change_desription(self,description: str):
        self.source_code.description = description
    def print_source_code(self):
        print(self.source_code)

    def get_source_code(self) -> SourceCode:
        return self.source_code
