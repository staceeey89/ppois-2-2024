import uuid
from model.group import Group


class Student:
    def __init__(self, id: uuid.UUID, name: str, group: Group,
                 absences_sick: int, absences_other: int, absences_unjust: int, absences_total: int):
        self.id = id
        self.name = name
        self.group = group
        self.absences_sick = absences_sick
        self.absences_other = absences_other
        self.absences_unjust = absences_unjust
        self.absences_total = absences_total

    def __str__(self):
        return (f"{self.id}, Group: {self.group.number}, Student:  Name: {self.name},"
                f" Sick: {self.absences_sick},"
                f" Other: {self.absences_other},"
                f" Unjust: {self.absences_unjust}")
