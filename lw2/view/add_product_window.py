from tkinter import *
from tkinter import ttk
import uuid
from model.Manufacturer import Manufacturer
from model.Product import Product
from add_manufacturer_window import AddManufacturerWindow


class AddProductWindow(Toplevel):
    def __init__(self, manufacturer_list, main_window):
        super().__init__()
        self.__manufacturer_list: list = manufacturer_list
        self.__main_window = main_window

        # window settings

        self.title('Добавление товара')
        self.geometry('600x400')
        self.rowconfigure(index=(0, 1, 2, 3), weight=1)

        # manufacturer choose panel

        self.__manufacturer_panel: ttk.Frame = ttk.Frame(self)
        self.__manufacturer_label: ttk.Label = ttk.Label(self.__manufacturer_panel,
                                                         text='Выберите производителя или добавьте нового')
        self.__manufacturer_label.pack()
        self.__manufacturer_box: ttk.Combobox = ttk.Combobox(self.__manufacturer_panel,
                                                             values=[i.name for i in manufacturer_list])
        self.__manufacturer_box.pack()
        self.__manufacturer_button: ttk.Button = ttk.Button(self.__manufacturer_panel, text='Добавить производителя',
                                                            command=self.add_manufacturer)
        self.__manufacturer_button.pack()
        self.__manufacturer_panel.pack(pady=20)

        # name panel

        self.__name_panel: ttk.Frame = ttk.Frame(self)
        self.__name_label: ttk.Label = ttk.Label(self.__name_panel, text='Введите имя')
        self.__name_label.pack()
        self.__name_entry: ttk.Entry = ttk.Entry(self.__name_panel)
        self.__name_entry.pack()
        self.__name_panel.pack(pady=20)

        # amount in storage panel

        self.__amount_in_storage_panel: ttk.Frame = ttk.Frame(self)
        self.__amount_in_storage_label: ttk.Label = ttk.Label(self.__amount_in_storage_panel,
                                                              text='Введите количество на складе')
        self.__amount_in_storage_label.pack()
        self.__amount_in_storage_entry: ttk.Entry = ttk.Entry(self.__amount_in_storage_panel)
        self.__amount_in_storage_entry.pack()
        self.__amount_in_storage_panel.pack(pady=20)

        # storage address panel

        self.__storage_address_panel: ttk.Frame = ttk.Frame(self)
        self.__storage_address_label: ttk.Label = ttk.Label(self.__storage_address_panel, text='Введите адрес хранения')
        self.__storage_address_label.pack()
        self.__storage_address_entry: ttk.Entry = ttk.Entry(self.__storage_address_panel)
        self.__storage_address_entry.pack()
        self.__storage_address_panel.pack(pady=20)

        # add button

        self.__add_button: ttk.Button = ttk.Button(self, text='Добавить', command=self.return_data)
        self.__add_button.pack()

        # error label

        self.__error_label: ttk.Label = ttk.Label(self, foreground='red')
        self.__error_label.pack()

    def add_manufacturer(self):
        AddManufacturerWindow(self)

    def add_manufacturer_to_box(self, manufacturer):
        self.__manufacturer_box.insert(END, manufacturer.name)
        new_list: list = list(self.__manufacturer_box['values'])
        new_list.append(manufacturer.name)
        self.__manufacturer_box['values'] = tuple(new_list)
        self.__manufacturer_list.append(manufacturer)

    def return_data(self):
        if (self.__name_entry.get() == '' or self.__storage_address_entry.get() == '' or
                self.__amount_in_storage_entry.get() == '' or self.__manufacturer_box.get() == ''):
            self.__error_label['text'] = 'Для добавления товара заполните все поля'
            return
        manufacturer: Manufacturer = Manufacturer(uuid.uuid1(), '', 0)
        for i in self.__manufacturer_list:
            if self.__manufacturer_box.get() == i.name:
                manufacturer = i
        try:
            product = (uuid.uuid1(), self.__name_entry.get(), manufacturer.name, manufacturer.UNP,
                       int(self.__amount_in_storage_entry.get()), self.__storage_address_entry.get())
        except ValueError as e:
            self.__error_label['text'] = 'Неправильный формат ввода'
            return
        self.__main_window.data_controller.add_product(Product(*product))
        self.__main_window.page_update()
        self.destroy()
