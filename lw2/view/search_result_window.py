from tkinter import *
from tkinter import ttk

from model.Product import Product


class SearchResultWindow(Toplevel):
    def __init__(self, product_list: list[Product]):
        super().__init__()
        self.__product_list: list[Product] = product_list

        # window settings

        self.title('Результат поиска')
        self.geometry('1000x800')
        self.rowconfigure(index=0, weight=1)
        self.rowconfigure(index=1, weight=10)
        self.columnconfigure(index=0, weight=1)

        # result label

        self.__result_label: ttk.Label = ttk.Label(self, text='Результат поиска:')
        self.__result_label.grid(row=0, column=0)

        # result text panel

        self.__result_panel: ttk.Frame = ttk.Frame(self)
        self.__result_panel.rowconfigure(index=0, weight=1)
        self.__result_panel.columnconfigure(index=0, weight=1)
        self.__result_text: Listbox = Listbox(self.__result_panel,
                                              listvariable=Variable(value=self.list_to_text_convert()))
        self.__result_text.grid(row=0, column=0, sticky=NSEW)
        self.__result_scrollbar: ttk.Scrollbar = ttk.Scrollbar(self.__result_panel, orient='vertical',
                                                               command=self.__result_text.yview)
        self.__result_scrollbar.grid(sticky=E)
        self.__result_panel.grid(row=1, column=0, sticky=NSEW)

    def list_to_text_convert(self):
        text: list = []
        for i in self.__product_list:
            text.append(i.__str__())
        return text
