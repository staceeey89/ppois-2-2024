import tkinter
import tkinter.messagebox
from tkinter import ttk
import datetime

from models.train import Train
from models.station import Station
from models.train_trip import TrainTrip
import views.window_operations
from models.source_type import SourceType


class AddingWindow(tkinter.Toplevel):
    def __init__(self, master, application):
        super().__init__(master=master)
        self.application = application
        self.title("Adding train trip")
        views.window_operations.window_center(self, 350, 350)
        self.resizable(False, False)

        train_values = [train[1] for train in self.application.trains_dao.get_all()]
        station_values = [station[1] for station in self.application.stations_dao.get_all()]

        self.train_label = ttk.Label(self, text="Поезд")
        self.departure_station_label = ttk.Label(self, text="Станция отправления")
        self.arrival_station_label = ttk.Label(self, text="Станция прибытия")
        self.departure_datetime_label = ttk.Label(self, text="Время отправления")
        self.arrival_datetime_label = ttk.Label(self, text="Время прибытия")
        self.train_combobox = ttk.Combobox(self, values=train_values)
        self.departure_station_combobox = ttk.Combobox(self, values=station_values)
        self.arrival_station_combobox = ttk.Combobox(self, values=station_values)
        self.departure_datetime_entry = ttk.Entry(self)
        self.arrival_datetime_entry = ttk.Entry(self)
        self.add_button = ttk.Button(self, text="Добавить", command=self.add_train_trip)

        self.train_label.place(x=80, y=10)
        self.train_combobox.place(x=80, y=30)
        self.departure_station_label.place(x=80, y=70)
        self.departure_station_combobox.place(x=80, y=90)
        self.arrival_station_label.place(x=80, y=130)
        self.arrival_station_combobox.place(x=80, y=150)
        self.departure_datetime_label.place(x=80, y=190)
        self.departure_datetime_entry.place(x=80, y=210)
        self.arrival_datetime_label.place(x=80, y=250)
        self.arrival_datetime_entry.place(x=80, y=270)
        self.add_button.place(x=120, y=310)

    def add_train_trip(self):
        train = Train(self.train_combobox.get())
        departure_station = Station(self.departure_station_combobox.get())
        arrival_station = Station(self.arrival_station_combobox.get())
        departure_datetime = datetime.datetime.strptime(self.departure_datetime_entry.get(), "%Y-%m-%d %H:%M:%S")
        arrival_datetime = datetime.datetime.strptime(self.arrival_datetime_entry.get(), "%Y-%m-%d %H:%M:%S")
        if departure_datetime > arrival_datetime:
            tkinter.messagebox.showinfo(message="Прибытие не может быть раньше отправления.")
            return
        train_trip = TrainTrip(train, departure_station, arrival_station, departure_datetime, arrival_datetime)

        if self.application.source_type == SourceType.database:
            self.application.train_trips_dao.insert(train_trip)
        else:
            self.application.xml_parser.add_train_trip(train_trip)

        self.application.update_train_trips_table()
        tkinter.messagebox.showinfo(message="Поездка успешно добавлена!")
        self.destroy()
