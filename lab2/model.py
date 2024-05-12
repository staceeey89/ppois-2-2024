import sqlite3
import io
from typing import List, Any
from dataclasses import dataclass
from abc import ABC, abstractmethod
import xml.sax
from xml.dom.minidom import Document


@dataclass
class Record:
    full_name: str
    father_name: str
    father_salary: int
    mother_name: str
    mother_salary: int
    brothers_amount: int
    sisters_amount: int


class Model(ABC):
    @abstractmethod
    def __init__(self, database_path: str):
        pass

    @abstractmethod
    def __del__(self):
        pass

    @abstractmethod
    def get_items_size(self) -> int:
        pass

    @abstractmethod
    def get_items_size_condition(self, condition: str) -> int:
        pass

    @abstractmethod
    def add_item(
        self,
        full_name: str,
        father_name: str,
        father_salary: int,
        mother_name: str,
        mother_salary: int,
        brothers_amount: int,
        sisters_amount: int,
    ):
        pass

    @abstractmethod
    def get_items(self, offset: int, limit: int) -> List[Any]:
        pass

    @abstractmethod
    def get_all_items(self) -> List[Record]:
        pass

    @abstractmethod
    def get_all_items_condition(self, condition: str) -> List[Record]:
        pass

    @abstractmethod
    def get_items_condition(self, condition: str, offset: int, limit: int) -> List[Any]:
        pass

    @abstractmethod
    def remove_items_condition(self, condition: str) -> int:
        pass

    @abstractmethod
    def save(self):
        pass


class XMLHandler(xml.sax.ContentHandler):
    def __init__(self):
        xml.sax.ContentHandler.__init__(self)
        self.items = []
        self.current_element = ""
        self.item = {}

    def startElement(self, name, attrs):
        if name == "student":
            self.item = {}
            self.current_element = "student"
        else:
            self.current_element = name

    def endElement(self, name):
        if name == "student":
            self.items.append(self.item)

    def characters(self, content):
        if self.current_element != "":
            self.item[self.current_element] = content.strip()
            self.current_element = ""


class XMLModel(Model):
    def __init__(self, xml_path: str):
        handler = XMLHandler()
        parser = xml.sax.make_parser()
        parser.setContentHandler(handler)
        parser.parse(xml_path)
        self.records: List[Record] = []
        self.records: List[Record] = [
            Record(*list(element.values())[1:]) for element in handler.items
        ]
        self.prev_condition: str = "None"
        self.cond_records: List[Record] = []
        self.file_path = xml_path

    def __del__(self):
        pass

    def get_items_size(self) -> int:
        return len(self.records)

    def update_condition_items(self, condition):
        if condition[0] == "full_name":
            if condition[1] == "first":
                place = 0
            elif condition[1] == "middle":
                place = 1
            else:
                place = -1

            if condition[2] == "student":
                self.cond_records = [
                    x
                    for x in self.records
                    if x.full_name.split()[place] == condition[3]
                ]
            elif condition[2] == "father":
                self.cond_records = [
                    x
                    for x in self.records
                    if x.father_name.split()[place] == condition[3]
                ]
            elif condition[2] == "mother":
                self.cond_records = [
                    x
                    for x in self.records
                    if x.mother_name.split()[place] == condition[3]
                ]

        elif condition[0] == "father_salary":
            if condition[1][0] != "" and condition[1][1] != "":
                max = int(condition[1][0])
                min = int(condition[1][1])
                self.cond_records = [
                    x
                    for x in self.records
                    if max >= int(x.father_salary) >= min
                ]
            elif condition[1][0] != "":
                max = int(condition[1][0])
                self.cond_records = [
                    x for x in self.records if int(x.father_salary) <= max
                ]
            else:
                min = int(condition[1][1])
                self.cond_records = [
                    x for x in self.records if int(x.father_salary) >= min
                ]

        elif condition[0] == "mother_salary":
            if condition[1][0] != "" and condition[1][1] != "":
                max = int(condition[1][0])
                min = int(condition[1][1])
                self.cond_records = [
                    x
                    for x in self.records
                    if max >= int(x.mother_salary) >= min
                ]
            elif condition[1][0] != "":
                max = int(condition[1][0])
                self.cond_records = [
                    x for x in self.records if int(x.mother_salary) <= max
                ]
            else:
                min = int(condition[1][1])
                self.cond_records = [
                    x for x in self.records if int(x.mother_salary) >= min
                ]

        elif condition[0] == "brothers_amount":
            self.cond_records = [
                x for x in self.records if int(x.brothers_amount) == int(condition[1])
            ]

        elif condition[0] == "sisters_amount":
            self.cond_records = [
                x for x in self.records if int(x.sisters_amount) == int(condition[1])
            ]

    def get_items_size_condition(self, condition: str) -> int:
        if condition == self.prev_condition:
            return len(self.cond_records)

        self.update_condition_items(condition)
        return len(self.cond_records)

    def add_item(
        self,
        full_name: str,
        father_name: str,
        father_salary: int,
        mother_name: str,
        mother_salary: int,
        brothers_amount: int,
        sisters_amount: int,
    ):
        self.records.append(
            Record(
                full_name,
                father_name,
                father_salary,
                mother_name,
                mother_salary,
                brothers_amount,
                sisters_amount,
            )
        )

    def get_items(self, offset: int, limit: int) -> List[Any]:
        return self.records[offset : limit + offset]

    def get_all_items(self) -> List[Record]:
        return self.records

    def get_all_items_condition(self, condition: str) -> List[Record]:
        if condition == self.prev_condition:
            return self.cond_records

        self.update_condition_items(condition)
        return self.cond_records

    def get_items_condition(self, condition: str, offset: int, limit: int) -> List[Any]:
        if condition == self.prev_condition:
            return self.cond_records[offset : limit + offset]

        self.update_condition_items(condition)
        return self.cond_records[offset : limit + offset]

    def remove_items_condition(self, condition: str) -> int:
        if condition != self.prev_condition:
            self.update_condition_items(condition)
        start = len(self.records)
        self.records = [x for x in self.records if x not in self.cond_records]
        end = len(self.records)
        return start - end

    def save(self):
        doc = Document()
        root = doc.createElement("students")
        doc.appendChild(root)

        for record in self.records:
            item_element = doc.createElement("student")
            sub_element = doc.createElement("full_name")
            sub_element.appendChild(doc.createTextNode(record.full_name))
            item_element.appendChild(sub_element)

            sub_element = doc.createElement("father_name")
            sub_element.appendChild(doc.createTextNode(record.father_name))
            item_element.appendChild(sub_element)

            sub_element = doc.createElement("father_salary")
            sub_element.appendChild(doc.createTextNode(str(record.father_salary)))
            item_element.appendChild(sub_element)

            sub_element = doc.createElement("mother_name")
            sub_element.appendChild(doc.createTextNode(record.mother_name))
            item_element.appendChild(sub_element)

            sub_element = doc.createElement("mother_salary")
            sub_element.appendChild(doc.createTextNode(str(record.mother_salary)))
            item_element.appendChild(sub_element)

            sub_element = doc.createElement("brothers_amount")
            sub_element.appendChild(doc.createTextNode(str(record.brothers_amount)))
            item_element.appendChild(sub_element)

            sub_element = doc.createElement("sisters_amount")
            sub_element.appendChild(doc.createTextNode(str(record.sisters_amount)))
            item_element.appendChild(sub_element)

            root.appendChild(item_element)

        with open(self.file_path, "w") as f:
            f.write(doc.toprettyxml(indent="  "))


