import tkinter as tk
from tkinter import messagebox, simpledialog
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

        self.ticket_label_text = f"Стоимость билета: {self.ticket.price}"
        self.ticket_label = tk.Label(self, text=self.ticket_label_text)
        self.ticket_label.pack()

        for element in self.schedule.trains:
            self.train_station_text = f"Поезд {element.number} на станции: {element.station.station_name}"
            self.train_station_label = tk.Label(self, text=self.train_station_text)
            self.train_station_label.pack()

        self.create_person_button = tk.Button(self, text="Создать человека", command=self.open_create_person_window)
        self.create_person_button.pack()

        self.show_people_button = tk.Button(self, text="Показать всех людей", command=self.show_people)
        self.show_people_button.pack()

        self.change_ticket_price_button = tk.Button(self, text="Изменить стоимость билета",
                                                    command=self.change_ticket_price)
        self.change_ticket_price_button.pack()

        self.buy_tickets_button = tk.Button(self, text="Купить билеты", command=self.buy_tickets)
        self.buy_tickets_button.pack()

        self.move_train_button = tk.Button(self, text="Пустить поезд", command=self.move_train)
        self.move_train_button.pack()

        self.platforms_button = tk.Button(self, text="Информация о платформах", command=self.show_platforms_info)
        self.platforms_button.pack()

    def open_create_person_window(self):
        CreatePersonWindow(self, self.add_person)

    def move_train(self):
        for element in self.schedule.trains:
            self.schedule.move_train()
            self.train_station_text = f"Поезд {element.number} на станции: {element.station.station_name}"
            self.train_station_label.config(text=self.train_station_text)

    def change_ticket_price(self):
        new_price = simpledialog.askfloat("Изменение стоимости билета", "Введите новую стоимость билета:")
        if new_price < 0:
            messagebox.showerror("Ошибка!", "Стоимость билета должна быть выше 0!")
            return
        if new_price is not None:
            self.ticket.price = new_price
            self.ticket_label_text = f"Стоимость билета: {self.ticket.price}"
            self.ticket_label.config(text=self.ticket_label_text)

    def buy_tickets(self):
        for person in self.people:
            if person.ticket is None:
                person.buy_ticket(self.ticket)
                person.enter_platform(self.schedule.stations[0].platform, self.turnstile)
        messagebox.showinfo("Билеты куплены", "Билеты успешно куплены!")

    def create_initial_state(self) -> Tuple[Turnstile, Schedule, Ticket]:
        turnstile: Turnstile = Turnstile()
        schedule: Schedule = Schedule()
        station_a: Station = Station(Station.StationName.STATION_A.value)
        station_b: Station = Station(Station.StationName.STATION_B.value)
        station_c: Station = Station(Station.StationName.STATION_C.value)
        schedule.add_station(station_a)
        schedule.add_station(station_b)
        schedule.add_station(station_c)
        ticket_price: float = 10
        ticket: Ticket = Ticket(ticket_price)
        train: Train = Train("1", station_a)
        schedule.add_train(train)
        return turnstile, schedule, ticket

    def show_people(self):
        people_info = self.get_people_info()
        messagebox.showinfo("Все люди", people_info)

    def get_people_info(self) -> str:
        people_info = "Список людей:\n"
        for person in self.people:
            if person.ticket is None:
                platform_name = None
                ticket_name = None
            else:
                platform_name = person.platform.name
                ticket_name = person.ticket.name
            people_info += (f"Имя: {person.name}, Деньги: {person.money}, Платформа: {platform_name}, "
                            f"Билет: {ticket_name}\n")
        return people_info

    def show_platforms_info(self):
        platforms_info = "Информация о платформах:\n"
        for station in self.schedule.stations:
            people_count = len(station.platform.persons)
            platforms_info += f"Платформа {station.platform.name}: Количество людей - {people_count}\n"
        messagebox.showinfo("Платформы", platforms_info)

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
