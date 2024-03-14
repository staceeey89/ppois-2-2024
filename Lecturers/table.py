import tkinter as tk
from tkinter import ttk, messagebox
from db import Lecturer
from typing import List
from constants import PAGE_SIZE


class Table:
    def __init__(self, main_window, function=None):
        self.main_window = main_window
        self.function = function
        self.start_index: int = 0
        self.page_size: int = PAGE_SIZE
        self._lecturers = None
        self._len = 0

        page_buttons_frame = tk.Frame(self.main_window)
        page_buttons_frame.pack(pady=10)

        label_frame = tk.Frame(self.main_window)
        label_frame.pack(pady=10)

        self.current_page_var = tk.IntVar(value=1)
        self.total_pages_var = tk.IntVar(value=0)

        first_page_button = tk.Button(page_buttons_frame, text="First", command=self.go_to_first_page)
        first_page_button.pack(side=tk.LEFT, padx=5)

        previous_page_button = tk.Button(page_buttons_frame, text="Previous", command=self.go_to_previous_page)
        previous_page_button.pack(side=tk.LEFT, padx=5)

        self.current_page_label = tk.Label(page_buttons_frame, text="")
        self.current_page_label.pack(side=tk.LEFT, padx=5)

        next_page_button = tk.Button(page_buttons_frame, text="Next", command=self.go_to_next_page)
        next_page_button.pack(side=tk.LEFT, padx=5)

        last_page_button = tk.Button(page_buttons_frame, text="Last", command=self.go_to_last_page)
        last_page_button.pack(side=tk.LEFT, padx=5)

        self.records_per_page_label = tk.Label(label_frame, text="Records per Page: ")
        self.records_per_page_label.pack(side=tk.LEFT, padx=5)

        page_size_options = list(map(str, range(1, 100)))
        self.page_size_var = tk.StringVar(value=str(self.page_size))
        self.page_size_dropdown = ttk.Combobox(label_frame, textvariable=self.page_size_var, values=page_size_options,
                                               width=5)
        self.page_size_dropdown.pack(side=tk.LEFT, padx=5)
        self.page_size_dropdown.bind("<<ComboboxSelected>>", self.update_page_size)
        self.page_size_dropdown.bind("<FocusOut>", self.update_page_size)
        self.page_size_dropdown.bind("<Return>", self.update_page_size)

        self.total_records_label = tk.Label(label_frame, text="")
        self.total_records_label.pack(side=tk.LEFT, padx=5)

        table_frame = ttk.Frame(self.main_window)
        table_frame.pack(padx=10, pady=10, fill=tk.X, expand=False)

        self.table = ttk.Treeview(table_frame)
        self.table["columns"] = ("Факультет", "Кафедра", "ФИО", "Учёное звание", "Учёная степень",
                                 "Стаж работы")

        self.table.heading("Факультет", text="Факультет")
        self.table.heading("Кафедра", text="Кафедра")
        self.table.heading("ФИО", text="ФИО")
        self.table.heading("Учёное звание", text="Учёное звание")
        self.table.heading("Учёная степень", text="Учёная степень")
        self.table.heading("Стаж работы", text="Стаж работы")
        self.table.column("Стаж работы", width=100)
        self.table.column("#0", width=50)

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.table.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.table.configure(yscrollcommand=scrollbar.set)
        self.table.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def show_table(self, lecturers: List[Lecturer], length: int):
        self._lecturers = lecturers
        self._len = length
        self._prepare_table()

    def _prepare_table(self):
        for row in self.table.get_children():
            self.table.delete(row)

        start_index = self.start_index

        for index, user in enumerate(self._lecturers, start=start_index + 1):
            self.table.insert("", index, text=str(index), values=(
                user.faculty,
                user.department,
                user.full_name,
                user.academic_title,
                user.academic_degree,
                user.years_of_experience)
                              )

        self.table.configure(height=self.page_size)
        self.update_page_info()

    def update_page_info(self):
        total_pages = (self._len + self.page_size - 1) // self.page_size
        self.total_pages_var.set(value=total_pages)

        self.total_records_label.config(text="Total Records: {}".format(self._len))
        if self.current_page_var.get() > total_pages:
            self.current_page_var.set(total_pages)
        elif self.current_page_var.get() == 0:
            self.current_page_var.set(1)
        self.current_page_label.config(text="Page: {}/{}".format(self.current_page_var.get(),
                                                                 total_pages))
        self.page_size_var = tk.StringVar(value=str(self.page_size))
        self.page_size_dropdown.set(str(self.page_size))

    def update_page_size(self, event=None):
        try:
            new_page_size = int(self.page_size_dropdown.get())
            if new_page_size > 0:
                new_crnt_pg = (self.page_size * (self.current_page_var.get() - 1) + new_page_size) // new_page_size
                self.page_size = new_page_size
                total_pages = (self._len + self.page_size - 1) // self.page_size
                self.total_pages_var.set(value=total_pages)
                self.current_page_var.set(value=new_crnt_pg)
                self.start_index = (new_crnt_pg - 1) * self.page_size
                self.function(self.start_index,
                              self.page_size)
            else:
                self.page_size_dropdown.set(str(self.page_size))
        except ValueError:
            self.page_size_dropdown.set(str(self.page_size))

    def go_to_first_page(self):
        self.current_page_var.set(1)
        self.start_index = 0
        self.function(self.start_index,
                      self.page_size)

    def go_to_last_page(self):
        self.current_page_var.set(self.total_pages_var.get())
        self.update_page_info()
        self.start_index = (self.total_pages_var.get() - 1) * self.page_size
        self.function(self.start_index,
                      self.page_size)

    def go_to_previous_page(self):
        current_page = self.current_page_var.get()
        if current_page > 1:
            self.current_page_var.set(current_page - 1)
            self.update_page_info()
            self.start_index -= self.page_size
            self.function(self.start_index,
                          self.page_size)

    def go_to_next_page(self):
        current_page = self.current_page_var.get()
        if current_page < self.total_pages_var.get():
            self.current_page_var.set(current_page + 1)
            self.update_page_info()
            self.start_index += self.page_size
            self.function(self.start_index,
                          self.page_size)


class ResultTable(Table):
    def __init__(self, main_window, function, request_window):
        super().__init__(main_window, function)
        self.__request_window = request_window

    def show_table(self, lecturers: List[Lecturer], length: int):
        if length == 0:
            messagebox.showinfo("Ничего не найдено",
                                "Поиск не дал результатов",
                                parent=self.main_window)
            self.main_window.destroy()
            return
        super().show_table(lecturers, length)
        self.__request_window.destroy()
