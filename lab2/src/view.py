from math import ceil
import tkinter as tk
import tkinter.ttk as ttk
from random import randint
from tkinter import messagebox, Toplevel, END

from anytree import Node, RenderTree

from src.controller import check_types
from extras.sql_storage import SqlStorage
from extras.tournament import Tournament
from extras.xml_storage import XmlStorage

sql_storage = SqlStorage()
xml_storage = XmlStorage()


class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Tournament Database')
        self.geometry('300x500')
        self._protected_create_toolbar()
        self._protected_create_buttons()

    def _protected_create_toolbar(self):
        toolbar = tk.Menu(self)
        self.config(menu=toolbar)

        file_menu = tk.Menu(toolbar, tearoff=0)
        file_menu.add_command(label='Open the database', command=lambda: self._protected_show_data('db'))
        file_menu.add_command(label='Save database', command=lambda: self._protected_save_changes('db'))
        file_menu.add_command(label='Open the xml', command=lambda: self._protected_show_data('xml'))
        file_menu.add_command(label='Save xml', command=lambda: self._protected_save_changes('xml'))

        add_tournament_menu = tk.Menu(toolbar, tearoff=0)
        add_tournament_menu.add_command(label='Add new tournament to db',
                                        command=lambda: self._protected_add_tournament('db'))
        add_tournament_menu.add_command(label='Add new tournament to xml',
                                        command=lambda: self._protected_add_tournament('xml'))

        search_menu = tk.Menu(toolbar, tearoff=0)
        search_menu.add_command(label='Search by tournament name in db',
                                command=lambda: self._protected_search_by_trn_name('db'))
        search_menu.add_command(label='Search by tournament sport in db',
                                command=lambda: self._protected_search_by_trn_sport('db'))
        search_menu.add_command(label='Search by tournament prize in db',
                                command=lambda: self._protected_search_by_trn_prize('db'))
        search_menu.add_command(label='Search by tournament name in xml',
                                command=lambda: self._protected_search_by_trn_name('xml'))
        search_menu.add_command(label='Search by tournament sport in xml',
                                command=lambda: self._protected_search_by_trn_sport('xml'))
        search_menu.add_command(label='Search by tournament prize in xml',
                                command=lambda: self._protected_search_by_trn_prize('xml'))

        delete_menu = tk.Menu(toolbar, tearoff=0)
        delete_menu.add_command(label='Delete by tournament name in db',
                                command=lambda: self._protected_delete_by_trn_name('db'))
        delete_menu.add_command(label='Delete by tournament sport in db',
                                command=lambda: self._protected_delete_by_trn_sport('db'))
        delete_menu.add_command(label='Delete by tournament prize in db',
                                command=lambda: self._protected_delete_by_trn_prize('db'))
        delete_menu.add_command(label='Delete by tournament name in xml',
                                command=lambda: self._protected_delete_by_trn_name('xml'))
        delete_menu.add_command(label='Delete by tournament sport in xml',
                                command=lambda: self._protected_delete_by_trn_sport('xml'))
        delete_menu.add_command(label='Delete by tournament prize in xml',
                                command=lambda: self._protected_delete_by_trn_prize('xml'))

        tree_menu = tk.Menu(toolbar, tearoff=0)
        tree_menu.add_command(label='Tree view in db', command=lambda: self._protected_tree_view('db'))
        tree_menu.add_command(label='Tree view in xml', command=lambda: self._protected_tree_view('xml'))

        toolbar.add_cascade(label='File', menu=file_menu)
        toolbar.add_cascade(label='Add', menu=add_tournament_menu)
        toolbar.add_cascade(label='Search', menu=search_menu)
        toolbar.add_cascade(label='Delete', menu=delete_menu)
        toolbar.add_cascade(label='Tree', menu=tree_menu)

    def _protected_create_buttons(self):
        open_database_db = ttk.Button(text='Open the database', command=lambda: self._protected_show_data('db'))
        save_database_db = ttk.Button(text='Save database', command=lambda: self._protected_save_changes('db'))
        open_database_xml = ttk.Button(text='Open the xml', command=lambda: self._protected_show_data('xml'))
        save_database_xml = ttk.Button(text='Save xml', command=lambda: self._protected_save_changes('xml'))
        open_database_db.pack()
        save_database_db.pack()
        open_database_xml.pack()
        save_database_xml.pack()

        add_tournament_db = ttk.Button(text='Add new tournament to db',
                                       command=lambda: self._protected_add_tournament('db'))
        add_tournament_xml = ttk.Button(text='Add new tournament to xml',
                                        command=lambda: self._protected_add_tournament('xml'))
        add_tournament_db.pack()
        add_tournament_xml.pack()

        search_by_trn_name_db = ttk.Button(text='Search by tournament name in db',
                                           command=lambda: self._protected_search_by_trn_name('db'))
        search_by_trn_sport_db = ttk.Button(text='Search by tournament sport in db',
                                            command=lambda: self._protected_search_by_trn_sport('db'))
        search_by_trn_prize_db = ttk.Button(text='Search by tournament prize in db',
                                            command=lambda: self._protected_search_by_trn_prize('db'))
        search_by_trn_name_xml = ttk.Button(text='Search by tournament name in xml',
                                            command=lambda: self._protected_search_by_trn_name('xml'))
        search_by_trn_sport_xml = ttk.Button(text='Search by tournament sport in xml',
                                             command=lambda: self._protected_search_by_trn_sport('xml'))
        search_by_trn_prize_xml = ttk.Button(text='Search by tournament prize in xml',
                                             command=lambda: self._protected_search_by_trn_prize('xml'))
        search_by_trn_name_db.pack()
        search_by_trn_sport_db.pack()
        search_by_trn_prize_db.pack()
        search_by_trn_name_xml.pack()
        search_by_trn_sport_xml.pack()
        search_by_trn_prize_xml.pack()

        delete_by_trn_name_db = ttk.Button(text='Delete by tournament name in db',
                                           command=lambda: self._protected_delete_by_trn_name('db'))
        delete_by_trn_sport_db = ttk.Button(text='Delete by tournament sport in db',
                                            command=lambda: self._protected_delete_by_trn_sport('db'))
        delete_by_trn_prize_db = ttk.Button(text='Delete by tournament prize in db',
                                            command=lambda: self._protected_delete_by_trn_prize('db'))
        delete_by_trn_name_xml = ttk.Button(text='Delete by tournament name in xml',
                                            command=lambda: self._protected_delete_by_trn_name('xml'))
        delete_by_trn_sport_xml = ttk.Button(text='Delete by tournament sport in xml',
                                             command=lambda: self._protected_delete_by_trn_sport('xml'))
        delete_by_trn_prize_xml = ttk.Button(text='Delete by tournament prize in xml',
                                             command=lambda: self._protected_delete_by_trn_prize('xml'))
        delete_by_trn_name_db.pack()
        delete_by_trn_sport_db.pack()
        delete_by_trn_prize_db.pack()
        delete_by_trn_name_xml.pack()
        delete_by_trn_sport_xml.pack()
        delete_by_trn_prize_xml.pack()

        tree_view_db = ttk.Button(text='Tree view in db', command=lambda: self._protected_tree_view('db'))
        tree_view_xml = ttk.Button(text='Tree view in xml', command=lambda: self._protected_tree_view('xml'))
        tree_view_db.pack()
        tree_view_xml.pack()

    def _protected_show_data(self, storage):
        data_table = DataTable(self, storage)
        data_table.show_all_tournaments()
        data_table.grab_set()

    @staticmethod
    def _protected_save_changes(storage):
        source = {'db': sql_storage.save, 'xml': xml_storage.save}
        source[storage]()
        messagebox.showinfo('Save changes', f'Save {storage} changes')

    def _protected_add_tournament(self, storage):
        add_tournament_window = AddTournamentWindow(self, storage)
        add_tournament_window.grab_set()

    def _protected_search_by_trn_name(self, storage):
        search_window = SearchWindow(self, storage)
        search_window.search_by_trn_name()
        search_window.grab_set()

    def _protected_search_by_trn_sport(self, storage):
        search_window = SearchWindow(self, storage)
        search_window.search_by_trn_sport()
        search_window.grab_set()

    def _protected_search_by_trn_prize(self, storage):
        search_window = SearchWindow(self, storage)
        search_window.search_by_trn_prize()
        search_window.grab_set()

    def _protected_delete_by_trn_name(self, storage):
        search_window = SearchWindow(self, storage)
        search_window.delete_by_trn_name()
        search_window.grab_set()

    def _protected_delete_by_trn_sport(self, storage):
        search_window = SearchWindow(self, storage)
        search_window.delete_by_trn_sport()
        search_window.grab_set()

    def _protected_delete_by_trn_prize(self, storage):
        search_window = SearchWindow(self, storage)
        search_window.delete_by_trn_prize()
        search_window.grab_set()

    def _protected_tree_view(self, storage):
        tree_window = TreeWindow(self, storage)
        tree_window.grab_set()


