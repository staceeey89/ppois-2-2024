import uuid
import xml.sax
from datetime import datetime

from controller import search_criteria
from controller.check_criteria import check_search_criteria
from controller.repository import AbstractRepository
from controller.sax_handlers.any_handlers import GroupAnyHandler, AbsenceReasonAnyHandler
from controller.sax_handlers.by_criteria_handlers import StudentByCriteriaHandler, AbsencesByCriteriaHandler, \
    AbsencesCountByStudentIdHandler
from controller.sax_handlers.by_id_handlers import AbsenceReasonByIdHandler, GroupByIdHandler, StudentByIdHandler
from controller.search_criteria import SearchCriteria
from model.absence import Absence
from model.absence_reason import AbsenceReason
from model.group import Group
from model.student import Student

from xml.dom.minidom import parse
from xml.dom.minidom import Document


class FileRepository(AbstractRepository):
    def __init__(self, filepath: str):
        self.file_path = filepath

    def initialize_file(self):
        doc = xml.dom.minidom.getDOMImplementation().createDocument(None, 'LW2', None)

        doc.documentElement.appendChild(doc.createElement('groups'))
        doc.documentElement.appendChild(doc.createElement('students'))
        doc.documentElement.appendChild(doc.createElement('absences'))
        doc.documentElement.appendChild(doc.createElement('absence_reasons'))

        self._save_modified_document(doc)

        self.add_group(221701)
        self.add_group(221702)
        self.add_group(221703)

        self.add_absence_reason('Sick', 'Person has legit sick list')
        self.add_absence_reason('Other', 'Nobody knows')
        self.add_absence_reason('Unjust cause', 'Just skip these classes, man')

    def _parse_existing_document(self) -> Document:
        doc = parse(self.file_path)
        return doc

    def _save_modified_document(self, doc):
        with open(self.file_path, 'w') as file:
            file.write(doc.toxml())

    def delete_students(self, search_criteria: SearchCriteria) -> int:
        students_to_delete = self.get_students(search_criteria)

        for student in students_to_delete:
            self.delete_student(student.id)

        return len(students_to_delete)

    def delete_student(self, student_id: uuid.UUID):
        absences = self.get_absences(student_id, 1, 0)
        for absence in absences:
            self.delete_absence(absence.id)

        self._delete_by_id('student', student_id)

    def get_students(self, search_criteria: SearchCriteria) -> list[Student]:
        handler = StudentByCriteriaHandler(search_criteria)
        try:
            xml.sax.parse(self.file_path, handler)
        finally:
            unfiltered_students = handler.result

            result = list[Student]()
            for s in unfiltered_students:
                group = self.get_group(s['group_id'])
                new_stud = Student(s['id'], s['name'], group, 0, 0, 0, 0)
                self._count_student_absences(new_stud)
                if check_search_criteria(new_stud, search_criteria):
                    result.append(new_stud)

            return result

    def _count_student_absences(self, student: Student):
        absences = self.get_absences(student.id, 1, 0)

        student.absences_total = len(absences)
        student.absences_sick = 0
        student.absences_other = 0
        student.absences_unjust = 0

        for absence in absences:
            match absence.reason.name:
                case 'Sick': student.absences_sick += 1
                case 'Other': student.absences_other += 1
                case 'Unjust cause': student.absences_unjust += 1

    def get_student(self, student_id: uuid.UUID) -> Student:
        handler = StudentByIdHandler(student_id)
        try:
            xml.sax.parse(self.file_path, handler)
        finally:
            result = handler.result
            # warning: this doesn't get actual group since we don't need it
            group = None  # self.get_group(result['group_id'])

            # warning: this doesn't count actual absences since we don't need it
            return Student(result['id'], result['name'], group, 0, 0, 0, 0)

    def add_student(self, name: str, group_id: uuid.UUID):
        doc = self._parse_existing_document()

        student_element = doc.createElement('student')
        student_element.attributes['id'] = uuid.uuid4().__str__()
        student_element.attributes['name'] = str(name)
        student_element.attributes['group_id'] = group_id.__str__()

        items_element = doc.getElementsByTagName('students')[0]
        items_element.appendChild(student_element)

        self._save_modified_document(doc)

    def add_group(self, group_number: int) -> None:
        doc = self._parse_existing_document()

        group_element = doc.createElement('group')
        group_element.attributes['id'] = uuid.uuid4().__str__()
        group_element.attributes['number'] = str(group_number)

        items_element = doc.getElementsByTagName('groups')[0]
        items_element.appendChild(group_element)

        self._save_modified_document(doc)

    def delete_group(self, group_id: uuid.UUID) -> None:
        self._delete_by_id('group', group_id)

    def get_groups(self) -> list[Group]:
        handler = GroupAnyHandler()
        xml.sax.parse(self.file_path, handler)
        return handler.result

    def get_group(self, group_id: uuid.UUID) -> Group:
        handler = GroupByIdHandler(group_id)
        try:
            xml.sax.parse(self.file_path, handler)
        finally:
            return handler.result

    def add_absence_reason(self, reason_name: str, reason_desc: str | None) -> None:
        doc = self._parse_existing_document()

        reason_element = doc.createElement('absence_reason')
        reason_element.attributes['id'] = uuid.uuid4().__str__()
        reason_element.attributes['name'] = reason_name
        reason_element.attributes['desc'] = reason_desc

        reasons_element = doc.getElementsByTagName('absence_reasons')[0]
        reasons_element.appendChild(reason_element)

        self._save_modified_document(doc)

    def delete_absence_reason(self, reason_id: uuid.UUID) -> None:
        self._delete_by_id('absence_reason', reason_id)

    def get_absence_reasons(self) -> list[AbsenceReason]:
        handler = AbsenceReasonAnyHandler()
        xml.sax.parse(self.file_path, handler)
        return handler.result

    def get_absence_reason(self, reason_id: uuid.UUID) -> AbsenceReason:
        handler = AbsenceReasonByIdHandler(reason_id)
        try:
            xml.sax.parse(self.file_path, handler)
        finally:
            return handler.result

    def get_absences(self, student_id: uuid.UUID | None, page_number: int = 1, page_size: int = 10) -> list[Absence]:
        handler = AbsencesByCriteriaHandler(student_id, page_number, page_size)
        try:
            xml.sax.parse(self.file_path, handler)
        finally:
            temp_absences = handler.result

            result = list[Absence]()
            for a in temp_absences:
                student = self.get_student(a['student_id'])
                reason = self.get_absence_reason(a['reason_id'])
                absence = Absence(a['id'], datetime.fromisoformat(a['date']).date(), student, reason)
                result.append(absence)

            return result

    def delete_absence(self, id: uuid.UUID) -> None:
        self._delete_by_id('absence', id)

    def add_absence(self, student_id: uuid.UUID, reason_id: uuid.UUID) -> None:
        doc = self._parse_existing_document()

        absence_element = doc.createElement('absence')
        absence_element.attributes['id'] = uuid.uuid4().__str__()
        absence_element.attributes['student_id'] = student_id.__str__()
        absence_element.attributes['reason_id'] = reason_id.__str__()
        absence_element.attributes['date'] = datetime.today().date().isoformat()

        reasons_element = doc.getElementsByTagName('absences')[0]
        reasons_element.appendChild(absence_element)
        self._save_modified_document(doc)

    def _delete_by_id(self, tag_name: str, id: uuid.UUID) -> None:
        doc = self._parse_existing_document()
        items = doc.getElementsByTagName(tag_name)
        for item in items:
            if item.getAttribute('id') == id.__str__():
                parent = item.parentNode
                parent.removeChild(item)
                self._save_modified_document(doc)
                return

    def count_students_amount(self, search_criteria: SearchCriteria) -> int:
        old_page_size = search_criteria.page_size

        search_criteria.page_size = 0
        students = self.get_students(search_criteria)

        search_criteria.page_size = old_page_size
        return len(students)

    def count_absences_amount(self, student_id: uuid.UUID | None) -> int:
        handler = AbsencesCountByStudentIdHandler(student_id)
        xml.sax.parse(self.file_path, handler)
        return handler.result
