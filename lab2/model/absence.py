import uuid
from datetime import datetime
from model.absence_reason import AbsenceReason
from model.student import Student


class Absence:
    def __init__(self, id: uuid.UUID, date: datetime.date, student: Student, reason: AbsenceReason):
        self.id = id
        self.reason = reason
        self.student = student
        self.date = date

    def __str__(self):
        return f'{self.id}, Absence: {self.reason.name}, Date: {self.date}'
