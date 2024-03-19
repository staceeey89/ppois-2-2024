import uuid

from controller.search_criteria import SearchCriteria
from model.absence import Absence
from model.absence_reason import AbsenceReason
from model.group import Group
from model.student import Student


class AbstractRepository:
    def count_students_amount(self, search_criteria: SearchCriteria) -> int:
        pass

    def count_absences_amount(self, student_id: uuid.UUID | None) -> int:
        pass

    def delete_students(self, search_criteria: SearchCriteria) -> int:
        pass

    def delete_student(self, student_id: uuid.UUID):
        pass

    def get_students(self, search_criteria: SearchCriteria) -> list[Student]:
        pass

    def get_student(self, student_id: uuid.UUID) -> Student:
        pass

    def add_student(self, name: str, group_id: uuid.UUID):
        pass

    def add_group(self, group_number: int) -> None:
        pass

    def delete_group(self, group_id: uuid.UUID) -> None:
        pass

    def get_groups(self) -> list[Group]:
        pass

    def get_group(self, group_id: uuid.UUID) -> Group:
        pass

    def add_absence_reason(self, reason_name: str, reason_desc: str | None) -> None:
        pass

    def delete_absence_reason(self, reason_id: uuid.UUID) -> None:
        pass

    def get_absence_reasons(self) -> list[AbsenceReason]:
        pass

    def get_absence_reason(self, reason_id: uuid.UUID) -> AbsenceReason:
        pass

    def get_absences(self, student_id: uuid.UUID | None, page_number: int = 1, page_size: int = 10) -> list[Absence]:
        pass

    def delete_absence(self, id: uuid.UUID) -> None:
        pass

    def add_absence(self, student_id: uuid.UUID, reason_id: uuid.UUID) -> None:
        pass

