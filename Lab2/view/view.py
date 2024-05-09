from tkinter import *
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as mb
from datetime import datetime
from tkcalendar import *
from model.model import ModelBase
from .search_interface import SearchInterface
from .delete_interface import DeleteInterface
from .add_interface import AddInterface
from controller.xml import parser
import math
import re


class Interface:
    def __init__(self, model_base: ModelBase):
        self.window = Tk()
        self.window.title("Главное окно")
        self.window.geometry()
        frame = ttk.Frame(borderwidth=1, padding=[5, 5])
        frame.grid()

        self.search_window = None
        self.delete_window = None

        self.model_base = model_base
        self.parser = None

        self.page_amount = 0
        self.page_number = 1
        self.list_on_page = 5

        tk.Button(frame, text="Поиск", command=self.search_interface).grid(row=0, column=0)
        tk.Button(frame, text="Удаление", command=self.delete_interface).grid(row=0, column=1)
        tk.Button(frame, text="Включить вид дерева", command=self._tree_view).grid(row=0, column=2)
        tk.Button(frame, text="Загрузить xml", command=self._parse_from).grid(row=0, column=3)
        tk.Button(frame, text="Сохранить xml", command=self._save_to).grid(row=0, column=4)
        tk.Button(frame, text="Очистить", command=self._cleaning).grid(row=0, column=5, pady=19)
        tk.Button(frame, text="Добавить запись", command=self._gui_new_entries).grid(row=0, column=6, pady=19)

        main_frame = ttk.Labelframe(text="Медицинские карты", padding=[5, 5])

        columns = ("patient_surname", "patient_name", "registration_address", "birthday_date", "appointment_date",
                   "doctor_surname", "doctor_name", "doctor_statement")
        self.table = ttk.Treeview(main_frame, columns=columns, show="headings")
        self.table.heading(0, text="Фамилия пациента", anchor=W)
        self.table.heading(1, text="Имя пациента", anchor=W)
        self.table.heading(2, text="Адрес прописки", anchor=W)
        self.table.heading(3, text="Дата рождения", anchor=W)
        self.table.heading(4, text="Дата приема", anchor=W)
        self.table.heading(5, text="Фамилия врача", anchor=W)
        self.table.heading(6, text="Имя врача", anchor=W)
        self.table.heading(7, text="Заключение", anchor=W)

        self.table.grid(row=1, column=0, columnspan=4, pady=20)
        main_frame.grid(row=1, column=0, columnspan=6)

        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=self.table.yview)
        scrollbar.grid(row=1, column=6, sticky="ns")
        self.table.configure(yscrollcommand=scrollbar.set)

        self.total_records = len(self.model_base.loading())
        self.total_pages = self.calculate_total_pages()
        self.update_page_label()
        self.load_page(self.list_on_page)

        frame_for_pages = tk.Frame(borderwidth=1, relief=SOLID)
        frame_for_pages.grid()

        tk.Button(frame_for_pages, text="Первая страница", command=self.first_page).grid(row=3, column=0)
        tk.Button(frame_for_pages, text="Последняя страница", command=self.last_page).grid(row=3, column=3)
        tk.Button(frame_for_pages, text="Предыдущая страница", command=self.prev_page).grid(row=3, column=1)
        tk.Button(frame_for_pages, text="Следующая страница", command=self.next_page).grid(row=3, column=2)

        page_val = [5, 10, 15]
        self.page_var = StringVar(value=page_val[0])
        tk.Label(text="Количество записей на странице").grid(row=2, column=1, pady=10)
        page_combo = ttk.Combobox(textvariable=self.page_var, values=page_val)
        page_combo.grid(row=3, column=1)
        page_combo.bind("<<ComboboxSelected>>", self.selected)

        self.window.mainloop()

    def selected(self, event):
        self.list_on_page = int(self.page_var.get())
        self.total_pages = self.calculate_total_pages()
        self.load_page(self.list_on_page)

    def _cleaning(self):
        self.model_base.clean_data_base()
        self.total_pages = self.calculate_total_pages()
        self.update_page_label()
        self.load_page(self.list_on_page)

    def _parse_from(self):
        window3 = tk.Toplevel()
        window3.title("Выберите файл")
        window3.geometry()
        tk.Button(window3, text="file1", command=lambda: self.__choose_file_to_load(1)).grid(row=0, column=0)
        tk.Button(window3, text="file2", command=lambda: self.__choose_file_to_load(2)).grid(row=1, column=0)

    def __choose_file_to_load(self, file):
        filename = "xml_file" + str(file) + ".xml"
        self.parser = parser(filename)
        data = self.parser.from_xml()
        for i in data:
            self.model_base.new_entry(i)
        self.total_pages = self.calculate_total_pages()
        self.update_page_label()
        self.load_page(self.list_on_page)

    def _save_to(self):
        window3 = tk.Toplevel()
        window3.title("Выберите файл")
        window3.geometry()
        tk.Button(window3, text="file1", command=lambda: self.__choose_file_to_save(1)).grid(row=0, column=0)
        tk.Button(window3, text="file2", command=lambda: self.__choose_file_to_save(2)).grid(row=1, column=0)

    def _tree_view(self):
        tree_window = tk.Toplevel()
        tree_window.title("Вид дерева")
        tree_window.geometry("400x400")

        frame = tk.Frame(tree_window)
        frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(0, weight=1)

        tree = ttk.Treeview(frame, show="tree")
        tree.grid(row=0, column=0, sticky="nsew")

        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")

        tree.configure(yscrollcommand=scrollbar.set)

        i = 1
        for record in self.model_base.loading():
            tree.insert("", tk.END, iid=i, text=f"Медицинская карта: {record[0]}")
            tree.insert(str(i), index=tk.END, text=f"Фамилия пациента: {record[0]}")
            tree.insert(str(i), index=tk.END, text=f"Имя пациента: {record[1]}")
            tree.insert(str(i), index=tk.END, text=f"Адрес прописки: {record[2]}")
            tree.insert(str(i), index=tk.END, text=f"Дата рождения: {record[3]}")
            tree.insert(str(i), index=tk.END, text=f"Дата приема: {record[4]}")
            tree.insert(str(i), index=tk.END, text=f"Фамилия врача: {record[5]}")
            tree.insert(str(i), index=tk.END, text=f"Имя врача: {record[6]}")
            tree.insert(str(i), index=tk.END, text=f"Заключение: {record[7]}")
            i += 1

        tree_window.mainloop()

    def __choose_file_to_save(self, file):
        filename = "xml_file" + str(file) + ".xml"
        self.parser = parser(filename)
        data = self.model_base.loading()
        if data is None:
            mgs = "no records"
            mb.showerror("error", mgs)
        else:
            self.parser.to_xml(data)

    def calculate_total_pages(self):
        self.total_records = len(self.model_base.loading())
        return math.ceil(self.total_records / self.list_on_page)

    def update_page_label(self):
        tk.Label(text=f"Страница {self.page_number}/{self.total_pages}").grid(row=2, column=0, pady=10)
        tk.Label(text=f"Общее количество записей: {self.total_records}").grid(row=2, column=2, pady=10)

    def first_page(self):
        self.page_number = 1
        self.load_page(self.list_on_page)
        self.update_page_label()

    def last_page(self):
        self.page_number = self.total_pages
        self.load_page(self.list_on_page)
        self.update_page_label()

    def load_page(self, limit):
        if self.page_number == 0:
            self.page_number = 1
        self._view_loading((self.page_number - 1) * limit, limit)
        self.update_page_label()

    def prev_page(self):
        if self.page_number > 1:
            self.page_number -= 1
            self.load_page(self.list_on_page)

    def next_page(self):
        if self.page_number < self.total_pages:
            self.page_number += 1
            self.load_page(self.list_on_page)

    def _view_loading(self, offset=0, limit=0):
        for item in self.table.get_children():
            self.table.delete(item)
        for i in self.model_base.loading(offset, limit):
            self.table.insert("", END, values=i)

    def search_interface(self):
        self.search_window = SearchInterface(self.model_base)

    def delete_interface(self):
        self.delete_window = DeleteInterface(self.model_base, self)

    def _gui_new_entries(self):
        self.add_window = AddInterface(self.model_base, self)
