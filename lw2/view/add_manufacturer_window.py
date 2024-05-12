from tkinter import *
from tkinter import ttk
import uuid
from model.Manufacturer import Manufacturer


class AddManufacturerWindow(Toplevel):
    def __init__(self, parent_window):
        super().__init__()
        self.__parent_window = parent_window

        # window settings

        self.title('Добавление производителя')
        self.geometry('500x300')

        # name panel

        self.__name_panel: ttk.Frame = ttk.Frame(self)
        self.__name_label: ttk.Label = ttk.Label(self.__name_panel, text='Введите название')
        self.__name_label.pack()
        self.__name_entry: ttk.Entry = ttk.Entry(self.__name_panel)
        self.__name_entry.pack()
        self.__name_panel.pack(pady=30)

        # UNP panel

        self.__UNP_panel: ttk.Frame = ttk.Frame(self)
        self.__UNP_label: ttk.Label = ttk.Label(self.__UNP_panel, text='Введите УНП производителя')
        self.__UNP_label.pack()
        self.__UNP_entry: ttk.Entry = ttk.Entry(self.__UNP_panel)
        self.__UNP_entry.pack()
        self.__UNP_panel.pack(pady=30)

        # add button

        self.__add_button: ttk.Button = ttk.Button(self, text='Добавить', command=self.return_data)
        self.__add_button.pack(pady=30)

        # error label

        self.__error_label: ttk.Label = ttk.Label(self, foreground='red')
        self.__error_label.pack()

    def return_data(self):
        if self.__name_entry.get() == '' or self.__UNP_entry.get() == '':
            self.__error_label['text'] = 'Для добавления производителя заполните все поля!'
            return
        new_manufacturer: Manufacturer = Manufacturer(uuid.uuid1(), self.__name_entry.get(), int(self.__UNP_entry.get()))
        self.__parent_window.add_manufacturer_to_box(new_manufacturer)
        self.destroy()
