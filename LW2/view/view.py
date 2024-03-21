import importlib
import tkinter as tk
from datetime import datetime
from tkinter import simpledialog
from tkinter import ttk
from tkcalendar import DateEntry

import constants
from constants import LIMIT
from controller.controller import Controller
from entity.clinic import PetRecord
from repository.clinic_repository import PetRecordRepositoryList, PetRecordRepositorySQL
from util.connection_manager import ConnectionManager


class View:
    def __init__(self, controller: Controller):
        self.controller = controller

    def create_start_window(self):
        self.root = tk.Tk()
        self.limit_for_main_table = 10
        self.root.geometry("1100x500")
        self.root.title("Veterinary clinic")
        self.f_for_buttons = tk.Frame(self.root)
        self.f_for_table = tk.Frame(self.root)
        self.f_for_pages_buttons = tk.Frame(self.root)

        self.f_for_buttons.place(relx=0.0, rely=0, relwidth=1, relheight=0.5)
        self.f_for_table.place(relx=0.0, rely=0.5, relwidth=1, relheight=0.4)
        self.f_for_pages_buttons.place(relx=0.0, rely=0.9, relwidth=1, relheight=0.1)
        self.offset_for_main_window = 0
        # Добавляем кнопку "Добавить запись"
        add_button = tk.Button(self.f_for_buttons, text="Добавить запись", command=self.open_add_record_window)
        search_button = tk.Button(self.f_for_buttons, text="Найти по условию", command=self.open_search_window)
        delete_button = tk.Button(self.f_for_buttons, text="Удалить по условию", command=self.open_delete_window)
        add_to_db_button = tk.Button(self.f_for_buttons, text="Добавить в базу данных", command=self.add_to_db)
        get_from_db_button = tk.Button(self.f_for_buttons, text="Извлечь из базы данных", command=self.get_from_db)
        add_to_xml_button = tk.Button(self.f_for_buttons, text="Добавить в xml файл", command=self.write_to_xml_file)
        get_from_xml_button = tk.Button(self.f_for_buttons, text="Извлечь из xml файла", command=self.get_from_xml_file)
        show_tree_button = tk.Button(self.f_for_buttons, text="Показать записи в виде дерева",
                                     command=self.show_records_as_tree)
        add_button.grid(row=0, column=0, padx=10, pady=20)
        search_button.grid(row=0, column=1, padx=10, pady=20)
        delete_button.grid(row=0, column=2, padx=10, pady=20)
        add_to_db_button.grid(row=1, column=0, padx=10, pady=20)
        get_from_db_button.grid(row=1, column=1, padx=10, pady=20)
        add_to_xml_button.grid(row=1, column=2, padx=10, pady=20)
        get_from_xml_button.grid(row=2, column=0, padx=10, pady=20)
        show_tree_button.grid(row=2, column=1, padx=10, pady=20)
        self.main_table = self.create_table(self.f_for_table)
        self.main_table.pack(expand=tk.YES, fill=tk.BOTH)
        next_page_button = tk.Button(self.f_for_pages_buttons, text="Следующая страница",
                                     command=lambda: self.next_page(self.main_table))
        prev_page_button = tk.Button(self.f_for_pages_buttons, text="Прошлая страница",
                                     command=lambda: self.prev_page(self.main_table))
        first_page_button = tk.Button(self.f_for_pages_buttons, text="Первая страница",
                                      command=lambda: self.first_page(self.main_table))

        last_page_button = tk.Button(self.f_for_pages_buttons, text="Последняя страница",
                                     command=lambda: self.last_page(self.main_table))
        self.current_page_label = tk.Label(self.f_for_pages_buttons, text="Текущая страница: 1")
        update_limit_button = tk.Button(self.f_for_pages_buttons, text="Обновить LIMIT",
                                        command=lambda: self.update_limit(1))

        # Размещаем кнопки под таблицей
        prev_page_button.grid(row=0, column=0, padx=10, pady=20)
        next_page_button.grid(row=0, column=1, padx=10, pady=20)
        first_page_button.grid(row=0, column=2, padx=10, pady=20)
        last_page_button.grid(row=0, column=3, padx=10, pady=20)
        self.current_page_label.grid(row=0, column=4, padx=10, pady=20)
        update_limit_button.grid(row=0, column=5, padx=10, pady=20)
        records = self.controller.get_record_with_offset(0)
        self.update_table(self.main_table, records)

    def create_table(self, frame):
        heads = ["pet name", "birth date", "last visit date", "vet full name", "diagnosis"]
        table = ttk.Treeview(frame, show="headings")
        table["columns"] = heads

        for header in heads:
            table.heading(header, text=header, anchor="center")
            table.column(header, anchor="center")

        return table

    def update_table(self, table, pet_records):
        table.delete(*table.get_children())  # Очистить существующие записи

        for record in pet_records:
            table.insert('', 'end', values=(
                record.pet_name, record.birth_date, record.last_visit_date, record.vet_full_name, record.diagnosis))

    def open_add_record_window(self):
        # Открываем окно для добавления записи
        add_record_window = tk.Toplevel(self.root)
        add_record_window.title("Add Record")

        # Добавляем элементы пользовательского интерфейса для ввода данных о питомце
        pet_name_label = tk.Label(add_record_window, text="Имя питомца:")
        pet_name_label.grid(row=0, column=0, padx=10, pady=5)
        self.pet_name_entry = tk.Entry(add_record_window)
        self.pet_name_entry.grid(row=0, column=1, padx=10, pady=5)

        birth_date_label = tk.Label(add_record_window, text="Дата рождения:")
        birth_date_label.grid(row=1, column=0, padx=10, pady=5)
        self.birth_date_entry = DateEntry(add_record_window)
        self.birth_date_entry.grid(row=1, column=1, padx=10, pady=5)

        last_visit_date_label = tk.Label(add_record_window, text="Дата последнего посещения:")
        last_visit_date_label.grid(row=2, column=0, padx=10, pady=5)
        self.last_visit_date_entry = DateEntry(add_record_window)
        self.last_visit_date_entry.grid(row=2, column=1, padx=10, pady=5)

        vet_full_name_label = tk.Label(add_record_window, text="ФИО врача:")
        vet_full_name_label.grid(row=3, column=0, padx=10, pady=5)
        self.vet_full_name_entry = tk.Entry(add_record_window)
        self.vet_full_name_entry.grid(row=3, column=1, padx=10, pady=5)

        diagnosis_label = tk.Label(add_record_window, text="Диагноз:")
        diagnosis_label.grid(row=4, column=0, padx=10, pady=5)
        self.diagnosis_entry = tk.Entry(add_record_window)
        self.diagnosis_entry.grid(row=4, column=1, padx=10, pady=5)

        # Кнопка "Сохранить"
        save_button = tk.Button(add_record_window, text="Сохранить",
                                command=lambda: self.save_record(add_record_window))
        save_button.grid(row=5, column=0, columnspan=2, pady=10)

    def save_record(self, window_to_close):
        pet_name = self.pet_name_entry.get()
        birth_date = self.birth_date_entry.get()
        last_visit_date = self.last_visit_date_entry.get()
        vet_full_name = self.vet_full_name_entry.get()
        diagnosis = self.diagnosis_entry.get()

        # Вызываем метод контроллера для сохранения записи

        pet_record = PetRecord(pet_name, birth_date, last_visit_date, vet_full_name, diagnosis)
        self.controller.add_record(pet_record)
        # Закрываем окно добавления записи
        window_to_close.destroy()
        records = self.controller.get_record_with_offset(0)
        self.update_table(self.main_table, records)

    def open_search_window(self):
        search_window = tk.Toplevel(self.root)
        search_window.geometry("1000x650")  # Увеличим высоту окна
        search_window.title("Search Record")

        frame_name, frame_FIO, frame_diagnosis = self.create_frames(search_window)

        self.create_entry_and_button(frame_name, 1, "Поиск", "Имя животного:", "Дата рождения")
        self.create_entry_and_button(frame_FIO, 2, "Поиск", "ФИО врача:", "Дата последнего посещения:")
        self.create_entry_and_button(frame_diagnosis, 3, "Поиск", "Подстрока диагноза")

        total_height = 0.5  # Высота трех верхних фреймов
        frame_bottom = tk.Frame(search_window, width=450, height=450)
        frame_bottom.place(relx=0, rely=total_height, relwidth=1, relheight=1 - total_height - 0.1)
        self.search_table = self.create_table(frame_bottom)
        self.search_table.pack(expand=tk.YES, fill=tk.BOTH)

        frame_pages = tk.Frame(search_window, width=450, height=50)
        frame_pages.place(relx=0, rely=0.9, relwidth=1, relheight=0.1)

        next_page_button = tk.Button(frame_pages, text="Следующая страница",
                                     command=lambda: self.next_page_for_search(self.search_table))
        prev_page_button = tk.Button(frame_pages, text="Прошлая страница",
                                     command=lambda: self.prev_page_for_search(self.search_table))
        first_page_button = tk.Button(frame_pages, text="Первая страница",
                                      command=lambda: self.first_page_for_search(self.search_table))

        last_page_button = tk.Button(frame_pages, text="Последняя страница",
                                     command=lambda: self.last_page_for_search(self.search_table))

        self.current_page_label_for_search = tk.Label(frame_pages, text="Текущая страница: 1")

        # Размещаем кнопки под таблицей
        prev_page_button.grid(row=0, column=0, padx=10, pady=20)
        next_page_button.grid(row=0, column=1, padx=10, pady=20)
        first_page_button.grid(row=0, column=2, padx=10, pady=20)
        last_page_button.grid(row=0, column=3, padx=10, pady=20)
        self.current_page_label_for_search.grid(row=0, column=4, padx=10, pady=20)

        search_window.mainloop()

    def open_delete_window(self):
        delete_window = tk.Toplevel(self.root)
        delete_window.geometry("1000x600")  # Увеличим высоту окна
        delete_window.title("Delete Record")

        frame_name, frame_FIO, frame_diagnosis = self.create_frames(delete_window)

        self.create_entry_and_button(frame_name, 1, "Удалить", "Имя животного:", "Дата рождения")
        self.create_entry_and_button(frame_FIO, 2, "Удалить", "ФИО врача:", "Дата последнего посещения:")
        self.create_entry_and_button(frame_diagnosis, 3, "Удалить", "Подстрока диагноза")

        total_height = 0.5  # Высота трех верхних фреймов
        self.frame_bottom = tk.Frame(delete_window, width=450, height=450)
        self.frame_bottom.place(relx=0, rely=total_height, relwidth=1, relheight=1 - total_height)

        # Добавляем виджет Label для отображения сообщения
        self.message_label = tk.Label(self.frame_bottom, text="Your message here", font=("Arial", 14),
                                      fg="white")
        self.message_label.pack(expand=True, fill=tk.BOTH)  # Заполнение всего пространства во фрейме

        delete_window.mainloop()

    def create_frames(self, search_window):
        frame_name = tk.Frame(search_window, width=150, height=150)
        frame_FIO = tk.Frame(search_window, width=150, height=150)
        frame_diagnosis = tk.Frame(search_window, width=150, height=150)

        frame_name.place(relx=0, rely=0, relwidth=0.33, relheight=0.5)
        frame_FIO.place(relx=0.33, rely=0, relwidth=0.33, relheight=0.5)
        frame_diagnosis.place(relx=0.66, rely=0, relwidth=0.33, relheight=0.5)

        return frame_name, frame_FIO, frame_diagnosis

    def create_entry_and_button(self, parent_frame, method, type, label_text1, label_text2="default"):

        l_first_searching_column = tk.Label(parent_frame, text=label_text1)
        l_first_searching_column.grid(row=0, column=0, padx=10, pady=5)

        e_first_searching_column = tk.Entry(parent_frame)
        e_first_searching_column.grid(row=0, column=1, padx=10, pady=5)
        e_second_searching_column = None
        if label_text2 != "default":
            l_second_searching_column = tk.Label(parent_frame, text=label_text2)
            l_second_searching_column.grid(row=1, column=0, padx=10, pady=5)
            e_second_searching_column = DateEntry(parent_frame)
            e_second_searching_column.grid(row=1, column=1, padx=10, pady=5)

        # Создаем кнопку "Поиск"
        if (type == "Поиск"):
            button = tk.Button(parent_frame, text="Поиск",
                               command=lambda: self.search_records(e_first_searching_column,
                                                                   e_second_searching_column, method))
        else:
            button = tk.Button(parent_frame, text="Удалить",
                               command=lambda: self.delete_records(e_first_searching_column,
                                                                   e_second_searching_column, method))
        button.grid(row=2, column=0, columnspan=2, pady=10)

    def search_records(self, first_searching_column, second_searching_column, method=1):
        self.choices = []
        self.offset_for_search = 0
        self.method = method
        # Получаем значения из текстовых полей
        value1 = first_searching_column.get()
        # Проверяем, есть ли второе поле
        if hasattr(second_searching_column, 'get'):
            value2 = second_searching_column.get()
        else:
            value2 = None
        self.choices.append(first_searching_column)
        self.choices.append(second_searching_column)
        records = self.perform_search(value1, value2, method, self.offset_for_search)
        self.update_table(self.search_table, records)
        self.offset_for_search = 0
        self.update_page_number_label(self.offset_for_search, self.current_page_label_for_search)

    def delete_records(self, first_searching_column, second_searching_column, method=1):
        # Получаем значения из текстовых полей
        value1 = first_searching_column.get()
        # Проверяем, есть ли второе поле
        if hasattr(second_searching_column, 'get'):
            value2 = second_searching_column.get()
        else:
            value2 = None

        if method == 1:
            message = self.controller.delete_record_by_name_and_birth(value2, value1)
        elif method == 2:
            message = self.controller.delete_record_by_last_visit_and_vet(value2, value1)
        elif method == 3:
            message = self.controller.delete_record_by_diagnosis(value1)

        for widget in self.frame_bottom.winfo_children():
            widget.destroy()

            # Добавляем сообщение в Label и помещаем его в четвертый фрейм
        message_label = tk.Label(self.frame_bottom, text=message, font=("Arial", 14), fg="black")
        message_label.pack(expand=True, fill=tk.BOTH)
        records = self.controller.get_record_with_offset(0)
        self.update_table(self.main_table, records)
        self.offset_for_search = 0
        self.update_page_number_label(self.offset_for_search, self.current_page_label)

    def start(self):
        self.create_start_window()
        self.root.mainloop()

    def next_page(self, table):
        records = self.controller.get_record_with_offset(self.offset_for_main_window)
        if len(records) == LIMIT and len(self.controller.get_record_with_offset(self.offset_for_main_window + 1, self.limit_for_main_table)) != 0:
            self.offset_for_main_window += 1
            records = self.controller.get_record_with_offset(self.offset_for_main_window, self.limit_for_main_table)
        self.update_table(table, records)
        self.update_page_number_label(self.offset_for_main_window, self.current_page_label)

    def prev_page(self, table):
        if self.offset_for_main_window >= 1:
            self.offset_for_main_window -= 1
        records = self.controller.get_record_with_offset(self.offset_for_main_window, self.limit_for_main_table)
        self.update_table(table, records)
        self.update_page_number_label(self.offset_for_main_window, self.current_page_label)

    def first_page(self, table):
        self.offset_for_main_window = 0
        records = self.controller.get_record_with_offset(self.offset_for_main_window)
        self.update_table(table, records)
        self.update_page_number_label(self.offset_for_main_window, self.current_page_label)

    def last_page(self, table):
        total_records = len(self.controller.get_all_records())
        last_offset = max(0, (total_records - 1) // LIMIT)
        self.offset_for_main_window = last_offset
        records = self.controller.get_record_with_offset(last_offset)
        self.update_table(table, records)
        self.update_page_number_label(self.offset_for_main_window, self.current_page_label)

    def next_page_for_search(self, table):
        first_value = self.choices[0].get()
        if self.choices[1] != None:
            second_value = self.choices[1].get()
        else:
            second_value = None
        records = self.perform_search(first_value, second_value, self.method, self.offset_for_search)
        if len(records) == LIMIT and len(
                self.perform_search(first_value, second_value, self.method, self.offset_for_search + 1)):
            self.offset_for_search += 1
            records = self.perform_search(first_value, second_value, self.method, self.offset_for_search)
        self.update_table(table, records)
        self.update_page_number_label(self.offset_for_search, self.current_page_label_for_search)

    def prev_page_for_search(self, table):
        first_value = self.choices[0].get()
        if self.choices[1] != None:
            second_value = self.choices[1].get()
        else:
            second_value = None
        if self.offset_for_search >= 1:
            self.offset_for_search -= 1
        records = self.perform_search(first_value, second_value, self.method, self.offset_for_search)
        self.update_table(table, records)
        self.update_page_number_label(self.offset_for_search, self.current_page_label_for_search)

    def first_page_for_search(self, table):
        first_value = self.choices[0].get()
        if self.choices[1] != None:
            second_value = self.choices[1].get()
        else:
            second_value = None
        self.offset_for_search = 0
        records = self.perform_search(first_value, second_value, self.method, self.offset_for_search)
        self.update_table(table, records)
        self.update_page_number_label(self.offset_for_search, self.current_page_label_for_search)

    def last_page_for_search(self, table):
        first_value = self.choices[0].get()
        if self.choices[1] != None:
            second_value = self.choices[1].get()
        else:
            second_value = None
        records = self.perform_search(first_value, second_value, self.method, self.offset_for_search)
        while (len(records) == LIMIT):
            self.offset_for_search += 1
            records = self.perform_search(first_value, second_value, self.method, self.offset_for_search)
        self.update_table(table, records)
        self.update_page_number_label(self.offset_for_search, self.current_page_label_for_search)

    def perform_search(self, value1, value2, method, offset):
        if method == 1:
            records = self.controller.find_by_birth_and_name(value2, value1, offset)
        elif method == 2:
            records = self.controller.find_by_last_visit_and_vet(value2, value1, offset)
        elif method == 3:
            records = self.controller.find_by_diagnosis(value1, offset)
        return records

    def add_to_db(self):
        self.controller.add_to_db()

    def get_from_db(self):
        self.controller.get_from_db()
        records = self.controller.get_record_with_offset(0)
        self.update_table(self.main_table, records)

    def get_from_xml_file(self):
        self.controller.get_from_xml_file()
        records = self.controller.get_record_with_offset(0)
        self.update_table(self.main_table, records)

    def write_to_xml_file(self):
        self.controller.write_to_xml_file()

    def create_record_treeview(self, records):
        # Создаем окно для отображения записей в виде дерева
        record_treeview_window = tk.Toplevel(self.root)
        record_treeview_window.geometry("600x400")
        record_treeview_window.title("Records Treeview")

        # Создаем Treeview
        treeview = ttk.Treeview(record_treeview_window, columns=("Value"))
        treeview.heading("#0", text="Поле")
        treeview.heading("Value", text="Значение")
        treeview.pack(expand=True, fill=tk.BOTH)

        # Заполняем Treeview данными из массива записей
        for record in records:
            # Создаем корневой узел для каждой записи
            record_node = treeview.insert("", "end")

            # Добавляем узел "Животное"
            pet_node = treeview.insert(record_node, "end", text="Животное")
            treeview.insert(pet_node, "end", text="Имя", values=(record.pet_name,))
            treeview.insert(pet_node, "end", text="Дата рождения", values=(record.birth_date,))

            # Добавляем узел "Дополнительная информация"
            info_node = treeview.insert(record_node, "end", text="Сведения о записи")
            treeview.insert(info_node, "end", text="Дата последнего посещения", values=(record.last_visit_date,))
            treeview.insert(info_node, "end", text="ФИО врача", values=(record.vet_full_name,))
            treeview.insert(info_node, "end", text="Диагноз", values=(record.diagnosis,))

    def show_records_as_tree(self):
        records = self.controller.get_all_records()
        self.create_record_treeview(records)

    def update_page_number_label(self, page, label):
        label.config(text=f"Текущая страница: {page + 1}")

    def update_limit(self, page):
        new_limit = simpledialog.askinteger("Изменение LIMIT", "Введите новое значение LIMIT:")
        if new_limit is not None:
            # Обработка нового значения LIMIT, например, обновление таблицы с новым LIMIT
            if page == 1:
                self.limit_for_main_table = new_limit
            records = self.controller.get_record_with_offset(0)
            self.update_table(self.main_table, records)
