from model import Model
from table import TableView
from datetime import datetime
from information_board import InformationBoard
import xml.etree.ElementTree as ET
import time
import tkinter as tk
import math
import os


class Controller():
    def __init__(self):
        self.file_path = None
        self.type = None

    def check_original_file(self, file_path: str):
        if file_path[-3:] != ".db" and file_path[-4:] != ".xml":
            return True
        if os.path.exists(file_path):
            self.file_path = file_path
            self.type = file_path[-2:]
            self.model = Model(file_path,self.type)
            return False
        else:
            return True

    def get_message(self, entry):
        print(entry.get())

    def set_connect(self, file_path):
        self.file_path = file_path

    def create_db_file(self, file_name):
        root = "../database/"
        expansion = ".db"
        root = root + file_name + expansion
        if os.path.exists(root):
            return True, root
        self.type = "db"
        self.model = Model(root,self.type)
        self.model.create_information_board()

    def create_xml_file(self, file_name):
        root = "../database/"
        expansion = ".xml"
        root = root + file_name + expansion
        if os.path.exists(root):
            return True, root
        self.type = "ml"
        self.model = Model(root,self.type)
        self.model.create_xml_file()
        self.file_path = root

    def delete_file(self, file_path):
        if os.path.exists(file_path):
            os.remove(file_path)

    def create_info_board(self, root, per_page):
        if self.type == "db":
            rows: list = self.model.get_info_array()
            page_number = math.ceil(len(rows) / per_page)
            data = ["| ".join(map(str, row)) for row in rows]
            self.table = TableView(root, data, page_number, 320, 200, per_page)
        else:
            rows: list = self.model.get_from_xml(self.file_path)
            page_number = math.ceil(len(rows) / per_page)
            values = ""
            data = []
            for row in rows:
                values = '|'.join(row)
                data.append(values)
            self.table = TableView(root,data,page_number,320,200,per_page)

    def window_add_into_database(self, root, x, y):
        if self.type == "db":
            rows: list = self.model.get_info_array()
            page_number = math.ceil(len(rows) / 10)
            data = ["| ".join(map(str, row)) for row in rows]
            self.table = TableView(root, data, page_number, x, y, 10)
        else:
            rows: list = self.model.get_from_xml(self.file_path)
            page_number = math.ceil(len(rows) / 10)
            data = ["| ".join(map(str, row)) for row in rows]
            self.table = TableView(root, data, page_number, x, y, 10)
    def add_to_database(self, data, root, label=None):
        if self.check_correct_input_data(data):
            date_format = "%Y-%m-%d %H:%M"
            date_time1 = datetime.strptime(data[2].get(), date_format)
            date_time2 = datetime.strptime(data[4].get(), date_format)
            time_difference = date_time2 - date_time1
            formatted_time_difference = f"{time_difference.days} days, {time_difference.seconds // 3600} hours, {(time_difference.seconds // 60) % 60} minutes"

            info_line = InformationBoard(data[0].get(), data[1].get(), data[2].get(), data[3].get(), data[4].get(),
                                         formatted_time_difference)
            info_row = [data[0].get(), data[1].get(), data[2].get(), data[3].get(), data[4].get(),
                                         formatted_time_difference]
            if self.type == "db":
                self.model.add_to_information_board(info_line)
            else:
                self.model.add_to_xml_file(info_row)
            return self.clear_field(data, root)
        if label:
            label.destroy()

    def clear_field(self, data, root):
        data[0].delete(0, tk.END)
        data[1].delete(0, tk.END)
        data[2].delete(0, tk.END)
        data[3].delete(0, tk.END)
        data[4].delete(0, tk.END)
        label = tk.Label(root, text="Запись успешно добавлена",
                         font=("Times New Roman", 12), fg="black", borderwidth=1, relief="solid")
        label.place(x=470, y=47)
        return label

    def get_data(self,data):
        new_data = []
        for i in range(6):
            new_data.append(data[i].get())
        return new_data
    def check_correct_input_data(self, data: list):
        flag = True
        if data[0].get() == None or data[1].get() == None or data[2].get() == None or data[3].get() == None \
                or data[4].get() == None:
            flag = False
        if not data[0].get().isdigit():
            data[0].delete(0, tk.END)
            flag = False
        if not data[1].get().isalpha():
            data[1].delete(0, tk.END)
            flag = False
        if not data[3].get().isalpha():
            data[3].delete(0, tk.END)
            flag = False
        if self.check_correct_format_data(data[2]):
            data[2].delete(0, tk.END)
            flag = False
        if self.check_correct_format_data(data[4], data[2]):
            data[4].delete(0, tk.END)
            flag = False
        return flag

    def check_correct_format_data(self, data, logic=None):
        text = data.get()
        try:
            datetime.strptime(text, "%Y-%m-%d %H:%M")
            if logic:
                date_format = "%Y-%m-%d %H:%M"
                date_time1 = datetime.strptime(data.get(), date_format)
                date_time2 = datetime.strptime(logic.get(), date_format)
                if date_time2 >= date_time1:
                    data.delete(0, tk.END)
                    return True
            return False
        except ValueError:
            data.delete(0, tk.END)
            return True

    def get_result_of_search(self, data: list, root, x, y):
        if self.type == "db":
            parametr = ["train_number", "departure_station", "departure_time", "arrival_station", "arrival_time",
                        "travel_time"]
            conditions = "WHERE "
            values = []
            for i in range(0, 6):
                if data[i]:
                    if conditions != "WHERE ":
                        conditions += " AND "
                    conditions += parametr[i]
                    conditions += " = ?"
                    values.append(data[i])
            if len(values) == 0:
                self.window_add_into_database(root, x, y)
                return
            info = self.model.search_from_database(conditions, values)
            page_number = math.ceil(len(info) / 10)
            data = ["| ".join(map(str, row)) for row in info]
            self.table.label_table.destroy()
            self.table = TableView(root, data, page_number, x, y, 10)
        else:
            data = self.change_input_data_list(data)
            info = self.get_info_by_dict()
            output = self.comparison(data,info)
            result = []
            result = self.transform_to_string(output)
            page_number = math.ceil(len(result) / 10)
            self.table = TableView(root, result, page_number, x, y, 10)

    def transform_to_string(self,data):
        buffer_data = []
        result = []
        for row in data:
            buffer_data.append(list(row.values()))
        for row in buffer_data:
            result_string = '|'.join(row)
            result.append(result_string)
        return result

    def comparison(self,data,info: list):
        buffer_list = []
        dict_iter = iter(data.items())
        for i in range(len(data)):
            key, value = next(dict_iter)
            for inf in info:
                if inf.get(key) == value:
                    buffer_list.append(inf)
            info = buffer_list.copy()
            buffer_list.clear()
        return info

    def get_info_by_dict(self):
        keys = ["train_number", "departure_station", "departure_time", "arrival_station",
                "arrival_time", "travel_time"]
        info = []
        trains = self.model.get_from_xml(self.file_path)
        for train in trains:
            temp_dict = {}
            for i in range(6):
                temp_dict[keys[i]] = train[i]
            info.append(temp_dict)
        return info



    def change_input_data_list(self,data: list):
        parametr = ["train_number", "departure_station", "departure_time", "arrival_station",
                    "arrival_time", "travel_time"]
        dict = {}
        for i in range(6):
            if data[i] != "":
                dict[parametr[i]] = data[i]
        return dict



    def destroy_table(self):
        self.table.destroy()

    def check_delete_info(self, columns):
        if self.type == "db":
            parametr = ["train_number = ", "departure_station = ", "departure_time = ", "arrival_station = ",
                        "arrival_time = ", "travel_time = "]
            num_deleted_rows = 0
            for i in range(0, 6):
                if columns[i]:
                    condition = parametr[i]
                    condition += self.check_column_data(columns[i])
                    num_deleted_rows += self.model.delete_from_database(condition)
            if num_deleted_rows == 0:
                return f"Записи не были найдены"
            else:
                return f"Было удалено {num_deleted_rows} записей"
        else:
            res = self.delete_info_into_xml(columns)
            return res

    def delete_info_into_xml(self,data):
        cond = self.change_input_data_list(data)
        info = self.get_info_by_dict()
        output = self.comparison(cond, info)
        result = []
        result = self.transform_to_string(output)
        if len(result) == 0:
            return f"Записи не были найдены"
        else:
            self.remove_from_xml_file(output)
            return f"Было удалено {len(result)} записей"

    def remove_from_xml_file(self,trains_data):
        tree = ET.parse(self.file_path)
        root = tree.getroot()
        for train in trains_data:
            train_number = train['train_number']
            departure_station = train['departure_station']
            departure_time = train['departure_time']
            arrival_station = train['arrival_station']
            arrival_time = train['arrival_time']
            travel_time = train['travel_time']

            for element in root.findall(".//train"):
                if (element.find("train_number").text == train_number and
                        element.find("departure_station").text == departure_station and
                        element.find("departure_time").text == departure_time and
                        element.find("arrival_station").text == arrival_station and
                        element.find("arrival_time").text == arrival_time and
                        element.find("travel_time").text == travel_time):
                    root.remove(element)
        tree.write(self.file_path)
    def check_column_data(self,data):
        if data.isdigit():
            return data
        else:
            text = f"\"{data}\""
            return text

    def create_tree(self):
        if self.type == "db":
            data = self.model.get_info_array()
        else:
            data = self.model.get_from_xml(self.file_path)
        index = 1
        text = "trains\n"
        for row in data:
            text += f"|---{index}\n"
            index += 1
            text += f"|   |-train_number: {row[0]}\n"
            text += f"|   |-departure_station: {row[1]}\n"
            text += f"|   |-departure_time: {row[2]}\n"
            text += f"|   |-arrival_station: {row[3]}\n"
            text += f"|   |-arrival_time: {row[4]}\n"
            text += f"|   |-travel_time: {row[5]}\n"
        return text

