from datetime import datetime
from abc import ABC


class ValidValue(ABC):
    pass


class ValidNumber(ABC):  # a = ValidNumber("Value").value

    def input_number(self, string: str) -> int:  # check correct number
        number: str = input(f"Input {string}: ")
        while not str.isnumeric(number):
            number = input(f"{number} should be a number\nPlease re-enter: ")
        return int(number)

    def input_index(self, string: str, num: int) -> int:  # check correct index
        number: str = input(f"Input {string}: ")
        while not str.isnumeric(number) or int(number) >= num or int(number) < 0:
            number = input(f"{number} should be a valid index\nPlease re-enter: ")
        return int(number)

    def input_number_of_classes(self, string: str) -> int:  # check correct number of classes
        number: str = input(f"Input {string}: ")
        while not str.isnumeric(number) or int(number) > 5 or int(number) < 1:
            number = input(f"{number} should be a valid number and in ranging [1-5]\nPlease re-enter: ")
        return int(number)


class ValidDate(ABC):

    def input_date(self, string: str) -> str:  # check correct date
        date: str = input(f"Input {string} (YYYY-MM-DD): ")
        while True:
            try:
                datetime.strptime(date, "%Y-%m-%d")
                return date
            except ValueError:
                date = input(f"{date} should be a valid date (YYYY-MM-DD)\nPlease re-enter: ")

    def input_time(self, string: str) -> str:  # check correct time
        time: str = input(f"Input {string} (HH:MM): ")
        while True:
            try:
                datetime.strptime(time, "%H:%M")
                return time
            except ValueError:
                time = input(f"{time} should be a valid time (HH:MM)\nPlease re-enter: ")


    def input_ours(self, string: str) -> int:  # check correct ours
        ours: str = input(f"Input {string}: ")
        while not str.isnumeric(ours) or int(ours) > 10 or int(ours) < 1:
            ours = input(f"{ours} should be a number and in ranging [1-10]\nPlease re-enter: ")
        return int(ours)


class ValidSubjectName(ABC):

    def input_subject_name(self, string: str) -> str:  # check correct subject_name
        subject_name: str = input(f"Input {string}: ")
        while not subject_name.isalpha():
            subject_name = input(f"{subject_name} should be a valid subject name\nPlease re-enter: ")
        return subject_name


class ValidInitials(ABC):

    def input_initials(self, string: str) -> str:  # check correct initials
        initials: str = input(f"Input {string}: ")
        words = initials.split()
        while (len(words) != 3 or
               not words[0].isalpha() or not words[0][0].isupper() or not words[0][1:].islower() or
               not words[1].isalpha() or not words[1][0].isupper() or not words[1][1:].islower() or
               not words[2].isalpha() or not words[2][0].isupper() or not words[2][1:].islower()):
           initials = input(f"{initials} should be full name (Surname Firstname Patronymic)\nPlease re-enter: ")
           words = initials.split()
        return initials