class TreeWindow(Toplevel):
    def __init__(self, parent, storage):
        super().__init__(parent)
        self.title("Tournament Tree")
        self.parent = parent
        self.data = {'db': sql_storage.get_all_tournaments, 'xml': xml_storage.get_all_tournaments}[storage](limit=100)
        root = Node('Tournaments')
        for tournament in self.data:
            new_node = Node(tournament.trn_name, parent=root)
            Node(f"Date: {tournament.trn_date}", parent=new_node)
            Node(f"Sport: {tournament.trn_sport}", parent=new_node)
            Node(f"Winner: {tournament.win_name}", parent=new_node)
            Node(f"T. Prize: {tournament.trn_prize}", parent=new_node)
            Node(f"W. Prize: {tournament.win_prize}", parent=new_node)

        text_widget = tk.Text(self, width=40, height=20)
        text_widget.pack()
        self._protected_display_tree(root, text_widget)

    @staticmethod
    def _protected_display_tree(root, text_widget):
        for pre, fill, node in RenderTree(root):
            text_widget.insert(tk.END, "%s%s\n" % (pre, node.name))


class DataTable(Toplevel):
    def __init__(self, parent, storage):
        super().__init__(parent)
        self.storage = storage
        self.title(f'Data Table - {self.storage.upper()}')
        self.geometry('1200x500')
        self.database = sql_storage if storage == 'db' else xml_storage
        self.current_page = 1
        self.records_per_page = 10
        self.max_pages = len(self.database) // self.records_per_page

    def show_all_tournaments(self):
        columns = ('trn_name', 'trn_date', 'trn_sport', 'win_name', 'win_prize', 'trn_prize')
        tree = ttk.Treeview(self, columns=columns, show='headings')
        tree.heading('trn_name', text='T. Name')
        tree.heading('trn_date', text='T. Date')
        tree.heading('trn_sport', text='T. Sport')
        tree.heading('win_name', text='W. Name')
        tree.heading('win_prize', text='T. Prize')
        tree.heading('trn_prize', text='W. Prize')

        def fill_table():
            source = {'db': sql_storage.get_all_tournaments, 'xml': xml_storage.get_all_tournaments}
            for trn in source[self.storage]((self.current_page - 1) * self.records_per_page,
                                            self.records_per_page):
                tournament = (trn.trn_name, trn.trn_date, trn.trn_sport, trn.win_name, trn.trn_prize, trn.win_prize)
                tree.insert('', END, values=tournament)

        fill_table()
        tree.pack(fill='both', expand=True)

        def update_page_info():
            page_count_label.config(text=f'{self.current_page}/{self.max_pages}')
            record_per_page_label.config(text=f'Records Per Page: {self.records_per_page}')
            total_records_label.config(text=f'Records Per Page: {len(self.database)}')

        def destroy_and_restart_tree():
            tree.delete(*tree.get_children())
            update_page_info()
            fill_table()

        def first_page():
            self.current_page = 1
            destroy_and_restart_tree()

        def prev_page():
            if self.current_page == 1:
                pass
            else:
                self.current_page -= 1
                destroy_and_restart_tree()

        def next_page():
            if self.current_page == self.max_pages:
                pass
            else:
                self.current_page += 1
                destroy_and_restart_tree()

        def last_page():
            self.current_page = self.max_pages
            destroy_and_restart_tree()

        def add_buttons_below_treeview():
            button_frame = tk.Frame(self)
            button_frame.pack()

            btn_first_page = tk.Button(button_frame, text="First Page", command=first_page)
            btn_first_page.pack(side=tk.LEFT, padx=5)

            btn_prev_page = tk.Button(button_frame, text="Prev Page", command=prev_page)
            btn_prev_page.pack(side=tk.LEFT, padx=5)

            page_size_entry_var = tk.StringVar()
            page_size_entry_var.set(self.records_per_page)
            page_size_entry = tk.Entry(button_frame, textvariable=page_size_entry_var)
            page_size_entry.pack(side=tk.LEFT, padx=5)

            btn_next_page = tk.Button(button_frame, text="Next Page", command=next_page)
            btn_next_page.pack(side=tk.LEFT, padx=5)

            btn_last_page = tk.Button(button_frame, text="Last Page", command=last_page)
            btn_last_page.pack(side=tk.LEFT, padx=5)

            def update():
                new_records_for_page = page_size_entry_var.get()
                if new_records_for_page.isdigit() and 0 < int(new_records_for_page) <= len(self.database):
                    self.records_per_page = int(new_records_for_page)
                    self.current_page = 1
                    self.max_pages = ceil((len(self.database) / self.records_per_page))
                    destroy_and_restart_tree()
                else:
                    messagebox.showinfo('Bad News', f'Invalid number of records: {new_records_for_page}')

            btn_update = tk.Button(self, text='Update', command=update)
            btn_update.pack()

        page_info_frame = tk.Frame(self)
        page_info_frame.pack()

        page_count_label = ttk.Label(page_info_frame, text=f'{self.current_page}/{self.max_pages}')
        page_count_label.pack(side=tk.LEFT, padx=5)

        record_per_page_label = ttk.Label(page_info_frame, text=f'Records Per Page: {self.records_per_page}')
        record_per_page_label.pack(side=tk.LEFT, padx=5)

        total_records_label = ttk.Label(page_info_frame, text=f'Records Per Page: {len(self.database)}')
        total_records_label.pack(side=tk.LEFT, padx=5)

        add_buttons_below_treeview()

    def show_that_tournaments(self, tournaments):
        columns = ('trn_name', 'trn_date', 'trn_sport', 'win_name', 'win_prize', 'trn_prize')
        tree = ttk.Treeview(self, columns=columns, show='headings')
        tree.heading('trn_name', text='T. Name')
        tree.heading('trn_date', text='T. Date')
        tree.heading('trn_sport', text='T. Sport')
        tree.heading('win_name', text='W. Name')
        tree.heading('win_prize', text='T. Prize')
        tree.heading('trn_prize', text='W. Prize')

        for trn in tournaments:
            tournament = (trn.trn_name, trn.trn_date, trn.trn_sport, trn.win_name, trn.trn_prize, trn.win_prize)
            tree.insert('', END, values=tournament)

        tree.pack(expand=True, fill='both')


