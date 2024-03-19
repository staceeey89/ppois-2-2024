import uuid
import xml.sax

from controller.parsing_exception import FinishedParsing
from controller.search_criteria import SearchCriteria
from model.absence import Absence
from model.group import Group
from model.student import Student


class StudentByCriteriaHandler(xml.sax.ContentHandler):
    def __init__(self, search_criteria: SearchCriteria):
        self.result = list()
        self.search_criteria = search_criteria
        self.students_to_skip = (search_criteria.page_number - 1) * search_criteria.page_size
        self.current_student = {}

    def startElement(self, name, attrs):
        if name == 'student':
            self.current_student = {
                'id': attrs.get('id'),
                'name': attrs.get('name'),
                'group_id': attrs.get('group_id')
            }

    def characters(self, content):
        pass

    def endElement(self, name):
        if name == 'student':
            if self.search_criteria.name is not None and self.search_criteria.name != self.current_student['name']:
                return
            if (self.search_criteria.group is not None and self.search_criteria.group.id.__str__()
                    != self.current_student['group_id']):
                return

            if self.students_to_skip > 0:
                self.students_to_skip -= 1
                return

            new_student = self.current_student
            new_student['id'] = uuid.UUID(self.current_student['id'])
            self.result.append(new_student)

            if self.search_criteria.page_size != 0 and len(self.result) >= self.search_criteria.page_size:
                raise FinishedParsing()


class AbsencesByCriteriaHandler(xml.sax.ContentHandler):
    def __init__(self, student_id: uuid.UUID | None, page_number: int = 1, page_size: int = 10):
        self.result = list()
        self.student_id = student_id
        self.page_size = page_size
        self.absences_to_skip = (page_number - 1) * page_size
        self.current_absence = {}

    def startElement(self, name, attrs):
        if name == 'absence':
            self.current_absence = {
                'id': attrs.get('id'),
                'date': attrs.get('date'),
                'student_id': attrs.get('student_id'),
                'reason_id': attrs.get('reason_id')
            }

    def characters(self, content):
        pass

    def endElement(self, name):
        if name == 'absence':
            if self.student_id is not None and self.student_id.__str__() != self.current_absence['student_id']:
                return

            if self.absences_to_skip > 0:
                self.absences_to_skip -= 1
                return

            new_absence = self.current_absence
            new_absence['id'] = uuid.UUID(self.current_absence['id'])
            self.result.append(new_absence)

            if self.page_size != 0 and len(self.result) >= self.page_size:
                raise FinishedParsing()


class AbsencesCountByStudentIdHandler(xml.sax.ContentHandler):
    def __init__(self, student_id: uuid.UUID):
        self.result = 0
        self.student_id = student_id
        self.current_absence = {}

    def startElement(self, name, attrs):
        if name == 'absence':
            self.current_absence = {
                'student_id': attrs.get('student_id'),
            }

    def characters(self, content):
        pass

    def endElement(self, name):
        if name == 'absence':
            if self.student_id is None or self.student_id.__str__() == self.current_absence['student_id']:
                self.result += 1
