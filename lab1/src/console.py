from src.compiler import Compiler
from src.person import Programmer
from src.programming_language import ProgrammingLanguage
import time
import sys
import pickle


def print_slow(str):
    for letter in str:
        print(letter, end='', flush=True)
        time.sleep(0.05)


def get_source_code():
    source_code: str = ""
    while True:
        code = input("Введите строчку кода. Если код написан, введите \"Сохранить код\": ")
        if code == "Сохранить код":
            break
        else:
            source_code += code + "\n"
    return source_code


def get_key_word_dictionary(key_word_dictionary: dict) -> dict:
    while True:
        key = input("Введите ключевое слово: ").split()
        if len(key) > 1:
            print(f"Ключевое слово должно состоять из одного слова")
            continue
        while True:
            category = int(
                input("Введите к какой категории относится ключевое слово(1 - \"dataType\",2 - \"singleOperator\"): "))
            if category < 1 and category > 2:
                print(f"Не верно выбрана категория ключевого слова")
                continue
            else:
                if category == 1:
                    category = "dataType"
                else:
                    category = "singleOperator"
                key_word_dictionary[key[0]] = category
                break
        choose = input("Если желаете закончить ввод ключевых слов, введите \"Закончить ввод\": ")
        if choose == "Закончить ввод":
            return key_word_dictionary


def write_source_code(operation: int, programmer: Programmer):
    source_code: str = ""
    description: str = ""
    file_extension: str = ""
    if operation == 1:
        source_code = get_source_code()
        description = input("Введите описание вашего кода: ")
        file_extension = input("Введите расширение файла: ")
        programmer.write_source_code(file_extension, source_code, description)
    if operation == 2:
        source_code = get_source_code()
        programmer.change_source_code(source_code)
    if operation == 3:
        description = input("Введите описание вашего кода: ")
        programmer.change_desription(description)

def write_personal_data(programmer: Programmer) -> Programmer:
    while True:
        fio = input("Введите ФИО программиста: ")
        age = int(input("Введите возраст: "))
        experience = int(input("Введи опыт работы: "))
        if len(fio) >= 2 and len(fio) <= 3 or age >= 18 and age <= 120:
            programmer.set_personal_data(fio, age, experience)
            return programmer
        else:
            print(f"Возраст или ФИО введены некорректно")

def write_programming_language_settings() -> ProgrammingLanguage:
    language = input("Введите название языка программирования: ")
    key_word_dictionary = {}
    key_word_dictionary = get_key_word_dictionary(key_word_dictionary)
    file_extension = input("Введите расширение исполняющегося файла: ")
    programming_language = ProgrammingLanguage(language, file_extension, key_word_dictionary)
    return programming_language

if __name__ == "__main__":
    programmer = Programmer()
    try:
        with open("personal_data", "rb") as file:
            programmer = pickle.load(file)
        with open("programming_language", "rb") as file:
            programming_language = pickle.load(file)
        print(f"Сохраненные данные были загружены")
    except FileNotFoundError:
        print(f"Сохраненные данные не были найдены")
        programmer = write_personal_data(programmer)
        programming_language = write_programming_language_settings()
        write_source_code(1, programmer)

    while True:
        print(
            f"1) Перезаписать проект\n2) Перезаписать исходный код\n3) Перезаписать описание\n4) Перезаписать данные программиста\n5) Перезаписать настройки языка"
            f"\n6) Перейти к компиляции")
        try:
            choose = int(input("Выберите операцию: "))
            if choose == 4:
                programmer = write_personal_data(programmer)
            if choose == 5:
                programming_language = write_programming_language_settings()
            if choose == 6:
                break
            if choose > 6 or choose < 1:
                print(f"Некорректный номер операции")
            else:
                write_source_code(choose, programmer)

        except ValueError:
            print(f"Введите число соответствующее номеру операции")

    with open("personal_data", "wb") as file:
        pickle.dump(programmer, file)
    with open("programming_language", "wb") as file:
        pickle.dump(programming_language, file)

    operators = {"+": ["int", "float", "string"], "-": ["int", "float"], "=": ["int", "float", "string"],
                 "*": ["int", "float"], "/": ["int", "float"]}
    compiler = Compiler()
    compiler.compile_the_project(programmer.get_source_code(), programming_language, operators)
    message = "========================= Идёт компиляция ========================="
    print_slow(message)
    print(compiler)
    print("Работа программы завершена")
