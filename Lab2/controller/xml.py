import xml.etree.ElementTree as ET
import xml.dom.minidom
from datetime import datetime


class parser():
    def __init__(self, filename='xml_file1.xml'):
        self.root = None
        self.tree = None
        self.filename = filename

    def from_xml(self):
        self.tree = ET.parse(self.filename)
        self.root = self.tree.getroot()
        data = []
        for medical_card in self.root.findall('medical_card'):
            patient_surname_elem = medical_card.find('patient_surname')
            patient_surname = patient_surname_elem.text if patient_surname_elem is not None else ""

            patient_name_elem = medical_card.find('patient_name')
            patient_name = patient_name_elem.text if patient_name_elem is not None else ""

            birthday_date_elem = medical_card.find('birthday_date')
            birthday_date = birthday_date_elem.text if birthday_date_elem is not None else ""

            registration_address_elem = medical_card.find('registration_address')
            registration_address = registration_address_elem.text if registration_address_elem is not None else ""

            appointment_date_elem = medical_card.find('appointment_date')
            appointment_date = appointment_date_elem.text if appointment_date_elem is not None else ""

            doctor_surname_elem = medical_card.find('doctor_surname')
            doctor_surname = doctor_surname_elem.text if doctor_surname_elem is not None else ""

            doctor_name_elem = medical_card.find('doctor_name')
            doctor_name = doctor_name_elem.text if doctor_name_elem is not None else ""

            doctor_statement_elem = medical_card.find('doctor_statement')
            doctor_statement = doctor_statement_elem.text if doctor_statement_elem is not None else ""

            data.append((patient_surname, patient_name, registration_address, birthday_date,
                         appointment_date, doctor_surname, doctor_name, doctor_statement))
        return data

    '''def to_xml(self, data):
        self.root = ET.Element("catalog")
        j = 1
        for record in data:
            medical_card = ET.SubElement(self.root, "medical_card")
            medical_card.set("id", str(j))
            j += 1
            ET.SubElement(medical_card, "patient_surname").text = record[0]
            ET.SubElement(medical_card, "patient_name").text = record[1]
            ET.SubElement(medical_card, "registration_address").text = record[2]
            ET.SubElement(medical_card, "birthday_date").text = record[3].strftime('%Y-%m-%d')
            ET.SubElement(medical_card, "appointment_date").text = record[4].strftime('%Y-%m-%d')
            ET.SubElement(medical_card, "doctor_surname").text = record[5]
            ET.SubElement(medical_card, "doctor_name").text = record[6]
            ET.SubElement(medical_card, "doctor_statement").text = record[7]

        self.tree = ET.ElementTree(self.root)
        self.tree.write(self.filename, encoding='utf-8', xml_declaration=True)'''

    def to_xml(self, data):
        self.root = ET.Element("catalog")
        j = 1
        for record in data:
            medical_card = ET.SubElement(self.root, "medical_card")
            medical_card.set("id", str(j))
            j += 1
            ET.SubElement(medical_card, "patient_surname").text = record[0]
            ET.SubElement(medical_card, "patient_name").text = record[1]
            ET.SubElement(medical_card, "registration_address").text = record[2]
            ET.SubElement(medical_card, "birthday_date").text = record[3].strftime('%Y-%m-%d')
            ET.SubElement(medical_card, "appointment_date").text = record[4].strftime('%Y-%m-%d')
            ET.SubElement(medical_card, "doctor_surname").text = record[5]
            ET.SubElement(medical_card, "doctor_name").text = record[6]
            ET.SubElement(medical_card, "doctor_statement").text = record[7]

        xml_string = ET.tostring(self.root, encoding='utf-8')
        dom = xml.dom.minidom.parseString(xml_string)
        formatted_xml = dom.toprettyxml(indent="  ")

        with open(self.filename, "w", encoding='utf-8') as xml_file:
            xml_file.write(formatted_xml)
