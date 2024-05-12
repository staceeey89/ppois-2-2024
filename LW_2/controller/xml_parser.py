import xml.etree.ElementTree as ET


class XMLParser:
    @staticmethod
    def parse(xml_file):
        students = []
        tree = ET.parse(xml_file)
        root = tree.getroot()
        for student_elem in root.findall('student'):
            student = {}
            student['id'] = student_elem.find('id').text
            student['fio'] = student_elem.find('fio').text
            student['group'] = student_elem.find('group').text
            student['sick_absent'] = student_elem.find('sick_absent').text
            student['other_absent'] = student_elem.find('other_absent').text
            student['unexcused_absent'] = student_elem.find('unexcused_absent').text
            students.append(student)
        return students


class XMLWriter:
    @staticmethod
    def save(file_path, students_data):
        root = ET.Element("students")
        for student in students_data:
            student_elem = ET.SubElement(root, "student")
            id_elem = ET.SubElement(student_elem, "id")
            id_elem.text = str(student['id'])
            fio_elem = ET.SubElement(student_elem, "fio")
            fio_elem.text = student['fio']
            group_elem = ET.SubElement(student_elem, "group")
            group_elem.text = student['group']
            sick_absent_elem = ET.SubElement(student_elem, "sick_absent")
            sick_absent_elem.text = str(student['sick_absent'])
            other_absent_elem = ET.SubElement(student_elem, "other_absent")
            other_absent_elem.text = str(student['other_absent'])
            unexcused_absent_elem = ET.SubElement(student_elem, "unexcused_absent")
            unexcused_absent_elem.text = str(student['unexcused_absent'])

        tree = ET.ElementTree(root)
        tree.write(file_path, encoding='utf-8', xml_declaration=True)
