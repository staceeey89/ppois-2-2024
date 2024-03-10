from tkinter import *
import xml.sax
import xml.dom.minidom
from tkinter import messagebox, ttk, Frame
from datetime import datetime


class TrainHandler(xml.sax.ContentHandler):
    def __init__(self):
        self.trains = []
        self.departures = []
        self.arrivals = []
        self.current_train = None
        self.current_station = None
        self.current_datetime = None
        self.departure_time = None
        self.arrival_time = None

    def startElement(self, name, attrs):
        if name == "train":
            self.current_train = {'id': attrs['id']}
        elif name == "departure":
            self.departure = {'train_id': self.current_train['id']}
        elif name == "arrival":
            self.arrival = {'train_id': self.current_train['id']}
        elif name == "station":
            self.current_station = True
        elif name == "datetime":
            self.current_datetime = True

    def characters(self, content):
        if self.current_station:
            if hasattr(self, 'departure'):
                self.departure['station'] = content
            elif hasattr(self, 'arrival'):
                self.arrival['station'] = content
            self.current_train['station'] = content
            self.current_station = False
        elif self.current_datetime:
            if hasattr(self, 'departure'):
                self.departure['datetime'] = content
                self.departure_time = datetime.strptime(content, "%Y-%m-%dT%H:%M:%S")
            elif hasattr(self, 'arrival'):
                self.arrival['datetime'] = content
                self.arrival_time = datetime.strptime(content, "%Y-%m-%dT%H:%M:%S")
            self.current_train['datetime'] = content
            self.current_datetime = False

    def endElement(self, name):
        if name == "train":
            self.trains.append(self.current_train)
        elif name == "departure":
            self.departures.append(self.departure)
            delattr(self, 'departure')
            self.departure_time = None
        elif name == "arrival":
            self.arrivals.append(self.arrival)
            delattr(self, 'arrival')
            self.arrival_time = None
        self.current = ""


def parse_xml():
    handler = TrainHandler()
    parser = xml.sax.make_parser()
    parser.setContentHandler(handler)
    parser.parse('trip.xml')
    return handler.departures, handler.arrivals


