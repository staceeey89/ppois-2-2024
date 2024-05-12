import uuid
import xml.sax

from controller.parsing_exception import FinishedParsing
from model.absence_reason import AbsenceReason
from model.group import Group
from model.student import Student


class AbsenceReasonByIdHandler(xml.sax.ContentHandler):
    def __init__(self, target_id: uuid.UUID):
        self.result = None
        self.target_id = target_id
        self.current_absence_reason = {}

    def startElement(self, name, attrs):
        if name == 'absence_reason':
            self.current_absence_reason = {
                'id': attrs.get('id'),
                'name': attrs.get('name'),
                'desc': attrs.get('desc'),
            }

    def characters(self, content):
        pass

    def endElement(self, name):
        if name == 'absence_reason' and self.current_absence_reason['id'] == self.target_id.__str__():
            self.result = AbsenceReason(**self.current_absence_reason)
            self.result.id = uuid.UUID(self.current_absence_reason['id'])
            raise FinishedParsing()


class GroupByIdHandler(xml.sax.ContentHandler):
    def __init__(self, target_id: uuid.UUID):
        self.result = None
        self.target_id = target_id
        self.current_group = {}

    def startElement(self, name, attrs):
        if name == 'group':
            self.current_group = {
                'id': attrs.get('id'),
                'number': attrs.get('number')
            }

    def characters(self, content):
        pass

    def endElement(self, name):
        if name == 'group' and self.current_group['id'] == self.target_id.__str__():
            self.result = Group(**self.current_group)
            self.result.id = uuid.UUID(self.current_group['id'])
            raise FinishedParsing()


class StudentByIdHandler(xml.sax.ContentHandler):
    def __init__(self, target_id: uuid.UUID):
        self.result = {}
        self.target_id = target_id
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
        if name == 'student' and self.current_student['id'] == self.target_id.__str__():
            self.result = self.current_student
            self.result['id'] = uuid.UUID(self.current_student['id'])
            raise FinishedParsing()
