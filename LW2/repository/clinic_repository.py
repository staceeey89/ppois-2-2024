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
            # Очищаем данные от лишних символов
            self.pet_name = self.pet_name.strip()
            self.birth_date = self.birth_date.strip()
            self.last_visit_date = self.last_visit_date.strip()
            self.vet_full_name = self.vet_full_name.strip()
            self.diagnosis = self.diagnosis.strip()

            # Добавляем запись в список
            self.records.append(
                PetRecord(self.pet_name, self.birth_date, self.last_visit_date, self.vet_full_name, self.diagnosis))
            # Сбрасываем данные
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
            # Читаем существующий XML-документ
            doc = xml.dom.minidom.parse(filename)
            root = doc.documentElement
        except FileNotFoundError:
            # Если файл не найден, создаем новый XML-документ
            doc = xml.dom.minidom.Document()
            root = doc.createElement("pet_records")
            doc.appendChild(root)

        # Добавляем новые записи в XML-документ
        for record in records:
            record_element = doc.createElement("pet_record")
            root.appendChild(record_element)

            # Добавляем атрибуты записи
            PetRecordRepositoryXML.add_text_element(doc, record_element, "pet_name", record.pet_name)
            PetRecordRepositoryXML.add_text_element(doc, record_element, "birth_date", str(record.birth_date))
            PetRecordRepositoryXML.add_text_element(doc, record_element, "last_visit_date", str(record.last_visit_date))
            PetRecordRepositoryXML.add_text_element(doc, record_element, "vet_full_name", record.vet_full_name)
            PetRecordRepositoryXML.add_text_element(doc, record_element, "diagnosis", record.diagnosis)

        # Записываем XML-документ в файл
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

        # pet_record_1 = PetRecord("Pet_1", "2022-01-01", "2022-01-10", "Dr. Vet_1", "Diagnosis_1")
        # pet_record_2 = PetRecord("Pet_2", "2022-01-01", "2022-01-10", "Dr. Vet_2", "Diagnosis_2")
        # pet_record_3 = PetRecord("Pet_3", "2022-01-01", "2022-01-10", "Dr. Vet_3", "Diagnosis_3")
        # pet_record_4 = PetRecord("Pet_4", "2022-01-01", "2022-01-10", "Dr. Vet_4", "Diagnosis_4")
        # pet_record_5 = PetRecord("Pet_5", "2022-01-01", "2022-01-10", "Dr. Vet_5", "Diagnosis_5")
        # pet_record_6 = PetRecord("Pet_6", "2022-01-01", "2022-01-10", "Dr. Vet_6", "Diagnosis_6")
        # pet_record_7 = PetRecord("Pet_7", "2022-01-01", "2022-01-10", "Dr. Vet_7", "Diagnosis_7")
        # pet_record_8 = PetRecord("Pet_8", "2022-01-01", "2022-01-10", "Dr. Vet_8", "Diagnosis_8")
        # pet_record_9 = PetRecord("Pet_9", "2022-01-01", "2022-01-10", "Dr. Vet_9", "Diagnosis_9")
        # pet_record_10 = PetRecord("Pet_10", "2022-01-01", "2022-01-10", "Dr. Vet_10", "Diagnosis_10")
        #
        # self.records.extend([pet_record_1, pet_record_2, pet_record_3, pet_record_4, pet_record_5,
        #                      pet_record_6, pet_record_7, pet_record_8, pet_record_9, pet_record_10])

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

    def search_records(self, criteria):
        results = []
        for record in self.records:
            if criteria.lower() in record.pet_name.lower() or \
                    criteria.lower() in record.vet_full_name.lower() or \
                    criteria.lower() in record.diagnosis.lower():
                results.append(record)
        return results

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
            if record.pet_name == name and record.birth_date == birth_date:
                result_records.append(record)
        return result_records

    def find_by_last_visit_and_vet(self, last_visit_date, vet_full_name):
        result_records = []
        for record in self.records:
            if record.last_visit_date == last_visit_date and record.vet_full_name == vet_full_name:
                result_records.append(record)
        return result_records

    def delete_record_by_name_and_birth(self, name, birth_date):
        deleted_count = 0
        records_copy = self.records[:]
        for record in records_copy:
            if record.pet_name == name and record.birth_date == birth_date:
                self.records.remove(record)
                deleted_count += 1
        return deleted_count

    def delete_by_last_visit_and_vet(self, last_visit_date, vet_full_name):
        deleted_count = 0
        records_copy = self.records[:]
        for record in records_copy:
            if record.last_visit_date == last_visit_date and record.vet_full_name == vet_full_name:
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
