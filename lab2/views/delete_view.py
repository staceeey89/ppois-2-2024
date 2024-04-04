import tkinter
from tkinter import ttk
import tkinter.messagebox

import views.window_operations
import controllers.DAO
from models.filter_criteria import FilterCriteria
from models.source_type import SourceType


class DeleteWindow(tkinter.Toplevel):
    def __init__(self, master, application):
        super().__init__(master)
        self.master = master
        self.application = application
        self.title("Deleting train trips")
        views.window_operations.window_center(self, 600, 600)
        self.resizable(False, False)
        self.station_dao = controllers.DAO.StationDAO()

        # Создание переменных для checkbuttons
        self.is_delete_by_train_id = tkinter.IntVar()
        self.is_delete_by_departure_datetime = tkinter.IntVar()
        self.is_delete_by_arrival_datetime = tkinter.IntVar()
        self.is_delete_by_departure_station = tkinter.IntVar()
        self.is_delete_by_arrival_station = tkinter.IntVar()
        self.is_delete_by_travel_time = tkinter.IntVar()

        # Создание фреймов для каждого типа удаления
        self.delete_by_train_id_frame = tkinter.LabelFrame(self, text="По номеру поезда", borderwidth=1, relief=tkinter.SOLID, width=500, height=80)
        self.delete_by_departure_datetime_frame = tkinter.LabelFrame(self, borderwidth=1, text="По промежутку времени отправления", relief=tkinter.SOLID, width=500, height=80)
        self.delete_by_arrival_datetime_frame = tkinter.LabelFrame(self, borderwidth=1, text="По промежутку времени прибытия", relief=tkinter.SOLID, width=500, height=80)
        self.delete_by_departure_station_frame = tkinter.LabelFrame(self, borderwidth=1, text="По станции отправления", relief=tkinter.SOLID, width=500, height=80)
        self.delete_by_arrival_station_frame = tkinter.LabelFrame(self, borderwidth=1, text="По станции прибытия", relief=tkinter.SOLID, width=500, height=80)
        self.delete_by_travel_time_frame = tkinter.LabelFrame(self, borderwidth=1, text="По промежутку времени в пути", relief=tkinter.SOLID, width=500, height=80)

        # Создание checkbuttons для каждого типа удаления
        self.delete_by_train_id_checkbutton = ttk.Checkbutton(self.delete_by_train_id_frame, variable=self.is_delete_by_train_id)
        self.delete_by_departure_datetime_checkbutton = ttk.Checkbutton(self.delete_by_departure_datetime_frame, variable=self.is_delete_by_departure_datetime)
        self.delete_by_arrival_datetime_checkbutton = ttk.Checkbutton(self.delete_by_arrival_datetime_frame, variable=self.is_delete_by_arrival_datetime)
        self.delete_by_departure_station_checkbutton = ttk.Checkbutton(self.delete_by_departure_station_frame, variable=self.is_delete_by_departure_station)
        self.delete_by_arrival_station_checkbutton = ttk.Checkbutton(self.delete_by_arrival_station_frame, variable=self.is_delete_by_arrival_station)
        self.delete_by_travel_time_checkbutton = ttk.Checkbutton(self.delete_by_travel_time_frame, variable=self.is_delete_by_travel_time)

        # Создание полей ввода для каждого типа удаления
        station_values = [station[1] for station in self.station_dao.get_all()]

        self.delete_by_train_id_label = ttk.Label(self.delete_by_train_id_frame, text="Номер поезда")
        self.delete_by_train_id_entry = ttk.Entry(self.delete_by_train_id_frame)

        self.delete_by_departure_datetime_start_label = ttk.Label(self.delete_by_departure_datetime_frame, text="От")
        self.delete_by_departure_datetime_finish_label = ttk.Label(self.delete_by_departure_datetime_frame, text="До")
        self.delete_by_departure_datetime_start_entry = ttk.Entry(self.delete_by_departure_datetime_frame)
        self.delete_by_departure_datetime_finish_entry = ttk.Entry(self.delete_by_departure_datetime_frame)

        self.delete_by_arrival_datetime_start_label = ttk.Label(self.delete_by_arrival_datetime_frame, text="От")
        self.delete_by_arrival_datetime_finish_label = ttk.Label(self.delete_by_arrival_datetime_frame, text="До")
        self.delete_by_arrival_datetime_start_entry = ttk.Entry(self.delete_by_arrival_datetime_frame)
        self.delete_by_arrival_datetime_finish_entry = ttk.Entry(self.delete_by_arrival_datetime_frame)

        self.delete_by_departure_station_label = ttk.Label(self.delete_by_departure_station_frame, text="Станция отправления")
        self.delete_by_departure_station_combobox = ttk.Combobox(self.delete_by_departure_station_frame, values=station_values)

        self.delete_by_arrival_station_label = ttk.Label(self.delete_by_arrival_station_frame, text="Станция прибытия")
        self.delete_by_arrival_station_combobox = ttk.Combobox(self.delete_by_arrival_station_frame, values=station_values)

        self.delete_by_travel_time_start_label = ttk.Label(self.delete_by_travel_time_frame, text="От")
        self.delete_by_travel_time_finish_label = ttk.Label(self.delete_by_travel_time_frame, text="До")
        self.delete_by_travel_time_start_entry = ttk.Entry(self.delete_by_travel_time_frame)
        self.delete_by_travel_time_finish_entry = ttk.Entry(self.delete_by_travel_time_frame)

        # Создание кнопки для удаления
        self.delete_button = ttk.Button(self, text="Удалить", command=self.delete_button_click)

        # Расположение виджетов в фрейме для удаления по номеру поезда
        self.delete_by_train_id_checkbutton.place(x=5, y=20)
        self.delete_by_train_id_label.place(x=70, y=15)
        self.delete_by_train_id_entry.place(x=70+self.delete_by_train_id_label.winfo_reqwidth()+10, y=13)
        views.window_operations.widget_center(self.delete_by_train_id_frame, 600, 20)

        # Расположение виджетов в фрейме для удаления по промежутку времени отправления
        self.delete_by_departure_datetime_checkbutton.place(x=5, y=20)
        self.delete_by_departure_datetime_start_label.place(x=70, y=5)
        self.delete_by_departure_datetime_start_entry.place(x=70+self.delete_by_departure_datetime_start_label.winfo_reqwidth()+10)
        self.delete_by_departure_datetime_finish_label.place(x=70, y=30)
        self.delete_by_departure_datetime_finish_entry.place(x=70+self.delete_by_departure_datetime_finish_label.winfo_reqwidth()+10, y=30)
        views.window_operations.widget_center(self.delete_by_departure_datetime_frame, 600, 110)

        # Расположение виджетов в фрейме для удаления по промежутку времени прибытия
        self.delete_by_arrival_datetime_checkbutton.place(x=5, y=20)
        self.delete_by_arrival_datetime_start_label.place(x=70, y=5)
        self.delete_by_arrival_datetime_start_entry.place(x=70+self.delete_by_arrival_datetime_start_label.winfo_reqwidth()+10)
        self.delete_by_arrival_datetime_finish_label.place(x=70, y=30)
        self.delete_by_arrival_datetime_finish_entry.place(x=70+self.delete_by_arrival_datetime_finish_label.winfo_reqwidth()+10, y=30)
        views.window_operations.widget_center(self.delete_by_arrival_datetime_frame, 600, 200)

        # Расположение виджетов в фрейме для удаления по станции отправления
        self.delete_by_departure_station_checkbutton.place(x=5, y=20)
        self.delete_by_departure_station_label.place(x=70, y=15)
        self.delete_by_departure_station_combobox.place(x=70+self.delete_by_departure_station_label.winfo_reqwidth()+10, y=13)
        views.window_operations.widget_center(self.delete_by_departure_station_frame, 600, 290)

        # Расположение виджетов в фрейме для удаления по станции прибытия
        self.delete_by_arrival_station_checkbutton.place(x=5, y=20)
        self.delete_by_arrival_station_label.place(x=70, y=15)
        self.delete_by_arrival_station_combobox.place(x=70+self.delete_by_arrival_station_label.winfo_reqwidth()+10, y=13)
        views.window_operations.widget_center(self.delete_by_arrival_station_frame, 600, 380)

        # Расположение виджетов в фрейме для удаления по времени в пути
        self.delete_by_travel_time_checkbutton.place(x=5, y=20)
        self.delete_by_travel_time_start_label.place(x=70, y=5)
        self.delete_by_travel_time_start_entry.place(x=70+self.delete_by_travel_time_start_label.winfo_reqwidth()+10)
        self.delete_by_travel_time_finish_label.place(x=70, y=30)
        self.delete_by_travel_time_finish_entry.place(x=70+self.delete_by_travel_time_finish_label.winfo_reqwidth()+10, y=30)
        views.window_operations.widget_center(self.delete_by_travel_time_frame, 600, 470)

        # Расположение кнопки для удаления
        views.window_operations.widget_center(self.delete_button, 600, 560)

    def delete_button_click(self):
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
        if self.is_delete_by_train_id.get() == 1:
            filter_criteria_dict["train_id"] = int(self.delete_by_train_id_entry.get())

        if self.is_delete_by_departure_datetime.get() == 1:
            filter_criteria_dict["departure_datetime_start"] = self.delete_by_departure_datetime_start_entry.get()
            filter_criteria_dict["departure_datetime_finish"] = self.delete_by_departure_datetime_finish_entry.get()

        if self.is_delete_by_arrival_datetime.get() == 1:
            filter_criteria_dict["arrival_datetime_start"] = self.delete_by_arrival_datetime_start_entry.get()
            filter_criteria_dict["arrival_datetime_finish"] = self.delete_by_arrival_datetime_finish_entry.get()

        if self.is_delete_by_departure_station.get() == 1:
            filter_criteria_dict["departure_station"] = self.delete_by_departure_station_combobox.get()

        if self.is_delete_by_arrival_station.get() == 1:
            filter_criteria_dict["arrival_station"] = self.delete_by_arrival_station_combobox.get()

        if self.is_delete_by_travel_time.get() == 1:
            filter_criteria_dict["travel_time_start"] = self.delete_by_travel_time_start_entry.get()
            filter_criteria_dict["travel_time_finish"] = self.delete_by_travel_time_finish_entry.get()

        filter_criteria = FilterCriteria(**filter_criteria_dict)

        if self.application.source_type == SourceType.database:
            deleted_rows_count = self.application.train_trips_dao.delete_by_filter(filter_criteria)
        else:
            deleted_rows_count = self.application.xml_parser.delete_by_filter(filter_criteria)

        if deleted_rows_count > 0:
            tkinter.messagebox.showinfo(message="Было удалено %s строк" % deleted_rows_count)
        else:
            tkinter.messagebox.showinfo(message="Строки не были удалены")
        if self.application.is_treeview.get() == 1:
            self.application.update_train_trips_treeview()
        else:
            self.application.update_train_trips_table()
        self.destroy()