class AddTournamentWindow(Toplevel):
    def __init__(self, parent, storage):
        super().__init__(parent)
        self.title(f'Add Tournament - {storage.upper()}')
        self.geometry('400x150')

        entry_trn_name = ttk.Entry(self)
        entry_trn_date = ttk.Entry(self)
        entry_trn_sport = ttk.Entry(self)
        entry_win_name = ttk.Entry(self)
        entry_trn_prize = ttk.Entry(self)

        entry_trn_name.grid(row=0, column=0)
        entry_trn_date.grid(row=1, column=0)
        entry_trn_sport.grid(row=2, column=0)
        entry_win_name.grid(row=3, column=0)
        entry_trn_prize.grid(row=4, column=0)

        label_trn_name = ttk.Label(self, text='Insert Tournament Name')
        label_trn_date = ttk.Label(self, text='Insert Tournament Date in format YYYY-MM-DD')
        label_trn_sport = ttk.Label(self, text='Insert Tournament Sport')
        label_win_name = ttk.Label(self, text='Insert Winner Name')
        label_trn_prize = ttk.Label(self, text='Insert Tournament Prize')

        label_trn_name.grid(row=0, column=1)
        label_trn_date.grid(row=1, column=1)
        label_trn_sport.grid(row=2, column=1)
        label_win_name.grid(row=3, column=1)
        label_trn_prize.grid(row=4, column=1)

        def add_tournament():
            trn_name: str = entry_trn_name.get()
            trn_date: str = entry_trn_date.get()
            trn_sport: str = entry_trn_sport.get()
            win_name: str = entry_win_name.get()
            trn_prize: str = entry_trn_prize.get()

            errors: str = check_types(trn_name, trn_date, trn_sport, win_name, trn_prize)
            if not errors:
                source = {'db': sql_storage.insert, 'xml': xml_storage.insert}
                tournament = Tournament(
                    randint(1, 100),
                    trn_name,
                    trn_date,
                    trn_sport,
                    win_name,
                    int(trn_prize)
                )
                source[storage](tournament)
                messagebox.showinfo('Good News', 'Tournament was added successfully')
                self.destroy()
            else:
                messagebox.showinfo('Bad News', errors)

        btn_add_tournament = ttk.Button(self, text='Add Tournament', command=add_tournament)
        btn_add_tournament.grid(row=5, column=1)


