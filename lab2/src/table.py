import tkinter as tk

class TableView:
    def __init__(self, root, data, page_number,x_table,y_table,page_size): #x320 y200
        self.x_table = x_table
        self.y_table = y_table
        self.root = root
        self.data = data
        self.pages = page_number - 1
        self.current_page = 0
        self.page_size = page_size

        self.label = tk.Label(self.root, text="РАСПИСАНИЕ", font=("Times New Roman", 20, "bold"), borderwidth=1,
                              relief="solid")
        self.label.place(x=x_table, y=y_table-40)

        self.text_widget = tk.Text(self.root, wrap="none", relief="solid")
        self.text_widget.place(height=165, width=600, x=x_table, y=y_table)

        self.first_button = tk.Button(self.root, text="Первая", command=self.first_page, borderwidth=1, relief="solid")
        self.first_button.place(x=x_table, y=y_table+172)

        self.prev_button = tk.Button(self.root, text="Предыдущая", command=self.prev_page, borderwidth=1, relief="solid")
        self.prev_button.place(x=x_table+54, y=y_table+172)

        self.next_button = tk.Button(self.root, text="Следующая", command=self.next_page, borderwidth=1, relief="solid")
        self.next_button.place(x=x_table+141, y=y_table+172)

        self.last_button = tk.Button(self.root, text="Последняя", command=self.last_page, borderwidth=1, relief="solid")
        self.last_button.place(x=x_table+222, y=y_table+172)
        self.label_table = tk.Label()
        self.update_text()
        self.print_table_info(x_table,y_table)

    def print_table_info(self,x_table,y_table):
        self.label_table.destroy()
        if self.current_page != self.pages:
            current = self.page_size
        else:
            current = len(self.data) % self.page_size
            if current == 0:
                current = self.page_size
        if len(self.data) == 0:
            current = 0
        if self.pages == -1:
            self.current_page = -1
        self.label_table = tk.Label(self.root, text=f"Страница {self.current_page + 1}/{self.pages+1} ({current}/{len(self.data)})",
                                    borderwidth=1, relief="solid")
        self.label_table.place(x=x_table+483,y=y_table+172)
    def update_text(self):
        start_index = self.current_page * self.page_size
        end_index = start_index + self.page_size
        page_data = self.data[start_index:end_index]
        text = "\n".join(page_data)
        self.text_widget.delete("1.0", "end")
        self.text_widget.insert("1.0", text)

    def first_page(self):
        if (0) * self.page_size < len(self.data):
            self.current_page = 0
            self.update_text()
        self.print_table_info(self.x_table, self.y_table)

    def last_page(self):
        if (self.pages) * self.page_size < len(self.data):
            self.current_page = self.pages
            self.update_text()
        self.print_table_info(self.x_table, self.y_table)

    def next_page(self):
        if (self.current_page + 1) * self.page_size < len(self.data):
            self.current_page += 1
            self.update_text()
        self.print_table_info(self.x_table, self.y_table)

    def prev_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.update_text()
        self.print_table_info(self.x_table,self.y_table)

    def destroy(self):
        self.label.destroy()
        self.text_widget.destroy()
        self.first_button.destroy()
        self.prev_button.destroy()
        self.last_button.destroy()
        self.next_button.destroy()
        self.label_table.destroy()