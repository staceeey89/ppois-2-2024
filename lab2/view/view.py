import math
import tkinter as tk
from datetime import datetime
from tkinter import simpledialog, messagebox
from tkinter import ttk
from tkinter import filedialog
import os

from controller.controller import Controller
from model.sportsman import Sportsman
from model.enums import TypeOfSport, VolleyballPosition, BasketballPosition, FootballPosition, Category, Team
from model.exceptions import ViewException


class View:
    def __init__(self, controller: Controller):
        self.controller = controller

    def create_start_window(self):
        self.root = tk.Tk()
        self.limit_for_main_table = 10
        self.root.geometry("800x500")
        self.root.title("Sportsmen")
        self.f_for_buttons = tk.Frame(self.root)
        self.f_for_table = tk.Frame(self.root)
        self.f_for_pages_buttons = tk.Frame(self.root)

        self.f_for_buttons.place(relx=0.0, rely=0, relwidth=1, relheight=0.1)
        self.f_for_table.place(relx=0.5, rely=0.1, relwidth=1, relheight=0.8, anchor='n')
        self.f_for_pages_buttons.place(relx=0.0, rely=0.9, relwidth=1, relheight=0.1)
        self.offset_for_main_window = 0

        add_button = tk.Button(self.f_for_buttons, text="Add record", command=self.add_record_to_list)
        search_button = tk.Button(self.f_for_buttons, text="Find by attribute", command=self.open_search)
        delete_button = tk.Button(self.f_for_buttons, text="Delete by attribute", command=self.open_delete_window)
        add_to_db_button = tk.Button(self.f_for_buttons, text="Add to db", command=self.add_to_db)
        get_from_db_button = tk.Button(self.f_for_buttons, text="Get from db", command=self.get_from_db)
        add_to_xml_button = tk.Button(self.f_for_buttons, text="Add to xml", command=self.write_to_xml_file)
        get_from_xml_button = tk.Button(self.f_for_buttons, text="Get from xml", command=self.get_from_xml_file)
        show_tree_button = tk.Button(self.f_for_buttons, text="Show records in a tree view",
                                     command=self.show_records_as_tree)
        add_button.grid(row=0, column=0, padx=10, pady=10)
        search_button.grid(row=0, column=1, padx=10, pady=10)
        delete_button.grid(row=0, column=2, padx=10, pady=10)
        add_to_db_button.grid(row=0, column=3, padx=10, pady=10)
        get_from_db_button.grid(row=0, column=4, padx=10, pady=10)
        add_to_xml_button.grid(row=0, column=5, padx=10, pady=10)
        get_from_xml_button.grid(row=0, column=6, padx=10, pady=10)
        show_tree_button.grid(row=0, column=7, padx=10, pady=10)
        self.main_table = self.create_table(self.f_for_table)
        self.main_table.pack(expand=tk.YES, fill=tk.BOTH)
        next_page_button = tk.Button(self.f_for_pages_buttons, text="Next page",
                                     command=lambda: self.next_page(self.main_table))
        prev_page_button = tk.Button(self.f_for_pages_buttons, text="Previous page",
                                     command=lambda: self.prev_page(self.main_table))
        first_page_button = tk.Button(self.f_for_pages_buttons, text="First page",
                                      command=lambda: self.first_page(self.main_table))

        last_page_button = tk.Button(self.f_for_pages_buttons, text="Last page",
                                     command=lambda: self.last_page(self.main_table))
        self.current_page_label = tk.Label(self.f_for_pages_buttons, text=f"Current page: 0/0 Records: 0")
        update_limit_button = tk.Button(self.f_for_pages_buttons, text="Update LIMIT",
                                        command=self.update_limit)

        prev_page_button.grid(row=0, column=0, padx=10, pady=20)
        next_page_button.grid(row=0, column=1, padx=10, pady=20)
        first_page_button.grid(row=0, column=2, padx=10, pady=20)
        last_page_button.grid(row=0, column=3, padx=10, pady=20)
        self.current_page_label.grid(row=0, column=4, padx=10, pady=20)
        update_limit_button.grid(row=0, column=5, padx=10, pady=20)
        records = self.controller.get_records_with_offset_and_limit(self.limit_for_main_table, 0)
        self.update_table(self.main_table, records)
        self.update_page_number_label(self.offset_for_main_window, self.current_page_label, self.limit_for_main_table,
                                      self.controller.get_all_records())

        main_menu = tk.Menu(self.root)

        dropdown_menu = tk.Menu(main_menu, tearoff=0)

        dropdown_menu.add_command(label="Add record", command=self.add_record_to_list)
        dropdown_menu.add_command(label="Find by attribute", command=self.open_search)
        dropdown_menu.add_command(label="Delete by attribute", command=self.open_delete_window)
        dropdown_menu.add_command(label="Add to db", command=self.add_to_db)
        dropdown_menu.add_command(label="Get from db", command=self.get_from_db)
        dropdown_menu.add_command(label="Add to xml", command=self.write_to_xml_file)
        dropdown_menu.add_command(label="Get from xml", command=self.get_from_xml_file)
        dropdown_menu.add_command(label="Show records in a tree view", command=self.show_records_as_tree)

        main_menu.add_cascade(label="Menu", menu=dropdown_menu)

        self.root.config(menu=main_menu)

    def create_table(self, frame):
        heads = ["sportsman name", "team", "position", "titles", "type of sport", "category"]
        table = ttk.Treeview(frame, show="headings")
        table["columns"] = heads

        for header in heads:
            table.heading(header, text=header, anchor="center")
            table.column(header, anchor="center")

        return table

    def update_table(self, table, records: list[Sportsman]):
        table.delete(*table.get_children())
        if not records:
            return
        for record in records:
            table.insert('', 'end', values=(
                record.name, record.team.value, record.position.value,
                record.titles, record.type_of_sport.value, record.category.value))

    def add_record_to_list(self):
        self.open_add_record_window("list")

    def open_add_record_window(self, method: str):
        add_record_window = tk.Toplevel(self.root)
        add_record_window.title("Add record")

        position_options = {
            TypeOfSport.FOOTBALL.value: [position.value for position in FootballPosition],
            TypeOfSport.BASKETBALL.value: [position.value for position in BasketballPosition],
            TypeOfSport.VOLLEYBALL.value: [position.value for position in VolleyballPosition],
        }

        def update_position_options(event):
            selected_sport = self.type_of_sport_dropdown.get()
            if selected_sport:
                self.position_dropdown.config(values=position_options[selected_sport])
                self.position_dropdown.current(0)

        # sportsman name
        sportsman_name_label = tk.Label(add_record_window, text='Sportsman name')
        sportsman_name_label.grid(row=0, column=0, padx=10, pady=5, sticky='w')
        self.sportsman_name_entry = tk.Entry(add_record_window)
        self.sportsman_name_entry.grid(row=0, column=1, padx=10, pady=5, sticky='e')
        # team
        team_label = tk.Label(add_record_window, text='Team')
        team_label.grid(row=1, column=0, padx=10, pady=5, sticky='w')
        self.team_entry = tk.StringVar(add_record_window)
        self.team_dropdown = ttk.Combobox(add_record_window, values=[team.value for team in Team],
                                          textvariable=self.team_entry,
                                          state='readonly')
        self.team_dropdown.current(0)
        self.team_dropdown.grid(row=1, column=1, padx=10, pady=5, sticky='w')
        # position
        position_label = tk.Label(add_record_window, text='Position')
        position_label.grid(row=2, column=0, padx=10, pady=5, sticky='w')
        self.position_entry = tk.StringVar(add_record_window)
        self.position_dropdown = ttk.Combobox(add_record_window, values=position_options["FOOTBALL"],
                                              textvariable=self.position_entry,
                                              state='readonly')
        self.position_dropdown.current(0)
        self.position_dropdown.grid(row=2, column=1, padx=10, pady=5, sticky='w')
        # titles
        titles_label = tk.Label(add_record_window, text='Titles')
        titles_label.grid(row=3, column=0, padx=10, pady=5, sticky='w')
        self.titles_entry = tk.Entry(add_record_window)
        self.titles_entry.grid(row=3, column=1, padx=10, pady=5, sticky='e')
        # type_of_sport
        type_of_sport_label = tk.Label(add_record_window, text='Type of sport')
        type_of_sport_label.grid(row=4, column=0, padx=10, pady=5, sticky='w')
        self.type_of_sport_entry = tk.StringVar(add_record_window)
        self.type_of_sport_dropdown = ttk.Combobox(add_record_window,
                                                   values=[type_of_sport.value for type_of_sport in TypeOfSport],
                                                   textvariable=self.type_of_sport_entry,
                                                   state='readonly')
        self.type_of_sport_dropdown.current(0)
        self.type_of_sport_dropdown.grid(row=4, column=1, padx=10, pady=5, sticky='w')
        self.type_of_sport_dropdown.bind('<<ComboboxSelected>>', update_position_options)
        # category
        category_label = tk.Label(add_record_window, text='Category')
        category_label.grid(row=5, column=0, padx=10, pady=5, sticky='w')
        self.category_entry = tk.StringVar(add_record_window)
        self.category_dropdown = ttk.Combobox(add_record_window, values=[category.value for category in Category],
                                              textvariable=self.category_entry,
                                              state='readonly')
        self.category_dropdown.current(0)
        self.category_dropdown.grid(row=5, column=1, padx=10, pady=5, sticky='w')

        save_button = tk.Button(add_record_window, text="Save",
                                command=lambda: self.save_record(add_record_window, method))
        save_button.grid(row=6, column=0, columnspan=2, pady=10)

    def save_record(self, window_to_close, method: str):
        sportsman_name = self.sportsman_name_entry.get()
        team = self.team_dropdown.get()
        position = self.position_dropdown.get()
        titles = self.titles_entry.get()
        type_of_sport = self.type_of_sport_dropdown.get()
        category = self.category_dropdown.get()

        if sportsman_name and position:
            try:
                if method == "list":
                    self.controller.save_to_list(sportsman_name, team, position, titles, type_of_sport, category)
                elif method == "db":
                    self.controller.save_to_database(sportsman_name, team, position, titles, type_of_sport, category)
                elif method == "xml":
                    self.controller.save_to_xml(sportsman_name, team, position, titles, type_of_sport, category,
                                                self.xml_filename)
            except ViewException as e:
                messagebox.showerror("Error", str(e))
                window_to_close.destroy()
                return
        else:
            messagebox.showerror("Error", "All values are required")
            window_to_close.destroy()
            return

        self.first_page(self.main_table)
        messagebox.showinfo("Succeed", "Record saved successfully")
        window_to_close.destroy()

    def open_search(self):
        self.search_window = tk.Toplevel(self.root)
        self.search_window.title("Search Options")

        search_label = tk.Label(self.search_window, text="Choose search criteria:")
        search_label.pack()

        self.search_var = tk.StringVar(value="Name/Sport")
        self.search_options = ["Name/Sport", "Number of Titles", "Name/Category"]

        for option in self.search_options:
            tk.Radiobutton(self.search_window, text=option, variable=self.search_var, value=option).pack()

        next_button = tk.Button(self.search_window, text="Next", command=self.show_input_fields)
        next_button.pack()

    def show_input_fields(self):
        selected_option = self.search_var.get()

        for widget in self.search_window.winfo_children():
            widget.destroy()

        if selected_option == "Name/Sport":
            self.show_name_sport_fields()
        elif selected_option == "Number of Titles":
            self.show_number_of_titles_fields()
        elif selected_option == "Name/Category":
            self.show_name_category_fields()

    def show_name_sport_fields(self):
        self.method_for_search = 1
        tk.Label(self.search_window, text="Enter Name:").grid(row=0, column=0, padx=10, pady=5, sticky='e')
        self.name = tk.Entry(self.search_window)
        self.name.grid(row=0, column=1, padx=10, pady=5, sticky='e')
        tk.Label(self.search_window, text="Choose type of sport:").grid(row=1, column=0, padx=10, pady=5, sticky='e')

        self.type_of_sport_entry = tk.StringVar(self.search_window)
        self.type_of_sport_dropdown = ttk.Combobox(self.search_window,
                                                   values=[type_of_sport.value for type_of_sport in TypeOfSport],
                                                   textvariable=self.type_of_sport_entry,
                                                   state='readonly')
        self.type_of_sport_dropdown.current(0)
        self.type_of_sport_dropdown.grid(row=1, column=1, padx=10, pady=5, sticky='e')

        def find_for_search():
            self.name_for_search = self.name.get()
            self.type_of_sport_entry_for_search = self.type_of_sport_entry.get()
            self.open_search_window(
                self.controller.find_sportsman_by_name_or_sport(self.name_for_search,
                                                                self.type_of_sport_entry_for_search))

        tk.Button(self.search_window, text="Find", command=lambda: find_for_search()).grid(
            row=2,
            column=0,
            padx=10,
            pady=5,
            sticky='e')

    def show_number_of_titles_fields(self):
        self.method_for_search = 2
        lower_frame = tk.Frame(self.search_window)
        lower_frame.pack()
        tk.Label(lower_frame, text="Enter Lower Bound:").pack()
        self.lower_bound = tk.Entry(lower_frame)
        self.lower_bound.pack()

        upper_frame = tk.Frame(self.search_window)
        upper_frame.pack()
        tk.Label(upper_frame, text="Enter Upper Bound:").pack()
        self.upper_bound = tk.Entry(upper_frame)
        self.upper_bound.pack()

        def find_button_lambda():
            try:
                self.open_search_window(
                    self.controller.find_sportsman_by_titles(self.lower_bound.get(), self.upper_bound.get()))
            except ViewException as e:
                messagebox.showerror("Error", str(e))

        tk.Button(self.search_window, text="Find", command=lambda: find_button_lambda()).pack()

    def show_name_category_fields(self):
        self.method_for_search = 3
        tk.Label(self.search_window, text="Enter Name:").grid(row=0, column=0, padx=10, pady=5, sticky='e')
        self.name = tk.Entry(self.search_window)
        self.name.grid(row=0, column=1, padx=10, pady=5, sticky='e')
        tk.Label(self.search_window, text="Choose category:").grid(row=1, column=0, padx=10, pady=5, sticky='e')

        self.category_entry = tk.StringVar(self.search_window)
        self.category_dropdown = ttk.Combobox(self.search_window,
                                              values=[category.value for category in Category],
                                              textvariable=self.category_entry,
                                              state='readonly')
        self.category_dropdown.current(0)
        self.category_dropdown.grid(row=1, column=1, padx=10, pady=5, sticky='e')
        tk.Button(self.search_window, text="Find", command=lambda: self.open_search_window(
            self.controller.find_sportsman_by_name_or_category(self.name.get(), self.category_entry.get()))).grid(row=2,
                                                                                                                  column=0,
                                                                                                                  padx=10,
                                                                                                                  pady=5,
                                                                                                                  sticky='e')

    def open_search_window(self, records: list[Sportsman]):

        self.search_window.destroy()
        self.search_window = tk.Toplevel(self.root)
        self.search_window.geometry("800x500")
        self.search_window.title("Found records")

        self.offset_for_search = 1
        self.current_offset_for_page = -1
        total_height = 0.45
        frame_bottom = tk.Frame(self.search_window, width=450, height=600)
        frame_bottom.place(relx=0, rely=total_height, relwidth=1, relheight=0.8, anchor='w')
        self.search_table = self.create_table(frame_bottom)
        self.search_table.pack(expand=tk.YES, fill=tk.BOTH, anchor=tk.CENTER)

        frame_pages = tk.Frame(self.search_window, width=450, height=50)
        frame_pages.place(relx=0, rely=0.9, relwidth=1, relheight=0.1)

        prev_page_button = tk.Button(frame_pages, text="Previous page",
                                     command=lambda: self.prev_page_for_search(self.search_table))
        next_page_button = tk.Button(frame_pages, text="Next page",
                                     command=lambda: self.next_page_for_search(self.search_table))
        first_page_button = tk.Button(frame_pages, text="First page",
                                      command=lambda: self.first_page_for_search(self.search_table))

        last_page_button = tk.Button(frame_pages, text="Last page",
                                     command=lambda: self.last_page_for_search(self.search_table))

        self.current_page_label_for_search = tk.Label(frame_pages, text="Current page: 0")

        prev_page_button.grid(row=0, column=0, padx=10, pady=20)
        next_page_button.grid(row=0, column=1, padx=10, pady=20)
        first_page_button.grid(row=0, column=2, padx=10, pady=20)
        last_page_button.grid(row=0, column=3, padx=10, pady=20)
        self.current_page_label_for_search.grid(row=0, column=4, padx=10, pady=20)
        self.update_page_number_label(self.offset_for_search, self.current_page_label_for_search,
                                      self.limit_for_main_table,
                                      records)
        records = self.controller.get_all_records_for_search()
        self.next_page_for_search(self.search_table)
        self.search_window.mainloop()

    def open_delete_window(self):
        self.delete_window = tk.Toplevel(self.root)
        self.delete_window.title("Delete Options")

        search_label = tk.Label(self.delete_window, text="Choose search criteria:")
        search_label.pack()

        self.search_var = tk.StringVar(value="Name/Sport")
        self.search_options = ["Name/Sport", "Number of Titles", "Name/Category"]

        for option in self.search_options:
            tk.Radiobutton(self.delete_window, text=option, variable=self.search_var, value=option).pack()

        next_button = tk.Button(self.delete_window, text="Next", command=self.show_input_fields_for_delete)
        next_button.pack()

    def show_input_fields_for_delete(self):
        selected_option = self.search_var.get()

        for widget in self.delete_window.winfo_children():
            widget.destroy()

        if selected_option == "Name/Sport":
            self.show_name_sport_fields_for_delete()
        elif selected_option == "Number of Titles":
            self.show_number_of_titles_fields_for_delete()
        elif selected_option == "Name/Category":
            self.show_name_category_fields_for_delete()

    def show_name_sport_fields_for_delete(self):
        self.method_for_delete = 1
        tk.Label(self.delete_window, text="Enter Name:").grid(row=0, column=0, padx=10, pady=5, sticky='e')
        self.name = tk.Entry(self.delete_window)
        self.name.grid(row=0, column=1, padx=10, pady=5, sticky='e')
        tk.Label(self.delete_window, text="Choose type of sport:").grid(row=1, column=0, padx=10, pady=5, sticky='e')

        self.type_of_sport_entry = tk.StringVar(self.delete_window)
        self.type_of_sport_dropdown = ttk.Combobox(self.delete_window,
                                                   values=[type_of_sport.value for type_of_sport in TypeOfSport],
                                                   textvariable=self.type_of_sport_entry,
                                                   state='readonly')
        self.type_of_sport_dropdown.current(0)
        self.type_of_sport_dropdown.grid(row=1, column=1, padx=10, pady=5, sticky='e')

        def delete_button_lambda():
            i = self.controller.delete_records_by_name_or_sport(self.name.get(), self.type_of_sport_entry.get())
            self.first_page(self.main_table)
            messagebox.showinfo("Info", f"{i} rows were deleted")
            self.delete_window.destroy()

        tk.Button(self.delete_window, text="Delete", command=lambda: delete_button_lambda()).grid(
            row=2,
            column=0,
            padx=10,
            pady=5,
            sticky='e')

    def show_number_of_titles_fields_for_delete(self):
        self.method_for_delete = 2
        lower_frame = tk.Frame(self.delete_window)
        lower_frame.pack()
        tk.Label(lower_frame, text="Enter Lower Bound:").pack()
        self.lower_bound = tk.Entry(lower_frame)
        self.lower_bound.pack()

        upper_frame = tk.Frame(self.delete_window)
        upper_frame.pack()
        tk.Label(upper_frame, text="Enter Upper Bound:").pack()
        self.upper_bound = tk.Entry(upper_frame)
        self.upper_bound.pack()

        def delete_button_lambda():
            try:
                i = self.controller.delete_records_by_titles(self.lower_bound.get(), self.upper_bound.get())
                messagebox.showinfo("Info", f"{i} rows were deleted")
                self.first_page(self.main_table)
                self.delete_window.destroy()
            except ViewException as e:
                messagebox.showerror("Error", e.message)

        tk.Button(self.delete_window, text="Delete", command=lambda: delete_button_lambda()).pack()

    def show_name_category_fields_for_delete(self):
        self.method_for_delete = 3
        tk.Label(self.delete_window, text="Enter Name:").grid(row=0, column=0, padx=10, pady=5, sticky='e')
        self.name = tk.Entry(self.delete_window)
        self.name.grid(row=0, column=1, padx=10, pady=5, sticky='e')
        tk.Label(self.delete_window, text="Choose category:").grid(row=1, column=0, padx=10, pady=5, sticky='e')

        self.category_entry = tk.StringVar(self.delete_window)
        self.category_dropdown = ttk.Combobox(self.delete_window,
                                              values=[category.value for category in Category],
                                              textvariable=self.category_entry,
                                              state='readonly')
        self.category_dropdown.current(0)
        self.category_dropdown.grid(row=1, column=1, padx=10, pady=5, sticky='e')

        def delete_button_lambda():
            i = self.controller.delete_records_by_name_or_category(self.name.get(), self.category_entry.get())
            tk.messagebox.showinfo("Info", f"{i} rows were deleted.")
            self.first_page(self.main_table)
            self.delete_window.destroy()

        tk.Button(self.delete_window, text="Delete", command=lambda: delete_button_lambda()).grid(row=2,
                                                                                                 column=0,
                                                                                                 padx=10,
                                                                                                 pady=5,
                                                                                                 sticky='e')

    def start(self):
        self.create_start_window()
        self.root.mainloop()

    def next_page(self, table):
        records = self.controller.get_records_with_offset_and_limit(self.limit_for_main_table,
                                                                    self.offset_for_main_window)
        if len(records) == self.limit_for_main_table and len(
                self.controller.get_records_with_offset_and_limit(self.limit_for_main_table,
                                                                  self.offset_for_main_window + 1)) != 0:
            self.offset_for_main_window += 1
            records = self.controller.get_records_with_offset_and_limit(self.limit_for_main_table,
                                                                        self.offset_for_main_window)
        self.update_table(table, records)
        self.update_page_number_label(self.offset_for_main_window, self.current_page_label, self.limit_for_main_table,
                                      self.controller.get_all_records())

    def prev_page(self, table):
        if self.offset_for_main_window >= 1:
            self.offset_for_main_window -= 1
        records = self.controller.get_records_with_offset_and_limit(self.limit_for_main_table,
                                                                    self.offset_for_main_window)
        self.update_table(table, records)
        self.update_page_number_label(self.offset_for_main_window, self.current_page_label, self.limit_for_main_table,
                                      self.controller.get_all_records())

    def first_page(self, table):
        self.offset_for_main_window = 0
        records = self.controller.get_records_with_offset_and_limit(self.limit_for_main_table,
                                                                    self.offset_for_main_window)
        self.update_table(table, records)
        self.update_page_number_label(self.offset_for_main_window, self.current_page_label, self.limit_for_main_table,
                                      self.controller.get_all_records())

    def last_page(self, table):
        total_records = len(self.controller.get_all_records())
        last_offset = max(0, (total_records - 1) // self.limit_for_main_table)
        self.offset_for_main_window = last_offset
        records = self.controller.get_records_with_offset_and_limit(self.limit_for_main_table, last_offset)
        self.update_table(table, records)
        self.update_page_number_label(self.offset_for_main_window, self.current_page_label, self.limit_for_main_table,
                                      self.controller.get_all_records())

    def next_page_for_search(self, table):
        limit = self.limit_for_main_table
        all_records = self.controller.get_all_records_for_search()
        if (self.current_offset_for_page + 1) * limit < len(all_records):
            self.current_offset_for_page += 1
            self.update_table(table, self.controller.get_records_for_search_with_offset_and_limit(limit,
                                                                                                  self.current_offset_for_page))
            self.update_page_number_label(self.current_offset_for_page, self.current_page_label_for_search,
                                          self.limit_for_main_table, all_records)

    def prev_page_for_search(self, table):
        if self.current_offset_for_page > 0:
            self.current_offset_for_page -= 1
            all_records = self.controller.get_all_records_for_search()
            records = self.controller.get_records_for_search_with_offset_and_limit(self.limit_for_main_table,
                                                                                   self.current_offset_for_page)
            self.update_table(self.search_table, records)
            self.update_page_number_label(self.current_offset_for_page, self.current_page_label_for_search,
                                          self.limit_for_main_table, all_records)

    def first_page_for_search(self, table):
        self.current_offset_for_page = 0
        records = self.controller.get_records_for_search_with_offset_and_limit(self.limit_for_main_table, 0)
        all_records = self.controller.get_all_records_for_search()
        self.update_table(self.search_table, records)
        self.update_page_number_label(self.current_offset_for_page, self.current_page_label_for_search,
                                      self.limit_for_main_table, all_records)

    def last_page_for_search(self, table):
        total_records = len(self.controller.get_all_records_for_search())
        last_offset = max(0, (total_records - 1) // self.limit_for_main_table)
        self.current_offset_for_page = last_offset
        self.offset_for_main_window = last_offset
        records = self.controller.get_records_for_search_with_offset_and_limit(self.limit_for_main_table, last_offset)
        self.update_table(table, records)
        self.update_page_number_label(last_offset, self.current_page_label_for_search, self.limit_for_main_table,
                                      self.controller.get_all_records_for_search())

    def add_to_db(self):
        self.open_add_record_window("db")

    def get_from_db(self):
        self.controller.set_list_from_database()
        self.update_table(self.main_table, self.controller.get_records_with_offset_and_limit(self.limit_for_main_table,
                                                                                             0))
        self.update_page_number_label(self.offset_for_main_window, self.current_page_label, self.limit_for_main_table,
                                      self.controller.get_all_records())
        self.first_page(self.main_table)

    def get_from_xml_file(self):
        filename = filedialog.askopenfilename(initialdir="/", title="Select XML File",
                                              filetypes=(("XML files", "*.xml"), ("All files", "*.*")))
        if not filename:
            return
        self.controller.set_list_from_xml(filename)
        self.update_table(self.main_table, self.controller.get_records_with_offset_and_limit(self.limit_for_main_table,
                                                                                             0))
        self.update_page_number_label(self.offset_for_main_window, self.current_page_label, self.limit_for_main_table,
                                      self.controller.get_all_records())
        self.first_page(self.main_table)

    def write_to_xml_file(self):
        filename = filedialog.askopenfilename(initialdir="/", title="Select XML File",
                                              filetypes=(("XML files", "*.xml"), ("All files", "*.*")))

        if not filename:
            return

        self.xml_filename = filename
        self.open_add_record_window("xml")

    def create_record_treeview(self, records):
        record_treeview_window = tk.Toplevel(self.root)
        record_treeview_window.geometry("600x400")
        record_treeview_window.title("Records Treeview")

        treeview = ttk.Treeview(record_treeview_window, columns=("Value"))
        treeview.heading("#0", text="Field")
        treeview.heading("Value", text="Value")
        treeview.pack(expand=True, fill=tk.BOTH)

        for record in records:
            record_node = treeview.insert("", "end")

            sportsman_node = treeview.insert(record_node, "end", text="Sportsman")
            treeview.insert(sportsman_node, "end", text="Name", values=(record.name,))

            info_node = treeview.insert(record_node, "end", text="Sportsman info")
            treeview.insert(info_node, "end", text="Team", values=(record.team.value,))
            treeview.insert(info_node, "end", text="Position", values=(record.position.value,))
            treeview.insert(info_node, "end", text="Titles", values=(record.titles,))
            treeview.insert(info_node, "end", text="Type of sport", values=(record.type_of_sport.value,))
            treeview.insert(info_node, "end", text="Category", values=(record.category.value,))

    def show_records_as_tree(self):
        records = self.controller.get_all_records()
        self.create_record_treeview(records)

    def update_page_number_label(self, page, label, limit, records):
        if not records:
            records = []
        pages = math.ceil(len(records) / limit)
        if pages == 0:
            label.config(text=f"Current page: 0/0 Records: 0")
        else:
            label.config(text=f"Current page: {page + 1}/{pages} Records: {len(records)}")

    def update_limit(self):
        new_limit = simpledialog.askinteger("LIMIT", "Enter new LIMIT value:")
        if new_limit is not None and int(new_limit) > 0:
            self.limit_for_main_table = new_limit
        self.first_page(self.main_table)