class SearchWindow(Toplevel):
    def __init__(self, parent, storage):
        super().__init__(parent)
        self.title(f'Search Window - {storage.upper()}')
        self.geometry('400x150')
        self.storage = storage
        self.parent = parent

    def search_by_trn_name(self):
        entry_trn_name = ttk.Entry(self)
        entry_trn_name.grid(row=0, column=0)
        label_trn_name = ttk.Label(self, text='Insert Tournament Name')
        label_trn_name.grid(row=0, column=1)
        button = ttk.Button(self, text='Search', command=lambda: self._protected_show_trn_name(entry_trn_name))
        button.grid(row=2, column=2)

    def search_by_trn_sport(self):
        source = {'db': sql_storage.get_all_sports, 'xml': xml_storage.get_all_sports}
        sports = source[self.storage]()
        selected_option = tk.StringVar(self)
        selected_option.set(sports[0])
        dropdown = ttk.OptionMenu(self, selected_option, *sports)
        dropdown.grid(row=0, column=0)
        label_trn_sport = ttk.Label(self, text='Select Tournament Sport')
        label_trn_sport.grid(row=0, column=1)

        button = ttk.Button(self, text='Search', command=lambda: self._protected_show_trn_sport(selected_option))
        button.grid(row=2, column=2)

    def search_by_trn_prize(self):
        entry_trn_prize_bottom = ttk.Entry(self)
        entry_trn_prize_top = ttk.Entry(self)
        entry_trn_prize_bottom.grid(row=0, column=0)
        entry_trn_prize_top.grid(row=1, column=0)

        label_trn_prize_bottom = ttk.Label(self, text='Insert Tournament Prize Bottom')
        label_trn_prize_bottom.grid(row=0, column=1)
        label_trn_prize_bottom = ttk.Label(self, text='Insert Tournament Prize Top')
        label_trn_prize_bottom.grid(row=1, column=1)

        button = ttk.Button(self, text='Search',
                            command=lambda: self._protected_show_trn_prize(entry_trn_prize_bottom, entry_trn_prize_top))
        button.grid(row=2, column=2)

    def _protected_show_trn_name(self, entry):
        trn_name: str = entry.get()
        if all([el.isalnum() for el in trn_name.split()]):
            source = {'db': sql_storage.search_by_trn_name, 'xml': xml_storage.search_by_trn_name}
            tournaments = source[self.storage](trn_name, limit=10)
            if not tournaments:
                messagebox.showinfo('Bad News', 'There is no tournament with that name')
            else:
                data_table = DataTable(self.parent, self.storage)
                data_table.show_that_tournaments(tournaments)
                data_table.grab_set()
                self.destroy()
        else:
            messagebox.showinfo('Bad News', f'Incorrect Tournament Name: {trn_name}')

    def _protected_show_trn_sport(self, selected_option):
        sport = selected_option.get()
        source = {'db': sql_storage.search_by_trn_sport, 'xml': xml_storage.search_by_trn_sport}
        tournaments = source[self.storage](sport, limit=10)
        data_table = DataTable(self.parent, self.storage)
        data_table.show_that_tournaments(tournaments)
        data_table.grab_set()
        self.destroy()

    def _protected_show_trn_prize(self, bottom, top):
        prize_bottom = bottom.get()
        prize_top = top.get()
        if prize_bottom.isdigit() and prize_top.isdigit():
            source = {'db': sql_storage.search_by_trn_prize, 'xml': xml_storage.search_by_trn_prize}
            tournaments = source[self.storage](int(prize_bottom), int(prize_top), limit=10)
            if not tournaments:
                messagebox.showinfo('Bad News', 'There is no tournament with that prize')
            else:
                data_table = DataTable(self.parent, self.storage)
                data_table.show_that_tournaments(tournaments)
                data_table.grab_set()
                self.destroy()
        else:
            messagebox.showinfo('Bad News', f'Incorrect Tournament Prize: {bottom, top}')

    def delete_by_trn_name(self):
        self.title('Delete Window')
        entry_trn_name = ttk.Entry(self)
        entry_trn_name.grid(row=0, column=0)
        label_trn_name = ttk.Label(self, text='Insert Tournament Name')
        label_trn_name.grid(row=0, column=1)
        button = ttk.Button(self, text='Delete', command=lambda: self._protected_delete_by_trn_name(entry_trn_name))
        button.grid(row=2, column=2)

    def delete_by_trn_sport(self):
        self.title('Delete Window')
        source = {'db': sql_storage.get_all_sports, 'xml': xml_storage.get_all_sports}
        sports = source[self.storage]()
        selected_option = tk.StringVar(self)
        selected_option.set(sports[0])
        dropdown = ttk.OptionMenu(self, selected_option, *sports)
        dropdown.grid(row=0, column=0)
        label_trn_sport = ttk.Label(self, text='Select Tournament Sport')
        label_trn_sport.grid(row=0, column=1)

        button = ttk.Button(self, text='Delete', command=lambda: self._protected_delete_by_trn_sport(selected_option))
        button.grid(row=2, column=2)

    def delete_by_trn_prize(self):
        self.title('Delete Window')
        entry_trn_prize_bottom = ttk.Entry(self)
        entry_trn_prize_top = ttk.Entry(self)
        entry_trn_prize_bottom.grid(row=0, column=0)
        entry_trn_prize_top.grid(row=1, column=0)

        label_trn_prize_bottom = ttk.Label(self, text='Insert Tournament Prize Bottom')
        label_trn_prize_bottom.grid(row=0, column=1)
        label_trn_prize_bottom = ttk.Label(self, text='Insert Tournament Prize Top')
        label_trn_prize_bottom.grid(row=1, column=1)

        button = ttk.Button(self, text='Delete',
                            command=lambda: self._protected_delete_by_trn_prize(entry_trn_prize_bottom,
                                                                                entry_trn_prize_top))
        button.grid(row=2, column=2)

    def _protected_delete_by_trn_name(self, entry):
        trn_name: str = entry.get()
        if all([el.isalnum() for el in trn_name.split()]):
            source = {'db': sql_storage.delete_by_trn_name, 'xml': xml_storage.delete_by_trn_name}
            tournaments = source[self.storage](trn_name)
            if not tournaments:
                messagebox.showinfo('Bad News', 'There is no tournament with that name')
            else:
                self.destroy()
                messagebox.showinfo('Good News', f'{tournaments} tournaments were deleted')
        else:
            messagebox.showinfo('Bad News', f'Incorrect Tournament Name: {trn_name}')

    def _protected_delete_by_trn_sport(self, selected_option):
        sport = selected_option.get()
        source = {'db': sql_storage.delete_by_trn_sport, 'xml': xml_storage.delete_by_trn_sport}
        tournaments = source[self.storage](sport)
        self.destroy()
        messagebox.showinfo('Good News', f'{tournaments} tournaments were deleted')

    def _protected_delete_by_trn_prize(self, bottom, top):
        prize_bottom = bottom.get()
        prize_top = top.get()
        if prize_bottom.isdigit() and prize_top.isdigit():
            source = {'db': sql_storage.delete_by_trn_prize, 'xml': xml_storage.delete_by_trn_prize}
            tournaments = source[self.storage](int(prize_bottom), int(prize_top))
            if not tournaments:
                messagebox.showinfo('Bad News', 'There is no tournament with that prize')
            else:
                self.destroy()
                messagebox.showinfo('Good News', f'{tournaments} tournaments were deleted')
        else:
            messagebox.showinfo('Bad News', f'Incorrect Tournament Prize: {bottom, top}')
