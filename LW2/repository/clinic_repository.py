from datetime import datetime

from entity.clinic import PetRecord
import xml.dom.minidom
import xml.sax


class PetRecordRepositorySQL:
    def __init__(self, connection_manager):
        self.connection_manager = connection_manager

    # def create_table(self):
    #     conn = self.connection_manager.open()
    #     if conn:
    #         create_table_sql = '''
    #         CREATE TABLE IF NOT EXISTS clinic (
    #             pet_name VARCHAR(32) NOT NULL,
    #             birth_date DATE NOT NULL,
    #             last_visit_date DATE NOT NULL,
    #             vet_full_name VARCHAR(128) NOT NULL,
    #             diagnosis VARCHAR(32) NOT NULL
    #         );
    #         '''
    #         conn.execute(create_table_sql)
    #         conn.commit()
    #         conn.close()

    def insert_clinic_record(self, pet_record):
        conn = self.connection_manager.open()
        if conn:
            insert_sql = '''
            INSERT INTO pet_record (pet_name, birth_date, last_visit_date, vet_full_name, diagnosis)
            VALUES (?, ?, ?, ?, ?);
            '''
            conn.execute(insert_sql, (
                pet_record.pet_name, pet_record.birth_date, pet_record.last_visit_date, pet_record.vet_full_name,
                pet_record.diagnosis))
            conn.commit()
            conn.close()

    def find_clinic_records(self):
        conn = self.connection_manager.open()
        if conn:
            search_sql = '''
            SELECT * FROM pet_record;'''
            cur = conn.cursor()
            cur.execute(search_sql)
            rows = cur.fetchall()
            conn.close()
            return rows


class PetRecordHandler(xml.sax.ContentHandler):
    def __init__(self):
        self.records = []
        self.current_data = ""
        self.pet_name = ""
        self.birth_date = ""
        self.last_visit_date = ""
        self.vet_full_name = ""
        self.diagnosis = ""

    def startElement(self, tag, attributes):
        self.current_data = tag

    def endElement(self, tag):
        if tag == "pet_record":
            self.pet_name = self.pet_name.strip()
            self.birth_date = self.birth_date.strip()
            self.last_visit_date = self.last_visit_date.strip()
            self.vet_full_name = self.vet_full_name.strip()
            self.diagnosis = self.diagnosis.strip()

            self.records.append(
                PetRecord(self.pet_name, datetime.strptime(self.birth_date, "%m/%d/%y").date(),
                          datetime.strptime(self.last_visit_date, "%m/%d/%y").date(), self.vet_full_name,
                          self.diagnosis))
            self.pet_name = ""
            self.birth_date = ""
            self.last_visit_date = ""
            self.vet_full_name = ""
            self.diagnosis = ""

    def characters(self, content):
        if self.current_data == "pet_name":
            self.pet_name += content
        elif self.current_data == "birth_date":
            self.birth_date += content
        elif self.current_data == "last_visit_date":
            self.last_visit_date += content
        elif self.current_data == "vet_full_name":
            self.vet_full_name += content
        elif self.current_data == "diagnosis":
            self.diagnosis += content


class PetRecordRepositoryXML:
    @staticmethod
    def write_to_xml_file(records, filename):
        try:
            doc = xml.dom.minidom.parse(filename)
            root = doc.documentElement
        except FileNotFoundError:
            doc = xml.dom.minidom.Document()
            root = doc.createElement("pet_records")
            doc.appendChild(root)

        for record in records:
            record_element = doc.createElement("pet_record")
            root.appendChild(record_element)

            PetRecordRepositoryXML.add_text_element(doc, record_element, "pet_name", record.pet_name)
            PetRecordRepositoryXML.add_text_element(doc, record_element, "birth_date",
                                                    record.birth_date.strftime("%m/%d/%y"))
            PetRecordRepositoryXML.add_text_element(doc, record_element, "last_visit_date",
                                                    record.last_visit_date.strftime("%m/%d/%y"))
            PetRecordRepositoryXML.add_text_element(doc, record_element, "vet_full_name", record.vet_full_name)
            PetRecordRepositoryXML.add_text_element(doc, record_element, "diagnosis", record.diagnosis)

        with open(filename, "w") as file:
            file.write(doc.toprettyxml(indent='', newl=''))

    @staticmethod
    def add_text_element(doc, parent, tag, text):
        element = doc.createElement(tag)
        element.appendChild(doc.createTextNode(text))
        parent.appendChild(element)

    @staticmethod
    def read_from_xml(filename):
        handler = PetRecordHandler()
        parser = xml.sax.make_parser()
        parser.setContentHandler(handler)
        parser.parse(filename)
        return handler.records


class PetRecordRepositoryList:
    def __init__(self):
        self.records = []

    def add_record(self, pet_record: PetRecord):
        self.records.append(pet_record)

    def delete_record(self, index):
        if 0 <= index < len(self.records):
            del self.records[index]
            return True
        else:
            return False

    def get_record(self, index):
        if 0 <= index < len(self.records):
            return self.records[index]
        else:
            return None


    def get_all_records(self):
        return self.records

    def find_by_diagnosis(self, partial_diagnosis):
        result_records = []
        for record in self.records:
            if partial_diagnosis.lower() in record.diagnosis.lower():
                result_records.append(record)
        return result_records

    def find_by_birth_and_name(self, birth_date, name):
        result_records = []
        for record in self.records:
            if record.pet_name == name and record.birth_date.strftime("%m/%d/%y") == birth_date.strftime("%m/%d/%y"):
                result_records.append(record)
        return result_records

    def find_by_last_visit_and_vet(self, last_visit_date, vet_full_name):
        result_records = []
        for record in self.records:
            if record.last_visit_date.strftime("%m/%d/%y") == last_visit_date.strftime(
                    "%m/%d/%y") and record.vet_full_name == vet_full_name:
                result_records.append(record)
        return result_records

    def delete_record_by_name_and_birth(self, name, birth_date):
        deleted_count = 0
        records_copy = self.records[:]
        for record in records_copy:
            if record.pet_name == name and record.birth_date.strftime("%m/%d/%y") == birth_date.strftime("%m/%d/%y"):
                self.records.remove(record)
                deleted_count += 1
        return deleted_count

    def delete_by_last_visit_and_vet(self, last_visit_date, vet_full_name):
        deleted_count = 0
        records_copy = self.records[:]
        for record in records_copy:
            if record.last_visit_date.strftime("%m/%d/%y") == last_visit_date.strftime(
                    "%m/%d/%y") and record.vet_full_name == vet_full_name:
                self.records.remove(record)
                deleted_count += 1
        return deleted_count

    def delete_by_diagnosis(self, partial_diagnosis):
        deleted_count = 0
        records_copy = self.records[:]
        for record in records_copy:
            if partial_diagnosis.lower() in record.diagnosis.lower():
                self.records.remove(record)
                deleted_count += 1
        return deleted_count
