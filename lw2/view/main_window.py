import uuid
import math
from tkinter import *
from tkinter import ttk
from tkinter import filedialog

from model.Product import Product
from model.Manufacturer import Manufacturer

from view.add_product_window import AddProductWindow
from view.search_product_window import SearchProductWindow
from view.search_result_window import SearchResultWindow
from view.delete_product_window import DeleteProductWindow
from view.create_data_base_window import CreateDataBaseWindow
from view.create_xml_file_window import CreateXMLFileWindow

from controller.search_criteria import SearchCriteria
from controller.db_controller import DataBaseController
from controller.file_controller import FileController
from controller.data_controller import DataController


class MainWindow:
    def __init__(self):
        self.__data_controller = None
        self.__current_page: int = 1

        # window

        self.__main_window: Tk = Tk()
        self.__number_of_products_on_page: IntVar = IntVar(value=10)
        self.__tree_view: BooleanVar = BooleanVar(value=False)

        # window settings

        self.window_config()

        # menu creation

        self.__open_file_menu: Menu = Menu(tearoff=0)
        self.__new_file_menu: Menu = Menu(tearoff=0)
        self.__file_menu: Menu = Menu(tearoff=0)
        self.__main_window_menu: Menu = Menu(tearoff=0)
        self.menu_config()

        # products label frame

        self.__products_panel: ttk.Labelframe = ttk.LabelFrame(self.__main_window, text='Товары')
        self.products_panel_config()

        # products table

        tree_columns = ('id', 'name', 'manufacturer_name', 'manufacturer_id', 'amount_in_storage', 'storage_address')
        self.__products_table: ttk.Treeview = ttk.Treeview(columns=tree_columns, show='headings',
                                                           master=self.__products_panel)
        self.table_config()

        # products on page

        self.__products_on_page_panel: ttk.Frame = ttk.Frame(self.__main_window)
        self.__products_on_page_label_text: ttk.Label = ttk.Label(self.__products_on_page_panel,
                                                                  text='Товаров на странице: ')
        self.__products_on_page_box: ttk.Combobox = ttk.Combobox(self.__products_on_page_panel,
                                                                 textvariable=self.__number_of_products_on_page,
                                                                 values=['5', '10', '15'], state='readonly')
        self.__current_product_page: ttk.Label = ttk.Label(self.__products_on_page_panel, text='1/1')
        self.__tree_view_checkbutton: ttk.Checkbutton = ttk.Checkbutton(self.__products_on_page_panel,
                                                                        text='Отображение в виде дерева',
                                                                        variable=self.__tree_view,
                                                                        command=self.tree_view_switch)
        self.products_on_page_config()

        # page control

        self.__page_buttons: ttk.Frame = ttk.Frame(self.__main_window)
        self.__next_page_button: ttk.Button = ttk.Button(self.__page_buttons, text='Следующая страница', command=self.next_page)
        self.__prev_page_button: ttk.Button = ttk.Button(self.__page_buttons, text='Предыдущая страница', command=self.prev_page)
        self.__first_page_button: ttk.Button = ttk.Button(self.__page_buttons, text='Первая страница', command=self.first_page)
        self.__last_page_button: ttk.Button = ttk.Button(self.__page_buttons, text='Последняя странциа', command=self.last_page)
        self.page_control_config()

        # error message

        self.__error_message: StringVar = StringVar(value='')
        self.__error_label: ttk.Label = ttk.Label(textvariable=self.__error_message, foreground='red')
        self.__error_label.grid(row=3, column=0)

        self.__main_window.mainloop()

    def window_config(self) -> None:
        self.__main_window.title('Система управления товарами')
        self.__main_window.state('zoomed')
        self.__main_window.rowconfigure(index=0, weight=1)
        self.__main_window.columnconfigure(index=0, weight=1)

    def menu_config(self) -> None:
        self.__open_file_menu.add_command(label='Файл xml', command=self.open_xml)
        self.__open_file_menu.add_command(label='Базу данных', command=self.open_db)
        self.__new_file_menu.add_command(label='Новый файл xml', command=self.create_xml)
        self.__new_file_menu.add_command(label='Новую базу данных', command=self.create_db)
        self.__file_menu.add_cascade(label='Создать', menu=self.__new_file_menu)
        self.__file_menu.add_cascade(label='Открыть', menu=self.__open_file_menu)

        self.__main_window_menu.add_cascade(label='Файл', menu=self.__file_menu)
        self.__main_window_menu.add_cascade(label='Добавить товар', command=self.add_product_window)
        self.__main_window_menu.add_cascade(label='Удалить товар', command=self.product_deleting)
        self.__main_window_menu.add_cascade(label='Поиск товара', command=self.product_search)

        self.__main_window.config(menu=self.__main_window_menu)

    def products_panel_config(self) -> None:
        self.__products_panel.grid(row=0, column=0, sticky=NSEW)
        self.__products_panel.columnconfigure(index=0, weight=1)
        self.__products_panel.rowconfigure(index=0, weight=1)

    def table_config(self) -> None:
        self.__products_table.grid(row=0, column=0, sticky=NSEW)
        self.table_columns_config()

    def table_columns_config(self) -> None:
        self.__products_table.heading('id', text='ID', anchor=W)
        self.__products_table.heading('name', text='Название', anchor=W)
        self.__products_table.heading('manufacturer_name', text='Производитель', anchor=W)
        self.__products_table.heading('manufacturer_id', text='УНП производителя', anchor=W)
        self.__products_table.heading('amount_in_storage', text='Количество на складе', anchor=W)
        self.__products_table.heading('storage_address', text='Адрес хранения', anchor=W)
        self.__products_table.column('#1', stretch=NO, width=300)
        self.__products_table.column('#2', stretch=NO, width=220)
        self.__products_table.column('#3', stretch=NO, width=220)
        self.__products_table.column('#4', stretch=NO)
        self.__products_table.column('#5', stretch=NO)
        self.__products_table.column('#6', stretch=NO, width=300)

    def products_on_page_config(self) -> None:
        self.__products_on_page_panel.columnconfigure(index=(0, 1), weight=1)
        self.__products_on_page_panel.columnconfigure(index=2, weight=15)
        self.__products_on_page_panel.grid(row=1, column=0, sticky=NSEW)
        self.__products_on_page_label_text.grid(row=1, column=0, sticky=W)
        self.__products_on_page_box.grid(row=1, column=1, sticky=W)
        self.__tree_view_checkbutton.grid(row=1, column=2, sticky=E)
        self.__current_product_page.grid(row=1, column=2, sticky=NSEW)
        self.__products_on_page_box.bind("<<ComboboxSelected>>", self.new_page_value)

    def page_control_config(self) -> None:
        self.__page_buttons.columnconfigure(index=(0, 1, 2, 3), weight=0)
        self.__page_buttons.rowconfigure(index=0, weight=0)
        self.__prev_page_button.grid(row=0, column=0, sticky=W)
        self.__first_page_button.grid(row=0, column=1)
        self.__last_page_button.grid(row=0, column=2)
        self.__next_page_button.grid(row=0, column=3, sticky=E)
        self.__page_buttons.grid(row=2)

    def create_db(self) -> None:
        CreateDataBaseWindow(self)

    def open_db(self) -> None:
        filepath: str = filedialog.askopenfilename(title="Выбор файла", filetypes={('Data Base files', '*.db')})
        if filepath != "":
            self.form_db(filepath)

    def form_db(self, filename: str) -> None:
        self.__current_page = 1
        self.__data_controller: DataBaseController = DataBaseController(filename)
        self.page_update()

    def create_xml(self) -> None:
        CreateXMLFileWindow(self)

    def open_xml(self) -> None:
        filepath: str = filedialog.askopenfilename(title="Выбор файла", filetypes={('XML files', '*.xml')})
        if filepath != "":
            self.form_xml(filepath)

    def form_xml(self, filepath: str) -> None:
        self.__current_page = 1
        self.__data_controller: FileController = FileController(filepath)
        self.page_update()

    def page_update(self) -> None:
        if self.__data_controller is not None:
            max_page: int = max(1, math.ceil(self.__data_controller.products_amount()
                                             / int(self.__number_of_products_on_page.get())))
            if max_page < self.__current_page:
                self.__current_page -= 1
                raise IndexError
            if self.__current_page == 0:
                self.__current_page = 1
                raise IndexError
            self.__error_message.set('')
            self.__current_product_page['text'] = f'{self.__current_page}/{max_page}'
            products: list[Product] = self.__data_controller.get_products()
            for product in self.__products_table.get_children("")[:]:
                self.__products_table.delete(product)
            for product in products[(self.__current_page - 1) * int(self.__number_of_products_on_page.get()):
            self.__current_page * int(self.__number_of_products_on_page.get())]:
                if not self.__tree_view.get():
                    self.__products_table.insert("", END, values=product.tuple())
                else:
                    parent_product = self.__products_table.insert("", END, text='Product')
                    self.__products_table.insert(parent_product, index=END, text='id', values=product.id)
                    self.__products_table.insert(parent_product, index=END, text='name', values=product.name)
                    self.__products_table.insert(parent_product, index=END, text='manufacturer name',
                                                 values=product.manufacturer_name)
                    self.__products_table.insert(parent_product, index=END, text='manufacturer id',
                                                 values=product.manufacturer_id)
                    self.__products_table.insert(parent_product, index=END, text='amount in storage',
                                                 values=product.amount_in_storage)
                    self.__products_table.insert(parent_product, index=END, text='storage address',
                                                 values=product.storage_address)
        else:
            raise AttributeError

    def new_page_value(self, event) -> None:
        self.__current_page = 1
        self.page_update()

    def next_page(self) -> None:
        self.__error_message.set('')
        self.__current_page += 1
        try:
            self.page_update()
        except IndexError as e:
            self.__error_message.set('Вы и так на последней странице')
        except AttributeError as e:
            self.__error_message.set('Вы не открыли файл или базу данных, чтобы начать работу')

    def prev_page(self) -> None:
        self.__current_page -= 1
        try:
            self.page_update()
        except IndexError as e:
            self.__error_message.set('Вы и так на первой странице')
        except AttributeError as e:
            self.__error_message.set('Вы не открыли файл или базу данных, чтобы начать работу')

    def add_product_window(self) -> None:
        self.__error_message.set('')
        try:
            manufacturer_list: list[Manufacturer] = []
            products: list[Product] = self.__data_controller.get_products()
            for i in products:
                manufacturer = Manufacturer(uuid.uuid1(), i.manufacturer_name, i.manufacturer_id)
                if manufacturer not in manufacturer_list:
                    manufacturer_list.append(manufacturer)
            AddProductWindow(manufacturer_list, self)
        except AttributeError as e:
            self.__error_message.set('Вы не открыли файл или базу данных, чтобы начать работу')

    def product_search(self) -> None:
        self.__error_message.set('')
        if self.__data_controller is None:
            self.__error_message.set('Вы не открыли файл или базу данных, чтобы начать работу')
            return
        SearchProductWindow(self)

    def form_search_result(self, values) -> None:
        search_criteria: SearchCriteria = SearchCriteria(*values)
        result_list: list[Product] = self.__data_controller.search_products(search_criteria)
        SearchResultWindow(result_list)

    def product_deleting(self) -> None:
        self.__error_message.set('')
        if self.__data_controller is None:
            self.__error_message.set('Вы не открыли файл или базу данных, чтобы начать работу')
            return
        DeleteProductWindow(self)

    def tree_view_switch(self) -> None:
        if self.__tree_view.get():
            self.__products_table['show'] = 'tree'
        else:
            self.__products_table['show'] = 'headings'
        self.page_update()

    def first_page(self):
        self.__current_page = 1
        try:
            self.page_update()
        except AttributeError as e:
            self.__error_message.set('Вы не открыли файл или базу данных, чтобы начать работу')

    def last_page(self):
        self.__current_page = math.ceil(self.__data_controller.products_amount()
                                        / int(self.__number_of_products_on_page.get()))
        try:
            self.page_update()
        except AttributeError as e:
            self.__error_message.set('Вы не открыли файл или базу данных, чтобы начать работу')

    @property
    def data_controller(self) -> DataController:
        return self.__data_controller


MainWindow()
