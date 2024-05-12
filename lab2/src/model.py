import sqlite3
import xml.sax
import xml.etree.ElementTree as ET
import xml.dom.minidom
from information_board import InformationBoard


class Model():
    def __init__(self, file_path,type):
        if type == "db":
            self.connect = sqlite3.connect(file_path)
        else:
            self.file_path = file_path

    def close_connect(self,type):
        if type == "db":
            self.connect.close()
    def get_info_array(self):
        cursor = self.connect.cursor()
        cursor.execute("SELECT * FROM information_board")
        rows = cursor.fetchall()
        cursor.close()
        return rows

    def create_information_board(self):
        cursor = self.connect.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS information_board (
                        /*id INTEGER PRIMARY KEY,*/
                        train_number INTEGER NOT NULL,
                        departure_station TEXT NOT NULL,
                        departure_time TEXT NOT NULL,
                        arrival_station TEXT NOT NULL,
                        arrival_time TEXT NOT NULL,
                        travel_time TEXT NOT NULL)""")

    def add_to_information_board(self, info: InformationBoard):
        cursor = self.connect.cursor()
        cursor.execute("""INSERT INTO information_board (train_number, departure_station, arrival_station, departure_time, arrival_time, travel_time) \
                                            VALUES (?, ?, ?, ?, ?, ?)""",
                       (info._train_number, info._departure_station, info._arrival_station, info._departure_time,
                        info._arrival_time, info._travel_time))
        self.connect.commit()
        cursor.close()

    def search_from_database(self, conditions, values):
        query = "SELECT * FROM information_board "
        cursor = self.connect.cursor()
        cursor.execute(f"""{query} {conditions}""", values)
        info = cursor.fetchall()
        cursor.close()
        return info

    def delete_from_database(self,condition):
        query = "DELETE FROM information_board WHERE "
        query += condition
        cursor = self.connect.cursor()
        cursor.execute(f"""{query}""")
        deleted_rows = cursor.rowcount
        self.connect.commit()
        cursor.close()
        return deleted_rows

    def create_xml_file(self):
        doc = xml.dom.minidom.Document()
        root = doc.createElement("trains")
        doc.appendChild(root)
        with open(self.file_path, "w") as file:
            file.write(doc.toprettyxml(indent="\t"))

    def parse_xml(self, xml_file):
        handler = XMLHandler()
        parser = xml.sax.make_parser()
        parser.setContentHandler(handler)
        parser.parse(xml_file)
        return handler.get_train_data()

    def get_from_xml(self, file_path):
        rows = self.parse_xml(file_path)
        return rows

    def add_to_xml_file(self, values):
        dict = {}
        tag = ["train_number", "departure_station", "departure_time", "arrival_station", "arrival_time", "travel_time"]
        for i in range(0,6):
            dict[tag[i]] = values[i]
        element = [dict]
        self.add_elements_to_xml_file(element)

    def add_elements_to_xml_file(self,elements):
        doc = xml.dom.minidom.parse(self.file_path)
        root = doc.documentElement
        for element in elements:
            train_element = doc.createElement('train')
            for key, value in element.items():
                child = doc.createElement(key)
                child_text = doc.createTextNode(value)
                child.appendChild(child_text)
                train_element.appendChild(child)
            root.appendChild(train_element)
        with open(self.file_path, 'w') as file:
            doc.writexml(file, addindent="  ", newl="\n")


class XMLHandler(xml.sax.ContentHandler):
    def __init__(self):
        self.current_data = ""
        self.train_data = []
        self.current_train = []

    def startElement(self, tag, attributes):
        self.current_data = tag

    def characters(self, content):
        if self.current_data in ["train_number", "departure_station", "departure_time", "arrival_station", "arrival_time", "travel_time"]:
            self.current_train.append(content)

    def endElement(self, tag):
        if tag == "train":
            self.train_data.append(self.current_train)
            self.current_train = []
        self.current_data = ""

    def get_train_data(self):
        return self.train_data