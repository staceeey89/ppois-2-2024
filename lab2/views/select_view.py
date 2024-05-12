import tkinter
from tkinter import ttk
import tkinter.messagebox

import views.window_operations
from models.filter_criteria import FilterCriteria
from views.select_result_view import SelectResultWindow


class SelectWindow(tkinter.Toplevel):
    def __init__(self, master, application):
        super().__init__(master)
        self.master = master
        self.application = application
        self.title("Selecting train trips")
        views.window_operations.window_center(self, 600, 600)
        self.resizable(False, False)

        # Создание переменных для checkbuttons
        self.is_select_by_train_id = tkinter.IntVar()
        self.is_select_by_departure_datetime = tkinter.IntVar()
        self.is_select_by_arrival_datetime = tkinter.IntVar()
        self.is_select_by_departure_station = tkinter.IntVar()
        self.is_select_by_arrival_station = tkinter.IntVar()
        self.is_select_by_travel_time = tkinter.IntVar()

        # Создание фреймов для каждого типа поиска
        self.select_by_train_id_frame = tkinter.LabelFrame(self, text="По номеру поезда", borderwidth=1, relief=tkinter.SOLID, width=500, height=80)
        self.select_by_departure_datetime_frame = tkinter.LabelFrame(self, borderwidth=1, text="По промежутку времени отправления", relief=tkinter.SOLID, width=500, height=80)
        self.select_by_arrival_datetime_frame = tkinter.LabelFrame(self, borderwidth=1, text="По промежутку времени прибытия", relief=tkinter.SOLID, width=500, height=80)
        self.select_by_departure_station_frame = tkinter.LabelFrame(self, borderwidth=1, text="По станции отправления", relief=tkinter.SOLID, width=500, height=80)
        self.select_by_arrival_station_frame = tkinter.LabelFrame(self, borderwidth=1, text="По станции прибытия", relief=tkinter.SOLID, width=500, height=80)
        self.select_by_travel_time_frame = tkinter.LabelFrame(self, borderwidth=1, text="По промежутку времени в пути", relief=tkinter.SOLID, width=500, height=80)

        # Создание checkbuttons для каждого типа поиска
        self.select_by_train_id_checkbutton = ttk.Checkbutton(self.select_by_train_id_frame, variable=self.is_select_by_train_id)
        self.select_by_departure_datetime_checkbutton = ttk.Checkbutton(self.select_by_departure_datetime_frame, variable=self.is_select_by_departure_datetime)
        self.select_by_arrival_datetime_checkbutton = ttk.Checkbutton(self.select_by_arrival_datetime_frame, variable=self.is_select_by_arrival_datetime)
        self.select_by_departure_station_checkbutton = ttk.Checkbutton(self.select_by_departure_station_frame, variable=self.is_select_by_departure_station)
        self.select_by_arrival_station_checkbutton = ttk.Checkbutton(self.select_by_arrival_station_frame, variable=self.is_select_by_arrival_station)
        self.select_by_travel_time_checkbutton = ttk.Checkbutton(self.select_by_travel_time_frame, variable=self.is_select_by_travel_time)

        # Создание полей ввода для каждого типа поиска
        station_values = [station[1] for station in self.application.stations_dao.get_all()]

        self.select_by_train_id_label = ttk.Label(self.select_by_train_id_frame, text="Номер поезда")
        self.select_by_train_id_entry = ttk.Entry(self.select_by_train_id_frame)

        self.select_by_departure_datetime_start_label = ttk.Label(self.select_by_departure_datetime_frame, text="От")
        self.select_by_departure_datetime_finish_label = ttk.Label(self.select_by_departure_datetime_frame, text="До")
        self.select_by_departure_datetime_start_entry = ttk.Entry(self.select_by_departure_datetime_frame)
        self.select_by_departure_datetime_finish_entry = ttk.Entry(self.select_by_departure_datetime_frame)

        self.select_by_arrival_datetime_start_label = ttk.Label(self.select_by_arrival_datetime_frame, text="От")
        self.select_by_arrival_datetime_finish_label = ttk.Label(self.select_by_arrival_datetime_frame, text="До")
        self.select_by_arrival_datetime_start_entry = ttk.Entry(self.select_by_arrival_datetime_frame)
        self.select_by_arrival_datetime_finish_entry = ttk.Entry(self.select_by_arrival_datetime_frame)

        self.select_by_departure_station_label = ttk.Label(self.select_by_departure_station_frame, text="Станция отправления")
        self.select_by_departure_station_combobox = ttk.Combobox(self.select_by_departure_station_frame, values=station_values)

        self.select_by_arrival_station_label = ttk.Label(self.select_by_arrival_station_frame, text="Станция прибытия")
        self.select_by_arrival_station_combobox = ttk.Combobox(self.select_by_arrival_station_frame, values=station_values)

        self.select_by_travel_time_start_label = ttk.Label(self.select_by_travel_time_frame, text="От")
        self.select_by_travel_time_finish_label = ttk.Label(self.select_by_travel_time_frame, text="До")
        self.select_by_travel_time_start_entry = ttk.Entry(self.select_by_travel_time_frame)
        self.select_by_travel_time_finish_entry = ttk.Entry(self.select_by_travel_time_frame)

        # Создание кнопки для вывода результатов
        self.select_button = ttk.Button(self, text="Найти", command=self.select_button_click)

        # Расположение виджетов в фрейме для поиска по номеру поезда
        self.select_by_train_id_checkbutton.place(x=5, y=20)
        self.select_by_train_id_label.place(x=70, y=15)
        self.select_by_train_id_entry.place(x=70+self.select_by_train_id_label.winfo_reqwidth()+10, y=13)
        views.window_operations.widget_center(self.select_by_train_id_frame, 600, 20)

        # Расположение виджетов в фрейме для поиска по промежутку времени отправления
        self.select_by_departure_datetime_checkbutton.place(x=5, y=20)
        self.select_by_departure_datetime_start_label.place(x=70, y=5)
        self.select_by_departure_datetime_start_entry.place(x=70+self.select_by_departure_datetime_start_label.winfo_reqwidth()+10)
        self.select_by_departure_datetime_finish_label.place(x=70, y=30)
        self.select_by_departure_datetime_finish_entry.place(x=70+self.select_by_departure_datetime_finish_label.winfo_reqwidth()+10, y=30)
        views.window_operations.widget_center(self.select_by_departure_datetime_frame, 600, 110)

        # Расположение виджетов в фрейме для поиска по промежутку времени прибытия
        self.select_by_arrival_datetime_checkbutton.place(x=5, y=20)
        self.select_by_arrival_datetime_start_label.place(x=70, y=5)
        self.select_by_arrival_datetime_start_entry.place(x=70+self.select_by_arrival_datetime_start_label.winfo_reqwidth()+10)
        self.select_by_arrival_datetime_finish_label.place(x=70, y=30)
        self.select_by_arrival_datetime_finish_entry.place(x=70+self.select_by_arrival_datetime_finish_label.winfo_reqwidth()+10, y=30)
        views.window_operations.widget_center(self.select_by_arrival_datetime_frame, 600, 200)

        # Расположение виджетов в фрейме для поиска по станции отправления
        self.select_by_departure_station_checkbutton.place(x=5, y=20)
        self.select_by_departure_station_label.place(x=70, y=15)
        self.select_by_departure_station_combobox.place(x=70+self.select_by_departure_station_label.winfo_reqwidth()+10, y=13)
        views.window_operations.widget_center(self.select_by_departure_station_frame, 600, 290)

        # Расположение виджетов в фрейме для поиска по станции прибытия
        self.select_by_arrival_station_checkbutton.place(x=5, y=20)
        self.select_by_arrival_station_label.place(x=70, y=15)
        self.select_by_arrival_station_combobox.place(x=70+self.select_by_arrival_station_label.winfo_reqwidth()+10, y=13)
        views.window_operations.widget_center(self.select_by_arrival_station_frame, 600, 380)

        # Расположение виджетов в фрейме для поиска по времени в пути
        self.select_by_travel_time_checkbutton.place(x=5, y=20)
        self.select_by_travel_time_start_label.place(x=70, y=5)
        self.select_by_travel_time_start_entry.place(x=70+self.select_by_travel_time_start_label.winfo_reqwidth()+10)
        self.select_by_travel_time_finish_label.place(x=70, y=30)
        self.select_by_travel_time_finish_entry.place(x=70+self.select_by_travel_time_finish_label.winfo_reqwidth()+10, y=30)
        views.window_operations.widget_center(self.select_by_travel_time_frame, 600, 470)

        # Расположение кнопки для просмотра результатов
        views.window_operations.widget_center(self.select_button, 600, 560)

    def select_button_click(self):
        filter_criteria_dict = {
            "train_id": None,
            "departure_station": None,
            "arrival_station": None,
            "departure_datetime_start": None,
            "departure_datetime_finish": None,
            "arrival_datetime_start": None,
            "arrival_datetime_finish": None,
            "travel_time_start": None,
            "travel_time_finish": None
        }
        if self.is_select_by_train_id.get() == 1:
            filter_criteria_dict["train_id"] = int(self.select_by_train_id_entry.get())

        if self.is_select_by_departure_datetime.get() == 1:
            filter_criteria_dict["departure_datetime_start"] = self.select_by_departure_datetime_start_entry.get()
            filter_criteria_dict["departure_datetime_finish"] = self.select_by_departure_datetime_finish_entry.get()

        if self.is_select_by_arrival_datetime.get() == 1:
            filter_criteria_dict["arrival_datetime_start"] = self.select_by_arrival_datetime_start_entry.get()
            filter_criteria_dict["arrival_datetime_finish"] = self.select_by_arrival_datetime_finish_entry.get()

        if self.is_select_by_departure_station.get() == 1:
            filter_criteria_dict["departure_station"] = self.select_by_departure_station_combobox.get()

        if self.is_select_by_arrival_station.get() == 1:
            filter_criteria_dict["arrival_station"] = self.select_by_arrival_station_combobox.get()

        if self.is_select_by_travel_time.get() == 1:
            filter_criteria_dict["travel_time_start"] = self.select_by_travel_time_start_entry.get()
            filter_criteria_dict["travel_time_finish"] = self.select_by_travel_time_finish_entry.get()

        filter_criteria = FilterCriteria(**filter_criteria_dict)
        self.destroy()
        SelectResultWindow(self.master, self.application, filter_criteria)