class SQLModel(Model):
    def __init__(self, database_path: str):
        self._connection = sqlite3.connect(database_path)
        self._cursor = self._connection.cursor()
        self._cursor.execute(
            """
                CREATE TABLE IF NOT EXISTS student (
                student_full_name TEXT,
                father_full_name TEXT,
                father_salary INTEGER,
                mother_full_name TEXT,
                mother_salary INTEGER,
                brothers_amount INTEGER,
                sisters_amount INTEGER
                )
            """
        )

    def __del__(self):
        self._connection.close()

    def get_items_size(self) -> int:
        self._cursor.execute("SELECT COUNT(*) FROM student")
        return self._cursor.fetchone()[0]

    def get_items_size_condition(self, condition: str) -> int:
        execute_command = f"SELECT COUNT(*) FROM student {condition}"
        self._cursor.execute(execute_command)
        return self._cursor.fetchone()[0]

    def add_item(
        self,
        full_name: str,
        father_name: str,
        father_salary: int,
        mother_name: str,
        mother_salary: int,
        brothers_amount: int,
        sisters_amount: int,
    ):
        self._cursor.execute(
            """ INSERT INTO student (student_full_name, father_full_name,
                father_salary, mother_full_name, mother_salary,
                brothers_amount, sisters_amount)
                VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (
                full_name,
                father_name,
                father_salary,
                mother_name,
                mother_salary,
                brothers_amount,
                sisters_amount,
            ),
        )

    def get_items(self, offset: int, limit: int) -> List[Any]:
        self._cursor.execute(
            """
            SELECT * FROM student LIMIT (?) OFFSET (?)
            """,
            (limit, offset),
        )
        query = self._cursor.fetchall()
        return [Record(*element) for element in query]

    def get_all_items(self):
        self._cursor.execute(
            """
        SELECT * FROM student
        """
        )
        query = self._cursor.fetchall()
        return [Record(*element) for element in query]

    def get_all_items_condition(self, condition: str):
        execute_command = "SELECT * FROM student " + condition
        self._cursor.execute(execute_command)
        query = self._cursor.fetchall()
        return [Record(*element) for element in query]

    def get_items_condition(self, condition: str, offset: int, limit: int) -> List[Any]:
        execute_command = "SELECT * FROM student " + condition + " LIMIT (?) OFFSET (?)"
        self._cursor.execute(execute_command, (limit, offset))
        query = self._cursor.fetchall()
        return [Record(*element) for element in query]

    def remove_items_condition(self, condition: str) -> int:
        self._cursor.execute("SELECT COUNT(*) FROM student")
        start_items = int(self._cursor.fetchone()[0])
        execute_command = "DELETE FROM student " + condition
        self._cursor.execute(execute_command)
        self._cursor.execute("SELECT COUNT(*) FROM student")
        end_items = int(self._cursor.fetchone()[0])
        return start_items - end_items

    def save(self):
        self._connection.commit()

    def save_as_commits(self, pathname):
        with io.open(pathname, "w") as file:
            for line in self._connection.iterdump():
                file.write("%s\n" % line)
