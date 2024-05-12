import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
from model.model import StudentModel


class StudentAttendanceView(tk.Tk):
    def __init__(self, db_file_path, controller):
        super().__init__()
        self.page_size_entry = None
        self.next_page_button = None
        self.page_label = None
        self.prev_page_button = None
        self.pagination_frame = None
        self.tree_view = None
        self.main_frame = None
        self.page_size_var = None
        self.toolbar = None
        self.menu_bar = None
        self.title("Учет посещаемости студентов")
        self.geometry("1300x470")

        self.controller = controller
        self.model = StudentModel(db_file_path)
        self.db_conn = sqlite3.connect(db_file_path)

        self.page_size = tk.IntVar(value=20)
        self.current_page = 1

        self.create_menu()
        self.create_toolbar()
        self.create_main_window()

        self.create_pagination_buttons()
        self.fill_treeview_from_db()

    def create_menu(self):
        self.menu_bar = tk.Menu(self)

        file_menu = tk.Menu(self.menu_bar, tearoff=0)
        file_menu.add_command(label="Загрузить из файла", command=self.load_from_file)
        file_menu.add_command(label="Сохранить в файл", command=self.save_to_file)
        file_menu.add_separator()
        file_menu.add_command(label="Выход", command=self.quit)
        self.menu_bar.add_cascade(label="Файл", menu=file_menu)

        view_menu = tk.Menu(self.menu_bar, tearoff=0)
        view_menu.add_command(label="Дерево данных", command=self.show_tree_window)
        self.menu_bar.add_cascade(label="Вид", menu=view_menu)

        self.config(menu=self.menu_bar)

    def create_toolbar(self):
        self.toolbar = tk.Frame(self, bd=1, relief=tk.RAISED)

        search_button = tk.Button(self.toolbar, text="Найти", command=self.search_records)
        search_button.pack(side=tk.LEFT, padx=2, pady=2)

        add_button = tk.Button(self.toolbar, text="Добавить", command=self.add_record)
        add_button.pack(side=tk.LEFT, padx=2, pady=2)

        delete_button = tk.Button(self.toolbar, text="Удалить", command=self.delete_records)
        delete_button.pack(side=tk.LEFT, padx=2, pady=2)

        self.toolbar.pack(side=tk.TOP, fill=tk.X)

    def create_main_window(self):
        self.main_frame = tk.Frame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.tree_view = ttk.Treeview(self.main_frame, columns=("fio", "group", "sick_absent", "other_absent",
                                                                "unexcused_absent", "total_absent"))
        self.tree_view.heading("#0", text="ID")
        self.tree_view.heading("fio", text="ФИО студента")
        self.tree_view.heading("group", text="Группа")
        self.tree_view.heading("sick_absent", text="Пропуски по болезни")
        self.tree_view.heading("other_absent", text="Пропуски по другим причинам")
        self.tree_view.heading("unexcused_absent", text="Пропуски без уважительной причины")
        self.tree_view.heading("total_absent", text="Итого пропусков")
        self.tree_view.column("#0", width=0)
        self.tree_view.column("fio", width=140, anchor="center")
        self.tree_view.column("group", width=10, anchor="center")
        self.tree_view.column("sick_absent", width=70, anchor="center")
        self.tree_view.column("other_absent", width=120, anchor="center")
        self.tree_view.column("unexcused_absent", width=120, anchor="center")
        self.tree_view.column("total_absent", width=60, anchor="center")
        self.tree_view.pack(fill=tk.BOTH, expand=True)

    def show_tree_window(self):
        tree_window = tk.Toplevel()
        tree_window.title("Дерево данных")

        tree = ttk.Treeview(tree_window)
        tree.pack(fill="both", expand=True)

        rows = self.model.fetch_students()
        for row in rows:
            student_node = tree.insert('', 'end', text=row[0])
            tree.insert(student_node, 'end', text=f"ФИО студента: {row[1]}")
            tree.insert(student_node, 'end', text=f"Группа: {row[2]}")
            tree.insert(student_node, 'end', text=f"Пропуски по болезни: {row[3]}")
            tree.insert(student_node, 'end', text=f"Пропуски по другим причинам: {row[4]}")
            tree.insert(student_node, 'end', text=f"Пропуски без уважительной причины: {row[5]}")
            tree.insert(student_node, 'end', text=f"Итого пропусков: {row[3] + row[4] + row[5]}")

    def show_prev_page(self):
        if self.current_page > 1:
            self.current_page -= 1
            self.fill_treeview_from_db()
            self.update_pagination_buttons()

    def show_next_page(self):
        self.current_page += 1
        self.fill_treeview_from_db()
        self.update_pagination_buttons()

    def go_to_first_page(self):
        self.current_page = 1
        self.fill_treeview_from_db()
        self.update_pagination_buttons()

    def go_to_last_page(self):

        total_records = self.model.count_students()
        total_pages = (total_records + self.page_size.get() - 1) // self.page_size.get()
        self.current_page = total_pages
        self.fill_treeview_from_db()
        self.update_pagination_buttons()

    def create_pagination_buttons(self):
        self.pagination_frame = tk.Frame(self.main_frame)
        self.pagination_frame.pack(side=tk.BOTTOM, pady=10)

        first_page_button = tk.Button(self.pagination_frame, text="<<", command=self.go_to_first_page)
        first_page_button.pack(side=tk.LEFT, padx=10)

        self.prev_page_button = tk.Button(self.pagination_frame, text="<", command=self.show_prev_page)
        self.prev_page_button.pack(side=tk.LEFT, padx=10)

        self.page_label = tk.Label(self.pagination_frame, text="")
        self.page_label.pack(side=tk.LEFT, padx=10)

        self.next_page_button = tk.Button(self.pagination_frame, text=">", command=self.show_next_page)
        self.next_page_button.pack(side=tk.LEFT, padx=10)

        last_page_button = tk.Button(self.pagination_frame, text=">>", command=self.go_to_last_page)
        last_page_button.pack(side=tk.LEFT, padx=10)

        page_size_label = tk.Label(self.pagination_frame, text="Записей на странице:")
        page_size_label.pack(side=tk.LEFT, padx=10)
        self.page_size_var = tk.StringVar(value="20")
        page_size_entry = tk.Entry(self.pagination_frame, textvariable=self.page_size_var, width=5)
        page_size_entry.pack(side=tk.LEFT, padx=2)
        change_button = tk.Button(self.pagination_frame, text="Изменить", command=self.change_page_size)
        change_button.pack(side=tk.LEFT, padx=2)

        self.update_pagination_buttons()

    def update_pagination_buttons(self):
        if self.current_page <= 1:
            self.prev_page_button.config(state=tk.DISABLED)
        else:
            self.prev_page_button.config(state=tk.NORMAL)

        total_records = self.model.count_students()

        total_pages = (total_records + self.page_size.get() - 1) // self.page_size.get()

        if self.current_page >= total_pages:
            self.next_page_button.config(state=tk.DISABLED)
        else:
            self.next_page_button.config(state=tk.NORMAL)

        self.page_label.config(text=f"{self.current_page} / {total_pages}")

    def update_page_size(self):
        self.current_page = 1
        self.fill_treeview_from_db()
        self.update_pagination_buttons()

    def change_page_size(self):
        try:
            new_page_size = int(self.page_size_var.get())
            if new_page_size > 0:
                self.page_size.set(new_page_size)
                self.update_page_size()
            else:
                messagebox.showerror("Ошибка", "Количество записей на странице должно быть положительным числом.")
        except ValueError:
            messagebox.showerror("Ошибка", "Пожалуйста, введите корректное число.")

    def fill_treeview_from_db(self):
        start_index = (self.current_page - 1) * int(self.page_size_var.get())
        self.current_page * int(self.page_size_var.get())

        for record in self.tree_view.get_children():
            self.tree_view.delete(record)

        cursor = self.db_conn.cursor()
        cursor.execute('''SELECT * FROM students LIMIT ?, ?''', (start_index, int(self.page_size_var.get())))
        rows = cursor.fetchall()
        for row in rows:
            self.tree_view.insert('', 'end', text=row[0],
                                  values=(row[1], row[2], row[3], row[4], row[5], row[3] + row[4] + row[5]))

    def search_records(self):
        absent_types = ["По болезни", "По другим причинам", "Без уважительной причины"]
        search_window = tk.Toplevel(self)
        search_window.title("Поиск записей")

        frame1 = tk.Frame(search_window, borderwidth=2, relief="groove", bg="")
        frame1.pack(padx=10, pady=10, anchor="w")

        search_group_var = tk.BooleanVar()
        search_group_checkbox = tk.Checkbutton(frame1, variable=search_group_var)
        search_group_checkbox.grid(row=0, column=0, sticky="w")

        tk.Label(frame1, text="По номеру группы или фамилии студента:").grid(row=0, column=1, sticky="w")

        tk.Label(frame1, text="Фамилия:").grid(row=1, column=0, sticky="w")
        search_name_entry = tk.Entry(frame1)
        search_name_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(frame1, text="Группа:").grid(row=2, column=0, sticky="w")
        search_group_entry = tk.Entry(frame1)
        search_group_entry.grid(row=2, column=1, padx=5, pady=5)

        frame2 = tk.Frame(search_window, borderwidth=2, relief="groove", bg="")
        frame2.pack(padx=10, pady=10, anchor="w")

        search_absent_var = tk.BooleanVar()
        search_absent_checkbox = tk.Checkbutton(frame2, text="По фамилии студента и типу пропуска",
                                                variable=search_absent_var)
        search_absent_checkbox.grid(row=0, column=0, sticky="w")

        search_absent_type_var = tk.StringVar()
        tk.Label(frame2, text="Фамилия:").grid(row=1, column=0, sticky="w")
        search_absent_entry = tk.Entry(frame2)
        search_absent_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(frame2, text="Тип пропуска:").grid(row=2, column=0, sticky="w")
        search_absent_type_combobox = ttk.Combobox(frame2, values=absent_types, textvariable=search_absent_type_var,
                                                   state="readonly", width=20)
        search_absent_type_combobox.grid(row=2, column=1, padx=5, pady=5)
        search_absent_type_combobox.state(['disabled'])

        def toggle_combobox_absent_state():
            if search_absent_var.get():
                search_absent_type_combobox.state(['!disabled'])
            else:
                search_absent_type_combobox.state(['disabled'])

        search_absent_var.trace_add('write', lambda *args: toggle_combobox_absent_state())

        frame3 = tk.Frame(search_window, borderwidth=2, relief="groove", bg="")
        frame3.pack(padx=10, pady=10, anchor="w")

        search_absent_count_var = tk.BooleanVar()
        search_absent_count_checkbox = tk.Checkbutton(frame3, text="По фамилии студента и кол. пропусков",
                                                      variable=search_absent_count_var)
        search_absent_count_checkbox.grid(row=0, column=0, sticky="w")

        search_absent_count_type_var = tk.StringVar()
        tk.Label(frame3, text="Фамилия:").grid(row=1, column=0, sticky="w")
        search_absent_count_entry = tk.Entry(frame3)
        search_absent_count_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(frame3, text="Тип пропуска:").grid(row=2, column=0, sticky="w")
        search_absent_count_type_combobox = ttk.Combobox(frame3, values=absent_types,
                                                         textvariable=search_absent_count_type_var, state="readonly",
                                                         width=20)
        search_absent_count_type_combobox.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(frame3, text="Нижний предел:").grid(row=3, column=0, sticky="w")
        search_absent_count_lower_entry = tk.Entry(frame3)
        search_absent_count_lower_entry.grid(row=3, column=1, padx=5, pady=5)

        tk.Label(frame3, text="Верхний предел:").grid(row=4, column=0, sticky="w")
        search_absent_count_upper_entry = tk.Entry(frame3)
        search_absent_count_upper_entry.grid(row=4, column=1, padx=5, pady=5)
        search_absent_count_type_combobox.state(['disabled'])

        def toggle_combobox_absent_count_state():
            if search_absent_count_var.get():
                search_absent_count_type_combobox.state(['!disabled'])
            else:
                search_absent_count_type_combobox.state(['disabled'])

        search_absent_count_var.trace_add('write', lambda *args: toggle_combobox_absent_count_state())

        def perform_search():
            cursor = self.db_conn.cursor()
            sql_query = "SELECT * FROM students WHERE "

            if search_group_var.get():
                group_num = search_group_entry.get()
                sql_query += f"group_num = '{group_num}' AND "

            if search_name_entry.get():
                name = search_name_entry.get()
                sql_query += f"fio LIKE '%{name}%' AND "

            if search_absent_var.get():
                name = search_absent_entry.get()
                absent_type = search_absent_type_combobox.get()
                if absent_type == "По болезни":
                    sql_query += f"fio LIKE '%{name}%' AND sick_absent > 0 AND "
                elif absent_type == "По другим причинам":
                    sql_query += f"fio LIKE '%{name}%' AND other_absent > 0 AND "
                elif absent_type == "Без уважительной причины":
                    sql_query += f"fio LIKE '%{name}%' AND unexcused_absent > 0 AND "

            if search_absent_count_var.get():
                name = search_absent_count_entry.get()
                absent_type = search_absent_count_type_combobox.get()
                lower_limit = search_absent_count_lower_entry.get()
                upper_limit = search_absent_count_upper_entry.get()

                if lower_limit and upper_limit:
                    if absent_type == "По болезни":
                        sql_query += f"fio LIKE '%{name}%' AND sick_absent BETWEEN {lower_limit} AND {upper_limit} AND "
                    elif absent_type == "По другим причинам":
                        sql_query += (f"fio LIKE '%{name}%' AND other_absent BETWEEN {lower_limit} AND "
                                      f"{upper_limit} AND ")
                    elif absent_type == "Без уважительной причины":
                        sql_query += (f"fio LIKE '%{name}%' AND unexcused_absent BETWEEN {lower_limit} "
                                      f"AND {upper_limit} AND ")
                elif lower_limit:
                    if absent_type == "По болезни":
                        sql_query += f"fio LIKE '%{name}%' AND sick_absent >= {lower_limit} AND "
                    elif absent_type == "По другим причинам":
                        sql_query += f"fio LIKE '%{name}%' AND other_absent >= {lower_limit} AND "
                    elif absent_type == "Без уважительной причины":
                        sql_query += f"fio LIKE '%{name}%' AND unexcused_absent >= {lower_limit} AND "
                elif upper_limit:
                    if absent_type == "По болезни":
                        sql_query += f"fio LIKE '%{name}%' AND sick_absent <= {upper_limit} AND "
                    elif absent_type == "По другим причинам":
                        sql_query += f"fio LIKE '%{name}%' AND other_absent <= {upper_limit} AND "
                    elif absent_type == "Без уважительной причины":
                        sql_query += f"fio LIKE '%{name}%' AND unexcused_absent <= {upper_limit} AND "

            if sql_query.endswith("AND "):
                sql_query = sql_query[:-5]

            cursor.execute(sql_query)
            rows = cursor.fetchall()

            result_window = tk.Toplevel(search_window)
            result_window.title("Результаты поиска")

            if not rows:
                result_label = tk.Label(result_window, text="Ничего не найдено", fg="red")
                result_label.pack()
            else:
                result_text = tk.Text(result_window)
                result_text.pack(fill="both", expand=True)
                for row in rows:
                    result_text.insert(tk.END,
                                       f"ФИО: {row[1]}\nГруппа: {row[2]}\nПо болезни:"
                                       f" {row[3]}\nПо другим причинам: {row[4]}"
                                       f"\nБез уважительной причины: {row[5]}\n\n")

        def toggle_search_button_state():
            if (search_group_var.get() or search_name_entry.get() or search_absent_var.get() or
                    search_absent_count_var.get()):
                delete_button.config(state=tk.NORMAL)
            else:
                delete_button.config(state=tk.DISABLED)

        search_group_var.trace_add('write', lambda *args: toggle_search_button_state())
        search_absent_var.trace_add('write', lambda *args: toggle_search_button_state())
        search_absent_count_var.trace_add('write', lambda *args: toggle_search_button_state())
        delete_button = tk.Button(search_window, text="Найти", command=perform_search, state=tk.DISABLED)
        delete_button.pack(pady=10)
        toggle_search_button_state()

    def add_record(self):
        def toggle_save_button_state():
            if (fio_entry.get() and group_entry.get() and sick_absent_entry.get() and other_absent_entry.get() and
                    unexcused_absent_entry.get()):
                save_button.config(state=tk.NORMAL)
            else:
                save_button.config(state=tk.DISABLED)

        def save_record():
            fio = fio_entry.get()
            group = group_entry.get()
            sick_absent = sick_absent_entry.get()
            other_absent = other_absent_entry.get()
            unexcused_absent = unexcused_absent_entry.get()

            self.model.insert_student(fio, group, sick_absent, other_absent, unexcused_absent)
            messagebox.showinfo("Успех", "Запись добавлена успешно")

            add_window.destroy()
            self.fill_treeview_from_db()

        add_window = tk.Toplevel(self)
        add_window.title("Добавить запись")

        fio_label = tk.Label(add_window, text="ФИО:")
        fio_label.grid(row=0, column=0, sticky="w")
        fio_entry = tk.Entry(add_window)
        fio_entry.grid(row=0, column=1, padx=5, pady=5)

        group_label = tk.Label(add_window, text="Группа:")
        group_label.grid(row=1, column=0, sticky="w")
        group_entry = tk.Entry(add_window)
        group_entry.grid(row=1, column=1, padx=5, pady=5)

        sick_absent_label = tk.Label(add_window, text="Пропуски по болезни:")
        sick_absent_label.grid(row=2, column=0, sticky="w")
        sick_absent_entry = tk.Entry(add_window)
        sick_absent_entry.grid(row=2, column=1, padx=5, pady=5)

        other_absent_label = tk.Label(add_window, text="Пропуски по другим причинам:")
        other_absent_label.grid(row=3, column=0, sticky="w")
        other_absent_entry = tk.Entry(add_window)
        other_absent_entry.grid(row=3, column=1, padx=5, pady=5)

        unexcused_absent_label = tk.Label(add_window, text="Пропуски без уважительной причины:")
        unexcused_absent_label.grid(row=4, column=0, sticky="w")
        unexcused_absent_entry = tk.Entry(add_window)
        unexcused_absent_entry.grid(row=4, column=1, padx=5, pady=5)

        save_button = tk.Button(add_window, text="Сохранить", command=save_record, state=tk.DISABLED)
        save_button.grid(row=5, columnspan=2, pady=10)

        fio_entry.bind("<KeyRelease>", lambda event: toggle_save_button_state())
        group_entry.bind("<KeyRelease>", lambda event: toggle_save_button_state())
        sick_absent_entry.bind("<KeyRelease>", lambda event: toggle_save_button_state())
        other_absent_entry.bind("<KeyRelease>", lambda event: toggle_save_button_state())
        unexcused_absent_entry.bind("<KeyRelease>", lambda event: toggle_save_button_state())

        toggle_save_button_state()

    def delete_records(self):
        absent_types = ["По болезни", "По другим причинам", "Без уважительной причины"]
        delete_window = tk.Toplevel(self)
        delete_window.title("Удаление записей")

        frame1 = tk.Frame(delete_window, borderwidth=2, relief="groove", bg="")
        frame1.pack(padx=10, pady=10, anchor="w")

        search_group_var = tk.BooleanVar()
        search_group_checkbox = tk.Checkbutton(frame1, variable=search_group_var)
        search_group_checkbox.grid(row=0, column=0, sticky="w")

        tk.Label(frame1, text="По номеру группы и фамилии студента:").grid(row=0, column=1, sticky="w")

        tk.Label(frame1, text="Фамилия:").grid(row=1, column=0, sticky="w")
        search_name_entry = tk.Entry(frame1)
        search_name_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(frame1, text="Группа:").grid(row=2, column=0, sticky="w")
        search_group_entry = tk.Entry(frame1)
        search_group_entry.grid(row=2, column=1, padx=5, pady=5)

        frame2 = tk.Frame(delete_window, borderwidth=2, relief="groove", bg="")
        frame2.pack(padx=10, pady=10, anchor="w")

        search_absent_var = tk.BooleanVar()
        search_absent_checkbox = tk.Checkbutton(frame2, text="По фамилии студента и типу пропуска",
                                                variable=search_absent_var)
        search_absent_checkbox.grid(row=0, column=0, sticky="w")

        search_absent_type_var = tk.StringVar()
        tk.Label(frame2, text="Фамилия:").grid(row=1, column=0, sticky="w")
        search_absent_entry = tk.Entry(frame2)
        search_absent_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(frame2, text="Тип пропуска:").grid(row=2, column=0, sticky="w")
        search_absent_type_combobox = ttk.Combobox(frame2, values=absent_types, textvariable=search_absent_type_var,
                                                   state="readonly", width=20)
        search_absent_type_combobox.grid(row=2, column=1, padx=5, pady=5)
        search_absent_type_combobox.state(['disabled'])

        def toggle_combobox_absent_state():
            if search_absent_var.get():
                search_absent_type_combobox.state(['!disabled'])
            else:
                search_absent_type_combobox.state(['disabled'])

        search_absent_var.trace_add('write', lambda *args: toggle_combobox_absent_state())

        frame3 = tk.Frame(delete_window, borderwidth=2, relief="groove", bg="")
        frame3.pack(padx=10, pady=10, anchor="w")

        search_absent_count_var = tk.BooleanVar()
        search_absent_count_checkbox = tk.Checkbutton(frame3, text="По фамилии студента и кол. пропусков",
                                                      variable=search_absent_count_var)
        search_absent_count_checkbox.grid(row=0, column=0, sticky="w")

        search_absent_count_type_var = tk.StringVar()
        tk.Label(frame3, text="Фамилия:").grid(row=1, column=0, sticky="w")
        search_absent_count_entry = tk.Entry(frame3)
        search_absent_count_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(frame3, text="Тип пропуска:").grid(row=2, column=0, sticky="w")
        search_absent_count_type_combobox = ttk.Combobox(frame3, values=absent_types,
                                                         textvariable=search_absent_count_type_var, state="readonly",
                                                         width=20)
        search_absent_count_type_combobox.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(frame3, text="Нижний предел:").grid(row=3, column=0, sticky="w")
        search_absent_count_lower_entry = tk.Entry(frame3)
        search_absent_count_lower_entry.grid(row=3, column=1, padx=5, pady=5)

        tk.Label(frame3, text="Верхний предел:").grid(row=4, column=0, sticky="w")
        search_absent_count_upper_entry = tk.Entry(frame3)
        search_absent_count_upper_entry.grid(row=4, column=1, padx=5, pady=5)
        search_absent_count_type_combobox.state(['disabled'])

        def toggle_combobox_absent_count_state():
            if search_absent_count_var.get():
                search_absent_count_type_combobox.state(['!disabled'])
            else:
                search_absent_count_type_combobox.state(['disabled'])

        search_absent_count_var.trace_add('write', lambda *args: toggle_combobox_absent_count_state())

        def perform_deletion():
            cursor = self.db_conn.cursor()
            sql_query = "DELETE FROM students WHERE "

            if search_group_var.get():
                group_num = search_group_entry.get()
                sql_query += f"group_num = '{group_num}' AND "

            if search_name_entry.get():
                name = search_name_entry.get()
                sql_query += f"fio LIKE '%{name}%' AND "

            if search_absent_var.get():
                name = search_absent_entry.get()
                absent_type = search_absent_type_combobox.get()
                if absent_type == "По болезни":
                    sql_query += f"fio LIKE '%{name}%' AND sick_absent > 0 AND "
                elif absent_type == "По другим причинам":
                    sql_query += f"fio LIKE '%{name}%' AND other_absent > 0 AND "
                elif absent_type == "Без уважительной причины":
                    sql_query += f"fio LIKE '%{name}%' AND unexcused_absent > 0 AND "

            if search_absent_count_var.get():
                name = search_absent_count_entry.get()
                absent_type = search_absent_count_type_combobox.get()
                lower_limit = search_absent_count_lower_entry.get()
                upper_limit = search_absent_count_upper_entry.get()

                if lower_limit and upper_limit:
                    if absent_type == "По болезни":
                        sql_query += f"fio LIKE '%{name}%' AND sick_absent BETWEEN {lower_limit} AND {upper_limit} AND "
                    elif absent_type == "По другим причинам":
                        sql_query += (f"fio LIKE '%{name}%' AND other_absent BETWEEN {lower_limit} AND "
                                      f"{upper_limit} AND ")
                    elif absent_type == "Без уважительной причины":
                        sql_query += (f"fio LIKE '%{name}%' AND unexcused_absent BETWEEN {lower_limit} "
                                      f"AND {upper_limit} AND ")
                elif lower_limit:
                    if absent_type == "По болезни":
                        sql_query += f"fio LIKE '%{name}%' AND sick_absent >= {lower_limit} AND "
                    elif absent_type == "По другим причинам":
                        sql_query += f"fio LIKE '%{name}%' AND other_absent >= {lower_limit} AND "
                    elif absent_type == "Без уважительной причины":
                        sql_query += f"fio LIKE '%{name}%' AND unexcused_absent >= {lower_limit} AND "
                elif upper_limit:
                    if absent_type == "По болезни":
                        sql_query += f"fio LIKE '%{name}%' AND sick_absent <= {upper_limit} AND "
                    elif absent_type == "По другим причинам":
                        sql_query += f"fio LIKE '%{name}%' AND other_absent <= {upper_limit} AND "
                    elif absent_type == "Без уважительной причины":
                        sql_query += f"fio LIKE '%{name}%' AND unexcused_absent <= {upper_limit} AND "

            if sql_query.endswith("AND "):
                sql_query = sql_query[:-5]

            cursor.execute(sql_query)
            self.db_conn.commit()

            self.fill_treeview_from_db()

            deleted_count = cursor.rowcount

            if deleted_count == 0:
                messagebox.showerror("Ошибка", "Ничего не найдено", icon="error")

            self.fill_treeview_from_db()
            delete_window.destroy()

            delete_window.destroy()

        def toggle_delete_button_state():
            if (search_group_var.get() or search_name_entry.get() or search_absent_var.get() or
                    search_absent_count_var.get()):
                delete_button.config(state=tk.NORMAL)
            else:
                delete_button.config(state=tk.DISABLED)

        search_group_var.trace_add('write', lambda *args: toggle_delete_button_state())
        search_absent_var.trace_add('write', lambda *args: toggle_delete_button_state())
        search_absent_count_var.trace_add('write', lambda *args: toggle_delete_button_state())
        delete_button = tk.Button(delete_window, text="Удалить", command=perform_deletion, state=tk.DISABLED)
        delete_button.pack(pady=10)
        toggle_delete_button_state()

    def load_from_file(self):
        self.controller.load_from_file()

    def save_to_file(self):
        self.controller.save_to_file()

    def insert_data_into_table(self, students_data):
        self.tree_view.delete(*self.tree_view.get_children())
        for student in students_data:
            self.tree_view.insert('', 'end', text=student['id'],
                                  values=(student['fio'], student['group'],
                                          student['sick_absent'], student['other_absent'],
                                          student['unexcused_absent'], int(student['sick_absent']) +
                                          int(student['other_absent']) + int(student['unexcused_absent'])))

    def get_students_data_from_treeview(self):
        students_data = self.model.fetch_students()
        students_data = [{'id': row[0], 'fio': row[1], 'group': row[2],
                          'sick_absent': row[3], 'other_absent': row[4], 'unexcused_absent': row[5]}
                         for row in students_data]
        return students_data
