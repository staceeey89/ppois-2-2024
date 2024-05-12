import tkinter as tk
from tkinter import messagebox

class PaginationControl(tk.Frame):
    def __init__(self, parent, table_widget, items_per_page):
        super().__init__(parent)
        self.table = table_widget
        self.items_per_page = items_per_page
        self.current_page = 1

        self.total_items_label = tk.Label(self, text=f"Total Items: {self.table.items_count}")
        self.total_items_label.grid(row=0, column=0)

        self.page_info_label = tk.Label(self, text=f"Page {self.current_page} of {self.calculate_total_pages()}")
        self.page_info_label.grid(row=0, column=1)

        self.prev_button = tk.Button(self, text="Prev", command=self.prev_page)
        self.prev_button.grid(row=0, column=2)

        self.next_button = tk.Button(self, text="Next", command=self.next_page)
        self.next_button.grid(row=0, column=3)

        self.items_per_page_label = tk.Label(self, text="Items per Page:")
        self.items_per_page_label.grid(row=0, column=4)

        self.items_per_page_entry = tk.Entry(self, width=5)
        self.items_per_page_entry.insert(0, str(self.items_per_page))
        self.items_per_page_entry.grid(row=0, column=5)

        self.items_per_page_button = tk.Button(self, text="Update", command=self.update_items_per_page)
        self.items_per_page_button.grid(row=0, column=6)

        self.first_page_button = tk.Button(self, text="First", command=self.go_to_first_page)
        self.first_page_button.grid(row=0, column=7)

        self.last_page_button = tk.Button(self, text="Last", command=self.go_to_last_page)
        self.last_page_button.grid(row=0, column=8)

        self.radio_var = tk.IntVar()
        self.radio_var.set(1)
        self.show_table_mode = 1

        tk.Radiobutton(self, text="Таблица",
                    variable=self.radio_var, value="1",
                    command=lambda: self.change_show_table_mode(1)).grid(row=0, column=9, sticky=tk.W)
        tk.Radiobutton(self, text="Дерево",
                    variable=self.radio_var, value="2",
                    command=lambda: self.change_show_table_mode(2)).grid(row=0, column=10, sticky=tk.W)

        self.update_table()



    def change_show_table_mode(self, value):
        if not value == self.show_table_mode:
            self.show_table_mode = value
            self.update_table()

    def update_pagination_info(self):
        total_pages = self.calculate_total_pages()
        self.page_info_label.config(text=f"Page {self.current_page} of {total_pages}")

    def prev_page(self):
        if self.current_page > 1:
            self.current_page -= 1
            self.update_table()
            self.update_pagination_info()

    def next_page(self):
        total_pages = self.calculate_total_pages()
        if self.current_page < total_pages:
            self.current_page += 1
            self.update_table()
            self.update_pagination_info()

    def go_to_first_page(self):
        self.current_page = 1
        self.update_table()
        self.update_pagination_info()

    def go_to_last_page(self):
        total_pages = self.calculate_total_pages()
        self.current_page = total_pages
        self.update_table()
        self.update_pagination_info()

    def calculate_total_pages(self):
        total_items = self.table.items_count
        return (total_items + self.items_per_page - 1) // self.items_per_page

    def update_items_per_page(self):
        new_items_per_page_str = self.items_per_page_entry.get()
        if not new_items_per_page_str.isdigit():
            messagebox.showerror("Ошибка", "Введите число", parent=self.root)
            return

        new_items_per_page = int(new_items_per_page_str)
        if new_items_per_page <= 0:
            messagebox.showerror("Ошибка", "Число должно быть не отрицательным",parent=self.root)
            return

        if new_items_per_page != self.items_per_page:
            self.items_per_page = new_items_per_page
            self.current_page = 1
            self.update_table()
            self.update_pagination_info()

    def update_table(self):
        start_index = (self.current_page - 1) * self.items_per_page
        end_index = start_index + self.items_per_page
        self.table.load_data(start_index, end_index, self.show_table_mode==2)
