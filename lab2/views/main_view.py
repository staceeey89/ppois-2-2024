import math
import tkinter
from tkinter import ttk
from tkinter import filedialog

from controllers import DAO
from views.adding_view import AddingWindow
from views.delete_view import DeleteWindow
from views.select_view import SelectWindow
import views.window_operations
from models.source_type import SourceType
from controllers.xml_parser import XMLParser
from tkinter import messagebox


class Application:
    def __init__(self):
        self.source_type = SourceType.database
        self.window = tkinter.Tk()
        self.train_trips_dao = DAO.TrainTripDAO()
        self.trains_dao = DAO.TrainDAO()
        self.stations_dao = DAO.StationDAO()
        self.xml_parser = None
        self.window.title("TrainTrips")
        self.window.resizable(False, False)
        self.current_page = 1
        self.page_size = 10
        views.window_operations.window_center(self.window, 1000, 700)

        self.is_treeview = tkinter.IntVar()

        self.menu = tkinter.Menu(self.window)
        self.file_menu = tkinter.Menu()
        self.file_menu.add_command(label="Открыть файл", command=self.open_xml_file)
        self.file_menu.add_command(label="Сохранить файл", command=self.save_xml_file)
        self.file_menu.add_command(label="Переключиться на БД", command=self.switch_to_database)
        self.menu.add_cascade(label="Файл", menu=self.file_menu)
        self.window.config(menu=self.menu)

        self.button_add = ttk.Button(self.window, text="Добавить поездку", command=self.adding_button_click)
        self.button_delete = ttk.Button(self.window, text="Удалить поездку(и)", command=self.delete_button_click)
        self.button_search = ttk.Button(self.window, text="Искать поездку(и)", command=self.select_button_click)
        self.treeview_checkbutton = ttk.Checkbutton(self.window, variable=self.is_treeview, text="Treeview", command=self.treeview_checkbutton_click)
        self.page_prev_button = ttk.Button(self.window, text="<", width=1, command=self.prev_page_click)
        self.page_next_button = ttk.Button(self.window, text=">", width=1, command=self.next_page_click)
        self.first_page_button = ttk.Button(self.window, text="<<", width=2, command=lambda: self.change_page(1))
        self.last_page_button = ttk.Button(self.window, text=">>", width=2, command=lambda: self.change_page(self.get_last_page()))
        self.current_page_combobox = ttk.Combobox(self.window, width=2, values=list([str(i) for i in range(1, math.ceil((self.train_trips_dao.get_rows_count() / self.page_size)) + 1)]))
        self.current_page_combobox.set(self.current_page)
        self.current_page_combobox.bind("<<ComboboxSelected>>", func=lambda event: self.change_page(int(self.current_page_combobox.get())))
        self.page_size_label = ttk.Label(self.window, text="Кол-во записей:")
        self.page_size_combobox = ttk.Combobox(self.window, width=2, values=["5", "10", "15", "20"])
        self.page_size_combobox.set(10)
        self.page_size_button = ttk.Button(self.window, text="OK", width=2, command=lambda: self.change_page_size(int(self.page_size_combobox.get())))

        self.button_add.place(x=50, y=15)
        self.button_delete.place(x=220, y=15)
        self.button_search.place(x=400, y=15)
        self.treeview_checkbutton.place(x=570, y=19)
        views.window_operations.widget_center(self.current_page_combobox, 1000, 565)
        self.page_prev_button.place(x=430, y=565)
        self.page_next_button.place(x=522, y=565)
        self.first_page_button.place(x=370, y=565)
        self.last_page_button.place(x=573, y=565)
        self.page_size_label.place(x=370, y=598)
        views.window_operations.widget_center(self.page_size_combobox, 1000, 595)
        self.page_size_button.place(x=520, y=595)

        columns = (
            "train_id",
            "departure_station",
            "arrival_station",
            "departure_datetime",
            "arrival_datetime",
            "travel_time"
        )

        self.table = ttk.Treeview(columns=columns, show="headings")
        self.table.config(height=26)
        self.table.place(x=50, y=60, width=900)

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
        self.window.mainloop()

    def adding_button_click(self):
        AddingWindow(master=self.window, application=self)

    def delete_button_click(self):
        DeleteWindow(master=self.window, application=self)

    def select_button_click(self):
        SelectWindow(master=self.window, application=self)

    def treeview_checkbutton_click(self):
        if self.is_treeview.get() == 1:
            self.table.config(show="tree", height=26)
            for item in self.table.get_children():
                self.table.delete(item)

            if self.source_type == SourceType.database:
                values = self.train_trips_dao.get_page(self.current_page, self.page_size)
            else:
                values = self.xml_parser.get_page_train_trips(self.current_page, self.page_size)

            for i in range(len(values)):
                self.table.insert("", tkinter.END, iid=i, text="Поездка №%d" % (i+1))
                self.table.insert(parent=i, index=tkinter.END, text="Номер поезда", values=values[i][0])
                self.table.insert(parent=i, index=tkinter.END, text="Станция отправления", values=values[i][1])
                self.table.insert(parent=i, index=tkinter.END, text="Станция прибытия", values=values[i][2])
                self.table.insert(parent=i, index=tkinter.END, text="Дата и время отправления", values=values[i][3])
                self.table.insert(parent=i, index=tkinter.END, text="Дата и время прибытия", values=values[i][4])
                self.table.insert(parent=i, index=tkinter.END, text="Время в пути", values=values[i][5])
        else:
            self.table.config(show="headings", height=20)
            self.update_train_trips_table()

    def update_train_trips_table(self):
        if self.source_type == SourceType.database:
            self.train_trips_dao = DAO.TrainTripDAO()
            values = self.train_trips_dao.get_page(self.current_page, self.page_size)
            self.current_page_combobox.config(values=list(
                [str(i) for i in range(1, math.ceil((self.train_trips_dao.get_rows_count() / self.page_size)) + 1)]))
        else:
            values = self.xml_parser.get_page_train_trips(self.current_page, self.page_size)
            self.current_page_combobox.config(values=list(
                [str(i) for i in range(1, math.ceil((len(self.xml_parser.get_all_train_trips()) / self.page_size)) + 1)]))

        for item in self.table.get_children():
            self.table.delete(item)

        for i in range(len(values)):
            self.table.insert("", tkinter.END, values=values[i])

    def update_train_trips_treeview(self):
        if self.source_type == SourceType.database:
            self.train_trips_dao = DAO.TrainTripDAO()
            values = self.train_trips_dao.get_page(self.current_page, self.page_size)
            self.current_page_combobox.config(values=list(
                [str(i) for i in range(1, math.ceil((self.train_trips_dao.get_rows_count() / self.page_size)) + 1)]))
        else:
            values = self.xml_parser.get_page_train_trips(self.current_page, self.page_size)
            self.current_page_combobox.config(values=list(
                [str(i) for i in
                 range(1, math.ceil((len(self.xml_parser.get_all_train_trips()) / self.page_size)) + 1)]))

        for item in self.table.get_children():
            self.table.delete(item)

        for i in range(len(values)):
            self.table.insert("", tkinter.END, iid=i, text="Поездка №%d" % (i + 1))
            self.table.insert(parent=i, index=tkinter.END, text="Номер поезда", values=values[i][0])
            self.table.insert(parent=i, index=tkinter.END, text="Станция отправления", values=values[i][1])
            self.table.insert(parent=i, index=tkinter.END, text="Станция прибытия", values=values[i][2])
            self.table.insert(parent=i, index=tkinter.END, text="Дата и время отправления", values=values[i][3])
            self.table.insert(parent=i, index=tkinter.END, text="Дата и время прибытия", values=values[i][4])
            self.table.insert(parent=i, index=tkinter.END, text="Время в пути", values=values[i][5])

    def next_page_click(self):
        self.change_page(self.current_page + 1)

    def prev_page_click(self):
        self.change_page(self.current_page - 1)

    def change_page(self, page):
        if self.source_type == SourceType.database:
            last_page = math.ceil(self.train_trips_dao.get_rows_count() / self.page_size)
        else:
            last_page = math.ceil(len(self.xml_parser.get_all_train_trips()) / self.page_size)
        if 1 <= page <= last_page:
            self.current_page = page
            self.current_page_combobox.set(self.current_page)
            if self.is_treeview.get() == 1:
                self.update_train_trips_treeview()
            else:
                self.update_train_trips_table()

    def change_page_size(self, size):
        self.page_size = size
        if self.is_treeview.get() == 1:
            self.update_train_trips_treeview()
        else:
            self.update_train_trips_table()
        self.change_page(1)

    def open_xml_file(self):
        source = filedialog.askopenfilename()
        self.xml_parser = XMLParser(source)
        self.source_type = SourceType.xml
        self.update_train_trips_table()
        self.change_page(1)

    def save_xml_file(self):
        if self.source_type == SourceType.xml:
            self.xml_parser.commit()
        else:
            tkinter.messagebox.showinfo(message="Вы можете сохранять только XML файлы.")

    def switch_to_database(self):
        self.source_type = SourceType.database
        self.update_train_trips_table()
        self.change_page(1)

    def get_last_page(self):
        if self.source_type == SourceType.database:
            return math.ceil(self.train_trips_dao.get_rows_count() / self.page_size)
        else:
            return math.ceil(len(self.xml_parser.get_all_train_trips()) / self.page_size)


window = Application()
