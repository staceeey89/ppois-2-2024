from tkinter import *
from tkinter import ttk

from tkinter.messagebox import showerror


class CreateXMLFileWindow(Toplevel):
    def __init__(self, main_window):
        super().__init__()
        self.__main_window = main_window

        # window settings

        self.title('Создание файла')
        self.geometry('200x120')

        # label settings

        self.__file_label: ttk.Label = ttk.Label(self, text='Введите имя файла')
        self.__file_label.pack(pady=5)

        # entry settings

        self.__file_entry: ttk.Entry = ttk.Entry(self)
        self.__file_entry.pack(pady=10)

        # button settings

        self.__file_button: ttk.Button = ttk.Button(self, text='Создать', command=self.create)
        self.__file_button.pack(pady=10)

    def create(self):
        filename = self.__file_entry.get()
        if filename == '':
            showerror(title='Ошибка', message='Файл не может иметь пустое название')
            return
        filepath = '../xml/' + filename + '.xml'
        self.__main_window.form_xml(filepath)
        self.destroy()
