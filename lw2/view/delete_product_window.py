from tkinter import *
from tkinter import ttk
from tkinter.messagebox import showinfo

from controller.search_criteria import SearchCriteria


class DeleteProductWindow(Toplevel):
    def __init__(self, main_window):
        super().__init__()
        self.__main_window = main_window

        # window settings

        self.title('Параметры удаления')
        self.geometry('700x400')
        self.rowconfigure(index=0, weight=1)
        self.rowconfigure(index=1, weight=2)
        self.rowconfigure(index=2, weight=1)
        self.rowconfigure(index=3, weight=1)
        self.columnconfigure(index=0, weight=1)

        # radiobuttons

        self.__name_criteria: str = 'name'
        self.__manufacturer_criteria: str = 'manufacturer'
        self.__address_criteria: str = 'address'

        self.__result_criteria: StringVar = StringVar(value=self.__name_criteria)

        self.__radiobuttons_panel: ttk.Frame = ttk.Frame(self)
        self.__radiobuttons_panel.columnconfigure(index=(0, 1, 2), weight=1)
        self.__radiobuttons_panel.rowconfigure(index=0, weight=1)
        self.__name_radiobutton: ttk.Radiobutton = ttk.Radiobutton(
            self.__radiobuttons_panel, text='Удаление по имени товара\nили количеству на складе',
            value=self.__name_criteria, variable=self.__result_criteria, command=self.select)
        self.__name_radiobutton.grid(row=0, column=0, sticky=W)
        self.__manufacturer_radiobutton: ttk.Radiobutton = ttk.Radiobutton(
            self.__radiobuttons_panel, text='Удаление по имени производителя\nили УНП производителя',
            value=self.__manufacturer_criteria, variable=self.__result_criteria, command=self.select)
        self.__manufacturer_radiobutton.grid(row=0, column=1, sticky=W)
        self.__address_radiobutton: ttk.Radiobutton = ttk.Radiobutton(
            self.__radiobuttons_panel, text='Удаление по адресу хранения', value=self.__address_criteria,
            variable=self.__result_criteria, command=self.select)
        self.__address_radiobutton.grid(row=0, column=2, sticky=W)
        self.__radiobuttons_panel.grid(row=0, column=0, pady=20, sticky=NSEW)

        # search input panel

        self.__search_input_panel: ttk.Frame = ttk.Frame(self)
        self.__search_input_panel.columnconfigure(index=(0, 1, 2), weight=1)
        self.__search_input_panel.rowconfigure(index=(0, 1, 2, 3), weight=1)
        self.__name_label: ttk.Label = ttk.Label(self.__search_input_panel, text='Введите имя товара')
        self.__name_entry: ttk.Entry = ttk.Entry(self.__search_input_panel, validate='key',
                                                 validatecommand=(self.register(self.validate_name), "%P"))
        self.__amount_in_storage_label: ttk.Label = ttk.Label(self.__search_input_panel,
                                                              text='Введите количество товара на складе')
        self.__amount_in_storage_entry: ttk.Entry = ttk.Entry(self.__search_input_panel, validate='key',
                                                              validatecommand=(self.register(self.validate_name), "%P"))
        self.__manufacturer_name_label: ttk.Label = ttk.Label(self.__search_input_panel,
                                                              text='Введите имя производителя')
        self.__manufacturer_name_entry: ttk.Entry = ttk.Entry(self.__search_input_panel, validate='key',
                                                              validatecommand=(self.register(
                                                                  self.validate_manufacturer), "%P"))
        self.__manufacturer_id_label: ttk.Label = ttk.Label(self.__search_input_panel,
                                                            text='Введите УНП производителя')
        self.__manufacturer_id_entry: ttk.Entry = ttk.Entry(self.__search_input_panel, validate='key',
                                                            validatecommand=(self.register(self.validate_manufacturer),
                                                                             "%P"))
        self.__storage_address_label: ttk.Label = ttk.Label(self.__search_input_panel,
                                                            text='Введите адрес хранения')
        self.__storage_address_entry: ttk.Entry = ttk.Entry(self.__search_input_panel, validate='key',
                                                            validatecommand=(self.register(self.validate_address),
                                                                             "%P"))
        self.__name_label.grid(row=0, column=0, pady=20, sticky=W)
        self.__name_entry.grid(row=1, column=0, pady=20, sticky=W)
        self.__amount_in_storage_label.grid(row=2, column=0, pady=20, sticky=W)
        self.__amount_in_storage_entry.grid(row=3, column=0, pady=20, sticky=W)
        self.__manufacturer_name_label.grid(row=0, column=1, pady=20, sticky=W)
        self.__manufacturer_name_entry.grid(row=1, column=1, pady=20, sticky=W)
        self.__manufacturer_id_label.grid(row=2, column=1, pady=20, sticky=W)
        self.__manufacturer_id_entry.grid(row=3, column=1, pady=20, sticky=W)
        self.__storage_address_label.grid(row=0, column=2, pady=20, sticky=W)
        self.__storage_address_entry.grid(row=1, column=2, pady=20, sticky=W)
        self.__search_input_panel.grid(row=1, column=0, pady=20, sticky=NSEW)

        # search button

        self.__search_button: ttk.Button = ttk.Button(self, text='Удалить', command=self.delete)
        self.__search_button.grid(row=2, column=0)

        # error label

        self.__error_message: StringVar = StringVar()
        self.__error_label: ttk.Label = ttk.Label(self, textvariable=self.__error_message, foreground='red')
        self.__error_label.grid(row=3, column=0)

    def select(self):
        match self.__result_criteria.get():
            case 'name':
                self.selected_name()
            case 'manufacturer':
                self.selected_manufacturer()
            case 'address':
                self.selected_address()

    def selected_name(self):
        self.__error_message.set('')

        self.__manufacturer_name_entry.delete(0, END)
        self.__manufacturer_id_entry.delete(0, END)
        self.__storage_address_entry.delete(0, END)

    def validate_name(self, new_value):
        if self.__result_criteria.get() != 'name':
            self.__name_entry.delete(0, END)
            self.__amount_in_storage_entry.delete(0, END)
        return self.__result_criteria.get() == 'name'

    def selected_manufacturer(self):
        self.__error_message.set('')

        self.__name_entry.delete(0, END)
        self.__amount_in_storage_entry.delete(0, END)
        self.__storage_address_entry.delete(0, END)

    def validate_manufacturer(self, new_value):
        if self.__result_criteria.get() != 'manufacturer':
            self.__manufacturer_name_entry.delete(0, END)
            self.__manufacturer_id_entry.delete(0, END)
        return self.__result_criteria.get() == 'manufacturer'

    def selected_address(self):
        self.__error_message.set('')

        self.__name_entry.delete(0, END)
        self.__amount_in_storage_entry.delete(0, END)
        self.__manufacturer_name_entry.delete(0, END)
        self.__manufacturer_id_entry.delete(0, END)

    def validate_address(self, new_value):
        if self.__result_criteria.get() != 'address':
            self.__storage_address_entry.delete(0, END)
        return self.__result_criteria.get() == 'address'

    def delete(self):
        try:
            search_criteria: SearchCriteria = SearchCriteria(self.__name_entry.get(), self.__manufacturer_name_entry.get(),
                        None if self.__manufacturer_id_entry.get() == '' else int(self.__manufacturer_id_entry.get()),
                        None if self.__amount_in_storage_entry.get() == '' else int(self.__amount_in_storage_entry.get()),
                        self.__storage_address_entry.get(), self.__result_criteria.get())
        except (AttributeError, ValueError) as e:
            self.__error_message.set('Неправильный формат ввода')
            return
        amount_of_deleted_elements: int = self.__main_window.data_controller.delete_products(search_criteria)
        showinfo_message = f'Было успешно удалено {amount_of_deleted_elements} товаров' if (
                amount_of_deleted_elements > 0) else \
            'Ни один товар не подошел под параметры,\nпоэтому ничего не было удалено'
        showinfo(title='Информация', message=showinfo_message)
        self.__main_window.page_update()
        self.destroy()
