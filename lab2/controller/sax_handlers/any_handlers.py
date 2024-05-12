import uuid
import xml.sax

from model.absence_reason import AbsenceReason
from model.group import Group


class GroupAnyHandler(xml.sax.ContentHandler):
    def __init__(self):
        self.result = list[Group]()
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
        if name == 'group':
            new_group = Group(**self.current_group)
            new_group.id = uuid.UUID(self.current_group['id'])
            self.result.append(new_group)


class AbsenceReasonAnyHandler(xml.sax.ContentHandler):
    def __init__(self):
        self.result = list[AbsenceReason]()
        self.current_reason = {}

    def startElement(self, name, attrs):
        if name == 'absence_reason':
            self.current_reason = {
                'id': attrs.get('id'),
                'name': attrs.get('name'),
                'desc': attrs.get('desc')
            }

    def characters(self, content):
        pass

    def endElement(self, name):
        if name == 'absence_reason':
            new_reason = AbsenceReason(**self.current_reason)
            new_reason.id = uuid.UUID(self.current_reason['id'])
            self.result.append(new_reason)
