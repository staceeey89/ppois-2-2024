import math
import tkinter
from tkinter import ttk

import controllers.DAO
import views.window_operations
from models.source_type import SourceType


class SelectResultWindow(tkinter.Toplevel):
    def __init__(self, master, application, filter_criteria):
        super().__init__(master)
        self.application = application
        self.filter_criteria = filter_criteria
        self.title("Search result")
        self.current_page = 1
        self.page_size = 10
        views.window_operations.window_center(self, 1000, 700)
        self.page_prev_button = ttk.Button(self, text="<", width=1, command=self.prev_page_click)
        self.page_next_button = ttk.Button(self, text=">", width=1, command=self.next_page_click)
        self.first_page_button = ttk.Button(self, text="<<", width=2, command=lambda: self.change_page(1))
        self.last_page_button = ttk.Button(self, text=">>", width=2, command=lambda: self.change_page(
            math.ceil(self.application.train_trips_dao.get_rows_count_by_filter(self.filter_criteria) / self.page_size)))
        self.current_page_combobox = ttk.Combobox(self, width=2, values=list(
            [str(i) for i in range(1, math.ceil((self.application.train_trips_dao.get_rows_count() / self.page_size)) + 1)]))
        self.current_page_combobox.set(self.current_page)
        self.current_page_combobox.bind("<<ComboboxSelected>>",
                                        func=lambda event: self.change_page(int(self.current_page_combobox.get())))
        self.page_size_label = ttk.Label(self, text="Кол-во записей:")
        self.page_size_combobox = ttk.Combobox(self, width=2, values=["5", "10", "15", "20"])
        self.page_size_combobox.set(10)
        self.page_size_button = ttk.Button(self, text="OK", width=2,
                                           command=lambda: self.change_page_size(int(self.page_size_combobox.get())))

        columns = (
            "train_id",
            "departure_station",
            "arrival_station",
            "departure_datetime",
            "arrival_datetime",
            "travel_time"
        )

        self.table = ttk.Treeview(master=self, columns=columns, show="headings", height=26)
        self.button = ttk.Button(master=self, text="OK", command=self.destroy)
        self.table.place(x=50, y=30)
        views.window_operations.widget_center(self.button, 1000, 650)
        views.window_operations.widget_center(self.current_page_combobox, 1000, 565)
        self.page_prev_button.place(x=430, y=565)
        self.page_next_button.place(x=522, y=565)
        self.first_page_button.place(x=370, y=565)
        self.last_page_button.place(x=573, y=565)
        self.page_size_label.place(x=370, y=598)
        views.window_operations.widget_center(self.page_size_combobox, 1000, 595)
        self.page_size_button.place(x=520, y=595)

        self.table.heading("train_id", text="Номер поезда")
        self.table.heading("departure_station", text="Станция отправления")
        self.table.heading("arrival_station", text="Станция прибытия")
        self.table.heading("departure_datetime", text="Дата и время отправления")
        self.table.heading("arrival_datetime", text="Дата и время прибытия")
        self.table.heading("travel_time", text="Время в пути")

        self.table.column("train_id", width=120, anchor=tkinter.CENTER)
        self.table.column("departure_station", width=140, anchor=tkinter.CENTER)
        self.table.column("arrival_station", width=140, anchor=tkinter.CENTER)
        self.table.column("departure_datetime", width=180, anchor=tkinter.CENTER)
        self.table.column("arrival_datetime", width=180, anchor=tkinter.CENTER)
        self.table.column("travel_time", width=140, anchor=tkinter.CENTER)
        self.update_train_trips_table()

    def update_train_trips_table(self):
        if self.application.source_type == SourceType.database:
            self.application.train_trips_dao = controllers.DAO.TrainTripDAO()
            values = self.application.train_trips_dao.select_by_filter(self.filter_criteria, self.current_page, self.page_size)
            self.current_page_combobox.config(values=list([str(i) for i in range(1, math.ceil(
                (self.application.train_trips_dao.get_rows_count_by_filter(self.filter_criteria) / self.page_size)) + 1)]))

        else:
            values = self.application.xml_parser.select_by_filter_page(self.filter_criteria, self.current_page, self.page_size)
            self.current_page_combobox.config(values=list(
                [str(i) for i in range(1, math.ceil((len(self.application.xml_parser.select_by_filter_page(self.filter_criteria, self.current_page, self.page_size)) / self.page_size)) + 1)]))

        for item in self.table.get_children():
            self.table.delete(item)

        for i in range(len(values)):
            self.table.insert("", tkinter.END, values=values[i])

    def next_page_click(self):
        self.change_page(self.current_page + 1)

    def prev_page_click(self):
        self.change_page(self.current_page - 1)

    def change_page(self, page):
        if 1 <= page <= math.ceil(self.application.train_trips_dao.get_rows_count_by_filter(self.filter_criteria) / self.page_size):
            self.current_page = page
            self.current_page_combobox.set(self.current_page)
            self.update_train_trips_table()

    def change_page_size(self, size):
        self.page_size = size
        self.update_train_trips_table()
        self.change_page(1)
