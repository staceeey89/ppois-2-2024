import tkinter as tk
from tkinter import messagebox
from typing import Tuple

from Person import Person
from Schedule import Schedule
from Station import Station
from Ticket import Ticket
from Train import Train
from Turnstile import Turnstile


class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.people: list = []
        self.title("Управление вокзалом")
        self.geometry("400x300")

        self.turnstile, self.schedule, self.ticket = self.create_initial_state()

        ticket_label_text = f"Стоимость билета: {self.ticket.price}"
        self.ticket_label = tk.Label(self, text=ticket_label_text)
        self.ticket_label.pack()

        for element in self.schedule.trains:
            train_station_text = f"Поезд {element.number} на станции: {element.station.station_name}"
            self.train_station_label = tk.Label(self, text=train_station_text)
            self.train_station_label.pack()

        self.create_person_button = tk.Button(self, text="Создать человека", command=self.open_create_person_window)
        self.create_person_button.pack()

        self.show_people_button = tk.Button(self, text="Показать всех людей", command=self.show_people)
        self.show_people_button.pack()

    def open_create_person_window(self):
        create_person_window = CreatePersonWindow(self, self.add_person)

    def create_initial_state(self) -> Tuple[Turnstile, Schedule, Ticket]:
        turnstile: Turnstile = Turnstile()
        schedule: Schedule = Schedule()
        station_a: Station = Station(Station.StationName.STATION_A.value)
        station_b: Station = Station(Station.StationName.STATION_B.value)
        station_c: Station = Station(Station.StationName.STATION_C.value)
        station_service: Station = Station(Station.StationName.STATION_SERVICE.value)
        schedule.add_station(station_a)
        schedule.add_station(station_b)
        schedule.add_station(station_c)
        schedule.add_station(station_service)
        ticket_price: float = 10
        ticket: Ticket = Ticket(ticket_price)
        train: Train = Train("1", station_service)
        schedule.add_train(train)
        return turnstile, schedule, ticket

    def show_people(self):
        people_info = self.get_people_info()
        messagebox.showinfo("Все люди", people_info)

    def get_people_info(self) -> str:
        people_info = "Список людей:\n"
        for person in self.people:
            people_info += f"Имя: {person.name}, Деньги: {person.money}, Платформа: {person.platform}, Билет: {person.ticket}\n"
        return people_info

    def show_people_on_platform(self):
        pass

    def get_people_platform_info(self) -> str:
        people_info = "Список на платформах людей:\n"
        for station in self.schedule.stations:
            for person in station.platform.persons:
                people_info += f"Имя: {person.name}, Деньги: {person.money}\n"
        return people_info

    def station_selection(self) -> Station:
        pass

    def add_person(self, person: Person):
        self.people.append(person)


class CreatePersonWindow(tk.Toplevel):
    def __init__(self, master, add_person_func):
        super().__init__(master)
        self.title("Создать человека")
        self.geometry("300x150")
        self.add_person_func = add_person_func

        self.name_label = tk.Label(self, text="Имя:")
        self.name_label.pack()
        self.name_entry = tk.Entry(self)
        self.name_entry.pack()

        self.money_label = tk.Label(self, text="Деньги:")
        self.money_label.pack()
        self.money_entry = tk.Entry(self)
        self.money_entry.pack()

        self.submit_button = tk.Button(self, text="Создать", command=self.create_person)
        self.submit_button.pack()

    def create_person(self):
        name = self.name_entry.get()
        money = self.money_entry.get()
        try:
            money = float(money)
        except ValueError:
            messagebox.showerror("Ошибка", "Некорректное значение для денег")
            return

        person = Person(name, money)
        self.add_person_func(person)
        messagebox.showinfo("Успех!", "Создание прошло успешно!")
        self.destroy()


if __name__ == "__main__":
    app = Application()
    app.mainloop()