def show_train_data(root):
    departures, arrivals = parse_xml()

    window = Toplevel(root)
    window.title('Информация о поезде')
    window.geometry('800x500')

    trains_per_page = 2
    current_page = 0
    total_pages = -(-len(departures) // trains_per_page)

    def show_page(page):
        nonlocal current_page
        current_page = page
        for widget in window.winfo_children():
            widget.destroy()

        page_departures = departures[current_page * trains_per_page: (current_page + 1) * trains_per_page]
        page_arrivals = arrivals[current_page * trains_per_page: (current_page + 1) * trains_per_page]

        for train_id, (departure, arrival) in enumerate(zip(page_departures, page_arrivals), start=current_page * trains_per_page + 1):
            train_label = Label(window, text=f'Train {train_id} info:', font=('Arial', 14, 'bold'))
            train_label.pack()
            departure_label = Label(window, text='Departure', font=('Arial', 14, 'bold'))
            departure_label.pack()

            departure_station = departure['station']
            departure_datetime = departure['datetime']
            departure_label_text = f'Station: {departure_station}, Datetime: {departure_datetime}'
            departure_label = Label(window, text=departure_label_text)
            departure_label.pack()

            arrival_label = Label(window, text='Arrival', font=('Arial', 14, 'bold'))
            arrival_label.pack()

            arrival_station = arrival['station']
            arrival_datetime = arrival['datetime']
            arrival_label_text = f'Station: {arrival_station}, Datetime: {arrival_datetime}'
            arrival_label = Label(window, text=arrival_label_text)
            arrival_label.pack()

            departure_time = datetime.strptime(departure_datetime, "%Y-%m-%dT%H:%M:%S")
            arrival_time = datetime.strptime(arrival_datetime, "%Y-%m-%dT%H:%M:%S")
            travel_time = str(arrival_time - departure_time)
            travel_time_label = Label(window, text=f'Travel Time: {travel_time}', font=('Arial', 14, 'bold'))
            travel_time_label.pack()


        page_label = Label(window, text=f'Страница: {page + 1}/{total_pages}')
        page_label.pack(side=BOTTOM)

        if page == 0:
            next_page_btn = Button(window, text="Следующая страница", command=lambda: show_page(page + 1))
            next_page_btn.pack(side='bottom', pady=(10, 0))
        elif 0 < page < total_pages - 1:
            prev_page_btn = Button(window, text="Предыдущая страница", command=lambda: show_page(page - 1))
            prev_page_btn.pack(side='bottom', pady=(10, 0))
            next_page_btn = Button(window, text="Следующая страница", command=lambda: show_page(page + 1))
            next_page_btn.pack(side='bottom', pady=(10, 0))
        elif page == total_pages - 1:
            prev_page_btn = Button(window, text="Предыдущая страница", command=lambda: show_page(page - 1))
            prev_page_btn.pack(side='bottom', pady=(10, 0))

        if total_pages > 1:
            first_page_btn = Button(window, text="Первая страница", command=lambda: show_page(0))
            first_page_btn.pack(side='top', pady=(0, 10))
            last_page_btn = Button(window, text="Последняя страница", command=lambda: show_page(total_pages - 1))
            last_page_btn.pack(side='top', pady=(0, 10))

    show_page(current_page)



def write_in_file(root):
    def submit_data():
        idd = IdField.get()
        departure_station = DepartureStationField.get()
        departure_datetime = DepartureDatetimeField.get()
        arrival_station = ArrivalStationField.get()
        arrival_datetime = ArrivalDatetimeField.get()

        if not idd.isdigit():
            messagebox.showerror("Ошибка", "Номер поезда должен быть целым числом!")
            return

        try:
            departure_time = datetime.strptime(departure_datetime, "%Y-%m-%dT%H:%M:%S")
        except ValueError:
            messagebox.showerror("Ошибка", "Неправильный формат даты и времени отправления!")
            return

        try:
            arrival_time = datetime.strptime(arrival_datetime, "%Y-%m-%dT%H:%M:%S")
        except ValueError:
            messagebox.showerror("Ошибка", "Неправильный формат даты и времени прибытия!")
            return

        if arrival_time <= departure_time:
            messagebox.showerror("Ошибка", "Дата и время прибытия должны быть позже даты и времени отправления!")
            return

        domtree = xml.dom.minidom.parse('trip.xml')
        trip = domtree.documentElement
        new_train = domtree.createElement('train')
        new_train.setAttribute('id', idd)
        new_departure = domtree.createElement("departure")
        new_arrival = domtree.createElement("arrival")

        new_departure_station = domtree.createElement("station")
        new_departure_station.appendChild(domtree.createTextNode(departure_station))
        new_departure_datetime = domtree.createElement("datetime")
        new_departure_datetime.appendChild(domtree.createTextNode(departure_datetime))
        new_departure.appendChild(new_departure_station)
        new_departure.appendChild(new_departure_datetime)

        new_arrival_station = domtree.createElement("station")
        new_arrival_station.appendChild(domtree.createTextNode(arrival_station))
        new_arrival_datetime = domtree.createElement("datetime")
        new_arrival_datetime.appendChild(domtree.createTextNode(arrival_datetime))
        new_arrival.appendChild(new_arrival_station)
        new_arrival.appendChild(new_arrival_datetime)

        new_train.appendChild(new_departure)
        new_train.appendChild(new_arrival)

        departure_time = datetime.strptime(departure_datetime, "%Y-%m-%dT%H:%M:%S")
        arrival_time = datetime.strptime(arrival_datetime, "%Y-%m-%dT%H:%M:%S")
        travel_time = str(arrival_time - departure_time)

        new_travel_time = domtree.createElement("travel_time")
        new_travel_time.appendChild(domtree.createTextNode(travel_time))
        new_train.appendChild(new_travel_time)

        trip.appendChild(new_train)
        domtree.writexml(open('trip.xml', 'w'))
        window.destroy()

    window = Toplevel(root)
    window.title('Информация о поезде')
    window.geometry('800x500')
    frame = Frame(window, borderwidth=1, relief=SOLID, padx = 5, pady = 5)
    name_label = Label(frame, text="Введите номер поезда")
    name_label.pack(anchor=NW)
    IdField = Entry(frame)
    IdField.pack()
    frame.pack(anchor=NW, fill=X, padx=5, pady=5)

    frame2 = Frame(window, borderwidth=1, relief=SOLID, padx=5, pady=5)
    name_label2 = Label(frame2, text="Введите станцию отправления")
    name_label2.pack(anchor=NW)
    DepartureStationField = Entry(frame2)
    DepartureStationField.pack()
    frame2.pack(anchor=NW, fill=X, padx=5, pady=5)

    frame3 = Frame(window, borderwidth=1, relief=SOLID, padx=5, pady=5)
    name_label3 = Label(frame3, text="Введите дату и время отправления (YYYY-MM-DDTHH:MM:SS)")
    name_label3.pack(anchor=NW)
    DepartureDatetimeField = Entry(frame3)
    DepartureDatetimeField.pack()
    frame3.pack(anchor=NW, fill=X, padx=5, pady=5)

    frame4 = Frame(window, borderwidth=1, relief=SOLID, padx=5, pady=5)
    name_label4 = Label(frame4, text="Введите станция прибытия")
    name_label4.pack(anchor=NW)
    ArrivalStationField = Entry(frame4)
    ArrivalStationField.pack()
    frame4.pack(anchor=NW, fill=X, padx=5, pady=5)

    frame5 = Frame(window, borderwidth=1, relief=SOLID, padx=5, pady=5)
    name_label5 = Label(frame5, text="Введите дату и время прибытия (YYYY-MM-DDTHH:MM:SS)")
    name_label5.pack(anchor=NW)
    ArrivalDatetimeField = Entry(frame5)
    ArrivalDatetimeField.pack()
    frame5.pack(anchor=NW, fill=X, padx=5, pady=5)

    submit_btn = Button(window, text="ОК", command=submit_data)
    submit_btn.pack()

def Search_Info(root):
    def print_info():
        count = False
        count2 = False
        id = IdField.get()
        departures, arrivals = parse_xml()

        for departure in departures:
            if id == departure['train_id']:
                count = True
                break

        for arrival in arrivals:
            if id == arrival['train_id']:
                count2 = True
                break

        window2 = Toplevel(window)
        window2.title('Результат')
        window2.geometry('800x500')
        if count:
            train_label = Label(window2, text=f'Train with number {id} is found!')
        else:
            train_label = Label(window2, text='No Train with such number!')
        train_label.pack()
        train2_label = Label(window2, text=f'Train {id} info:', font=('Arial', 14, 'bold'))
        train2_label.pack()
        departure2_label = Label(window2, text='Departure', font=('Arial', 14, 'bold'))
        departure2_label.pack()
        for id in range(1, len(departures) + 1):
              if count == True:
                station = departure['station']
                datetime = departure['datetime']
                label_text = f'Station: {station}, Datetime: {datetime}'
                label = Label(window2, text=label_text)
                label.pack()
                break

        arrival2_label = Label(window2, text='Arrival', font=('Arial', 14, 'bold'))
        arrival2_label.pack()
        for id in range(1, len(arrivals) + 1):
            if count2 == True:
                station = arrival['station']
                datetime = arrival['datetime']
                label_text = f'Station: {station}, Datetime: {datetime}'
                label = Label(window2, text=label_text)
                label.pack()
                break

    def search_by_date():
        date = DepartureDateTimeField.get()
        departures, arrivals = parse_xml()

        window3 = Toplevel(window)
        window3.title('Результат поиска по дате отправления')
        window3.geometry('800x500')

        found = False

        for departure, arrival in zip(departures, arrivals):
            if date == departure['datetime']:
                found = True
                train_id = departure['train_id']
                train_label = Label(window3, text=f'Train {train_id} info:', font=('Arial', 14, 'bold'))
                train_label.pack()
                departure_label = Label(window3, text='Departure', font=('Arial', 14, 'bold'))
                departure_label.pack()
                departure_info = f'Station: {departure["station"]}, Datetime: {departure["datetime"]}'
                departure_info_label = Label(window3, text=departure_info)
                departure_info_label.pack()

                arrival_label = Label(window3, text='Arrival', font=('Arial', 14, 'bold'))
                arrival_label.pack()
                arrival_info = f'Station: {arrival["station"]}, Datetime: {arrival["datetime"]}'
                arrival_info_label = Label(window3, text=arrival_info)
                arrival_info_label.pack()

        if not found:
            not_found_label = Label(window3, text='No trains found for the given date!', font=('Arial', 14, 'bold'))
            not_found_label.pack()

    window = Toplevel(root)
    window.title('Поиск поездов')
    window.geometry('800x500')
    frame = Frame(window, borderwidth=1, relief=SOLID, padx=5, pady=5)
    name_label = Label(frame, text="Введите номер поезда")
    name_label.pack(anchor=NW)
    IdField = Entry(frame)
    IdField.pack()
    frame.pack(anchor=NW, fill=X, padx=5, pady=5)

    submit_btn = Button(window, text="ОК", command=print_info)
    submit_btn.pack()

    frame2 = Frame(window, borderwidth=1, relief=SOLID, padx=5, pady=5)
    name_label2 = Label(frame2, text="Введите дату отправления (YYYY-MM-DDTHH:MM:SS)")
    name_label2.pack(anchor=NW)
    DepartureDateTimeField = Entry(frame2)
    DepartureDateTimeField.pack()
    frame2.pack(anchor=NW, fill=X, padx=5, pady=5)

    submit_btn2 = Button(window, text="Поиск по дате", command=search_by_date)
    submit_btn2.pack()


def delete_data(root):
    def perform_deletion():
        train_id = train_id_entry.get()
        departure_date = departure_date_entry.get()

        if not train_id or not departure_date:
            messagebox.showinfo("Ошибка", "Пожалуйста, введите номер поезда и дату удаления.")
            return

        if delete_by_train_id_and_date(train_id, departure_date):
            messagebox.showinfo("Успех", f"Данные по поезду {train_id} и дате {departure_date} удалены.")
        else:
            messagebox.showinfo("Ошибка", f"Данных по поезду {train_id} и дате {departure_date} не найдено.")

        window.destroy()

    def delete_by_train_id_and_date(train_id, departure_date):
        domtree = xml.dom.minidom.parse('trip.xml')
        trip = domtree.documentElement
        departures = trip.getElementsByTagName('departure')

        for departure in departures:
            train_id_element = departure.parentNode.getAttribute('id')
            datetime_element = departure.getElementsByTagName('datetime')[0]

            if train_id_element == train_id and datetime_element.firstChild.data == departure_date:
                trip.removeChild(departure.parentNode)
                with open('trip.xml', 'w') as f:
                    domtree.writexml(f)
                return True

        return False

    window = Toplevel(root)
    window.title('Удаление информации')
    window.geometry('500x300')

    frame = Frame(window, borderwidth=1, relief=SOLID, padx=5, pady=5)
    train_id_label = Label(frame, text="Номер поезда:")
    train_id_label.pack(anchor=NW)
    train_id_entry = Entry(frame)
    train_id_entry.pack()

    departure_date_label = Label(frame, text="Дата отправления (YYYY-MM-DDTHH:MM:SS):")
    departure_date_label.pack(anchor=NW)
    departure_date_entry = Entry(frame)
    departure_date_entry.pack()

    frame.pack(anchor=NW, fill=X, padx=5, pady=5)

    submit_btn = Button(window, text="Удалить данные", command=perform_deletion)
    submit_btn.pack()

def show_train_data_table(root):
    departures, arrivals = parse_xml()

    window = Toplevel(root)
    window.title('Информация о поезде (таблица)')
    window.geometry('1200x500')

    tree = ttk.Treeview(window)
    tree["columns"] = ("departure_station", "arrival_station", "departure_datetime", "arrival_datetime", "travel_time")
    tree.heading("#0", text="Train ID")
    tree.heading("departure_station", text="Станция отправления")
    tree.heading("arrival_station", text="Станция прибытия")
    tree.heading("departure_datetime", text="Дата и время отправления")
    tree.heading("arrival_datetime", text="Дата и время прибытия")
    tree.heading("travel_time", text="Время в пути")

    for i, (departure, arrival) in enumerate(zip(departures, arrivals), start=1):
        train_id = f"Train {i}"
        departure_station = departure['station']
        departure_datetime = departure['datetime']
        arrival_station = arrival['station']
        arrival_datetime = arrival['datetime']

        departure_time = datetime.strptime(departure_datetime, "%Y-%m-%dT%H:%M:%S")
        arrival_time = datetime.strptime(arrival_datetime, "%Y-%m-%dT%H:%M:%S")
        travel_time = str(arrival_time - departure_time)

        tree.insert("", "end", text=train_id, values=(departure_station, arrival_station, departure_datetime, arrival_datetime, travel_time))

    tree.pack(expand=True, fill="both")


def show_train_data_tree(root):
    departures, arrivals = parse_xml()

    window = Toplevel(root)
    window.title('Информация о поезде (дерево)')
    window.geometry('800x500')

    tree = ttk.Treeview(window)
    tree["columns"] = ("departure", "arrival")

    trains_node = tree.insert("", "end", text="Trains")

    for i, (departure, arrival) in enumerate(zip(departures, arrivals), start=1):
        train_id = f"Train {i}"
        train_node = tree.insert(trains_node, "end", text=train_id)

        departure_node = tree.insert(train_node, "end", text="Departure")
        tree.insert(departure_node, "end", text=f"Station: {departure['station']}")
        tree.insert(departure_node, "end", text=f"DateTime: {departure['datetime']}")

        arrival_node = tree.insert(train_node, "end", text="Arrival")
        tree.insert(arrival_node, "end", text=f"Station: {arrival['station']}")
        tree.insert(arrival_node, "end", text=f"DateTime: {arrival['datetime']}")

    tree.pack(expand=True, fill="both")


def create_toolbar(root):
    toolbar_frame = ttk.Frame(root)
    toolbar_frame.pack(side="top", fill="x", anchor="nw")

    btn_show_data_table = ttk.Button(toolbar_frame, text='Просмотреть данные (таблица)', command=lambda: show_train_data_table(root))
    btn_show_data_table.pack(side="left", padx=5, pady=5)

    btn_show_data_tree = ttk.Button(toolbar_frame, text='Просмотреть данные (дерево)', command=lambda: show_train_data_tree(root))
    btn_show_data_tree.pack(side="left", padx=5, pady=5)

    btn_show_data = ttk.Button(toolbar_frame, text='Просмотреть данные', command=lambda: show_train_data(root))
    btn_show_data.pack(side="left", padx=5, pady=5)

    btn_write_file = ttk.Button(toolbar_frame, text='Записать в файл', command=lambda: write_in_file(root))
    btn_write_file.pack(side="left", padx=5, pady=5)

    btn_search_info = ttk.Button(toolbar_frame, text='Найти информацию', command=lambda: Search_Info(root))
    btn_search_info.pack(side="left", padx=5, pady=5)

    btn_delete_data = ttk.Button(toolbar_frame, text='Удалить данные', command=lambda: delete_data(root))
    btn_delete_data.pack(side="left", padx=5, pady=5)

