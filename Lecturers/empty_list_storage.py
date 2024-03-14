from typing import List
from model import Model, Lecturer


class EmptyListStorage(Model):
    def __init__(self, *args):
        super().__init__()
        self._lecturers: List[Lecturer] = []

    def insert(self, lecturer: Lecturer):
        self._lecturers.append(lecturer)

    def get_all_lecturers(self) -> List[Lecturer]:
        return self._lecturers

    def get_len(self) -> int:
        return len(self._lecturers)

    def get_lecturers_by_index(self, offset=0, limit=10) -> List[Lecturer]:
        return self._lecturers[offset:offset + limit]

    def search_by_name(self, name, offset=0, limit=None) -> (List[Lecturer], int):
        result = [lecturer for lecturer in self._lecturers if
                  name.lower() in lecturer.full_name.lower()]
        return result[offset:offset + limit], len(result)

    def delete_by_name(self, name) -> int:
        lecturers_to_remove = [lecturer for lecturer in self._lecturers if name.lower() in lecturer.full_name.lower()]
        for lecturer in lecturers_to_remove:
            self._lecturers.remove(lecturer)
        return len(lecturers_to_remove)

    def collect(self, field: str):
        field = field.lower().replace(' ', '')
        field = field.replace("academictitle", "academic_title")
        return [getattr(lecturer, field) for lecturer in self._lecturers if hasattr(lecturer, field)]

    def retrieve(self, field):
        return self.collect(field)

    def search_by_department(self, department, offset=0, limit=None) -> (List[Lecturer], int):
        result = [lecturer for lecturer in self._lecturers
                  if department.lower() == lecturer.department.lower()]
        return result[offset:offset + limit], len(result)

    def delete_by_department(self, department) -> int:
        lecturers_to_remove = [lecturer for lecturer in self._lecturers if
                               department.lower() == lecturer.department.lower()]
        for lecturer in lecturers_to_remove:
            self._lecturers.remove(lecturer)
        return len(lecturers_to_remove)

    def search_by_academic_title_and_faculty(self,
                                             academic_title,
                                             faculty,
                                             offset=0,
                                             limit=None) -> (List[Lecturer], int):
        result = [lecturer for lecturer in self._lecturers if
                  academic_title.lower() == lecturer.academic_title.lower()
                  and faculty.lower() == lecturer.faculty.lower()]
        return result[offset:offset + limit], len(result)

    def delete_by_academic_title_and_faculty(self, academic_title, faculty) -> int:
        lecturers_to_remove = [lecturer for lecturer in self._lecturers
                               if academic_title.lower() == lecturer.academic_title.lower()
                               and faculty.lower() == lecturer.faculty.lower()]

        for lecturer in lecturers_to_remove:
            self._lecturers.remove(lecturer)
        return len(lecturers_to_remove)

    def search_by_experience(self,
                             lower_limit,
                             upper_limit,
                             offset=0,
                             limit=None) -> (List[Lecturer], int):
        result = [lecturer for lecturer in self._lecturers if
                  lower_limit <= lecturer.years_of_experience <= upper_limit]
        return result[offset:offset + limit], len(result)

    def delete_by_experience(self, lower_limit, upper_limit) -> int:
        lecturers_to_remove = [lecturer for lecturer in self._lecturers if
                               lower_limit <= lecturer.years_of_experience <= upper_limit]

        for lecturer in lecturers_to_remove:
            self._lecturers.remove(lecturer)
        return len(lecturers_to_remove)
