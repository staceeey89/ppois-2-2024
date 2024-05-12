import xml.dom.minidom
from typing import List
from xml.sax import ContentHandler

from model import Lecturer
from empty_list_storage import EmptyListStorage


class LecturerHandler(ContentHandler):
    def __init__(self):
        self.current_tag = ""
        self.current_lecturer = None
        self.lecturers = []

    def startElement(self, tag, attributes):
        self.current_tag = tag
        if tag == "lecturer":
            self.current_lecturer = {'id': attributes['id']}

    def endElement(self, tag):
        if tag == "lecturer":
            self.lecturers.append(self.current_lecturer)
            self.current_lecturer = None
        self.current_tag = ""

    def characters(self, content):
        if self.current_lecturer is not None:
            self.current_lecturer[self.current_tag] = content


class XmlStorage(EmptyListStorage):
    def __init__(self, file):
        super().__init__()
        self.file: str = file
        self._lecturers: List[Lecturer] = self.__load_lecturers_from_xml()

    def __load_lecturers_from_xml(self):
        handler = LecturerHandler()
        parser = xml.sax.make_parser()
        parser.setContentHandler(handler)
        parser.parse(self.file)

        lecturer_list = []
        for lecturer_data in handler.lecturers:
            lecturer = Lecturer(lecturer_data['id'], lecturer_data['faculty'], lecturer_data['department'],
                                lecturer_data['full_name'], lecturer_data['academic_title'],
                                lecturer_data['academic_degree'], int(lecturer_data['years_of_experience']))
            lecturer_list.append(lecturer)

        return lecturer_list

    def __save_lecturers_to_xml(self):
        doc = xml.dom.minidom.Document()
        root = doc.createElement("lecturers")
        doc.appendChild(root)
        for lecturer in self._lecturers:
            lecturer_element = doc.createElement("lecturer")
            for key, value in lecturer.__dict__.items():
                if key != 'id':
                    element = doc.createElement(key)
                    element.appendChild(doc.createTextNode(str(value)))
                    lecturer_element.appendChild(element)
            lecturer_element.setAttribute("id", str(lecturer.__dict__['id']))
            root.appendChild(lecturer_element)
        with open(self.file, "w") as f:
            f.write(doc.toprettyxml(indent="  "))

    def save(self):
        self.__save_lecturers_to_xml()
