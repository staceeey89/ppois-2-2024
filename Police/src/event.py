from src.law import Law
from utils.ccolors import ccolors


class Event:
    def __init__(self, title: str, description: str, slots: int):
        self.title = title
        self.description = description
        self.slots = slots

    def __str__(self):
        return (f"{ccolors.BOLD}+------------Запрос охраны общественного порядка-------------------{ccolors.DEFAULT}\n"
                f"{ccolors.BOLD}{ccolors.BLUE}{self.title}{ccolors.DEFAULT}\n"
                f"{self.description}\n"
                f"Необходимо назначить {self.slots} офицеров.\n"
                f"{ccolors.BOLD}+------------------------------------------------------------------{ccolors.DEFAULT}")


class Crime(Event):
    def __init__(self, title: str, description: str, slots: int, difficulty: str, law: Law):
        super().__init__(title, description, slots)
        self.difficulty = difficulty
        self.law = law

    def __str__(self):
        return (f"{ccolors.BOLD}+---------------------Совершено преступление-----------------------{ccolors.DEFAULT}\n"
                f"{ccolors.BOLD}{ccolors.BROWN}{self.title}{ccolors.DEFAULT}\n"
                f"{self.description}\n"
                f"Необходимо назначить {self.slots} офицеров.\n"
                f"{ccolors.BOLD}+------------------------------------------------------------------{ccolors.DEFAULT}")


class Call(Event):
    def __init__(self, title: str, description: str, slots: int, difficulty: str, address: str):
        super().__init__(title, description, slots)
        self.difficulty = difficulty
        self.address = address

    def __str__(self):
        return (f"{ccolors.BOLD}+---------------------------Вызов---------------------------------{ccolors.DEFAULT}\n"
                f"{ccolors.BOLD}{ccolors.CYAN}{self.title}{ccolors.DEFAULT}\n"
                f"{self.description}\n"
                f"{self.address}\n"
                # f"Время реакции {self.reaction_time} минут.\n"
                f"Необходимо назначить {self.slots} офицеров.\n"
                f"{ccolors.BOLD}+------------------------------------------------------------------{ccolors.DEFAULT}")
