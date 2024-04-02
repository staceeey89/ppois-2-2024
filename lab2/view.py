import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from tkinter import messagebox
from search_student import Search
from delete_student import Delete
import pymysql.cursors
import xml.sax


class StudentTable(Delete, Search):
    def __init__(self, main_window, db_config_param):
        super().__init__(main_window, db_config_param)

        self.main_window = main_window
        self.student_id = 1
        self.table = None
        self.table_data = []
        self.current_page = 1
        self.page_size = 10
        self.total_pages = 1
        self.setup_window()
        self.main_frame = ttk.Frame(self.main_window)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.button_frame = None
        self.first_page_button = None
        self.prev_page_button = None
        self.next_page_button = None
        self.last_page_button = None
        self.delete_button = None
        self.search_button = None
        self.add_button = None
        self.file_button = None
        self.page_info_label = None
        self.page_size_label = None
        self.page_size_entry = None
        self.page_size_button = None
        self.show_tree_button = None

        self.host = db_config_param['host']
        self.user = db_config_param['user']
        self.password = db_config_param['password']
        self.database = db_config_param['database']

        self.setup_buttons()

        self.setup_table()

        self.fetch_students_from_db()

        self.update_main_table()

        self.setup_page_buttons()

    def setup_page_buttons(self):
        self.page_info_label = ttk.Label(self.main_frame, text="")
        self.page_info_label.pack(side=tk.BOTTOM, padx=10, pady=10)

        self.page_size_label = ttk.Label(self.main_frame, text="Записей на странице:")
        self.page_size_label.pack(side=tk.BOTTOM, padx=10, pady=5)

        self.page_size_entry = ttk.Entry(self.main_frame)
        self.page_size_entry.insert(0, str(self.page_size))
        self.page_size_entry.pack(side=tk.BOTTOM, padx=10, pady=5)

        self.page_size_button = ttk.Button(self.main_frame, text="Изменить", command=self.change_page_size)
        self.page_size_button.pack(side=tk.BOTTOM, padx=10, pady=5)

        self.update_page_info()

        self.show_tree_button = ttk.Button(self.button_frame, text="Показать в виде дерева",
                                           command=self.show_tree_view)
        self.show_tree_button.grid(row=0, column=8, padx=5, pady=5)

    def setup_window(self):
        self.main_window.resizable(False, False)
        screen_width = self.main_window.winfo_screenwidth()
        screen_height = self.main_window.winfo_screenheight()

        window_width = 1500
        window_height = 300
        x_position = (screen_width - window_width) // 2
        y_position = (screen_height - window_height) // 2

        self.main_window.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

    def setup_table(self):
        self.main_frame = ttk.Frame(self.main_window)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Создаем таблицу
        self.table = ttk.Treeview(self.main_frame, columns=(
            "ID", "Фамилия", "Имя", "Отчество",
            "Группа", "1 сем(общ. раб)", "2 сем(общ. раб)", "3 сем(общ. раб)", "4 сем(общ. раб)",
            "5 сем(общ. раб)", "6 сем(общ. раб)", "7 сем(общ. раб)", "8 сем(общ. раб)"), show="headings")
        self.table.heading("ID", text="ID")
        self.table.heading("Фамилия", text="Фамилия")
        self.table.heading("Имя", text="Имя")
        self.table.heading("Отчество", text="Отчество")
        self.table.heading("Группа", text="Группа")
        for i in range(1, 9):
            self.table.heading(f"{i} сем(общ. раб)", text=f"{i} сем(общ. раб)")

        self.table.column("ID", width=50, anchor=tk.CENTER)
        self.table.column("Фамилия", width=100, anchor=tk.CENTER)
        self.table.column("Имя", width=100, anchor=tk.CENTER)
        self.table.column("Отчество", width=100, anchor=tk.CENTER)
        self.table.column("Группа", width=100, anchor=tk.CENTER)
        for i in range(1, 9):
            self.table.column(f"{i} сем(общ. раб)", width=100, anchor=tk.CENTER)

        self.table.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def setup_buttons(self):
        self.button_frame = ttk.Frame(self.main_frame)
        self.button_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

        self.first_page_button = ttk.Button(self.button_frame, text="Первая", command=self.go_to_first_page)
        self.first_page_button.grid(row=0, column=0, padx=5, pady=5)

        self.prev_page_button = ttk.Button(self.button_frame, text="Предыдущая", command=self.go_to_previous_page)
        self.prev_page_button.grid(row=0, column=1, padx=5, pady=5)

        self.next_page_button = ttk.Button(self.button_frame, text="Следующая", command=self.go_to_next_page)
        self.next_page_button.grid(row=0, column=2, padx=5, pady=5)

        self.last_page_button = ttk.Button(self.button_frame, text="Последняя", command=self.go_to_last_page)
        self.last_page_button.grid(row=0, column=3, padx=5, pady=5)

        self.delete_button = ttk.Button(self.button_frame, text="Удалить", command=self.delete_students)
        self.delete_button.grid(row=0, column=4, padx=5, pady=5)

        self.search_button = ttk.Button(self.button_frame, text="Поиск", command=self.search_students)
        self.search_button.grid(row=0, column=5, padx=5, pady=5)

        self.add_button = ttk.Button(self.button_frame, text="Добавить студента", command=self.add_student)
        self.add_button.grid(row=0, column=6, padx=5, pady=5)

        self.file_button = ttk.Button(self.button_frame, text="Считать с файла xml", command=self.load_data_from_xml)
        self.file_button.grid(row=0, column=7, padx=5, pady=5)

        self.file_button = ttk.Button(self.button_frame, text="Загрузить в файл xml", command=self.save_student_to_xml)
        self.file_button.grid(row=0, column=9, padx=5, pady=5)

    def show_tree_view(self):
        tree_view_dialog = tk.Toplevel(self.main_window)
        tree_view_dialog.title("Дерево записей")
        tree_view_dialog.geometry("800x600")

        tree = ttk.Treeview(tree_view_dialog)
        tree.pack(fill=tk.BOTH, expand=True)

        root_node = tree.insert("", tk.END, text="Студенты")

        for student_row in self.table_data:
            student_info = (f"{student_row['last_name']} {student_row['first_name']} {student_row['middle_name']} - "
                            f"{student_row['group_name']}")
            student_node = tree.insert(root_node, tk.END, text=student_info)
            tree.insert(student_node, tk.END, text=f"1 сем(общ. раб): {student_row['sem1_public_works']}")
            tree.insert(student_node, tk.END, text=f"2 сем(общ. раб): {student_row['sem2_public_works']}")
            tree.insert(student_node, tk.END, text=f"3 сем(общ. раб): {student_row['sem3_public_works']}")
            tree.insert(student_node, tk.END, text=f"4 сем(общ. раб): {student_row['sem4_public_works']}")
            tree.insert(student_node, tk.END, text=f"5 сем(общ. раб): {student_row['sem5_public_works']}")
            tree.insert(student_node, tk.END, text=f"6 сем(общ. раб): {student_row['sem6_public_works']}")
            tree.insert(student_node, tk.END, text=f"7 сем(общ. раб): {student_row['sem7_public_works']}")
            tree.insert(student_node, tk.END, text=f"8 сем(общ. раб): {student_row['sem8_public_works']}")

        tree_view_dialog.mainloop()

    def load_data_from_xml(self):
        filename = filedialog.askopenfilename(title="Выберите XML файл", filetypes=(("XML files", "*.xml"),))
        if filename:
            try:
                xml_handler = StudentXMLHandler(self)
                parser = xml.sax.make_parser()
                parser.setContentHandler(xml_handler)
                parser.parse(filename)

                self.fetch_students_from_db()

                messagebox.showinfo("Успех", "Данные успешно загружены из файла.")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Ошибка загрузки файла: {e}")

    def save_student_to_xml(self):
        try:
            selected_item = self.table.selection()
            if not selected_item:
                messagebox.showerror("Ошибка", "Пожалуйста, выберите студента.")
                return

            student_id = self.table.item(selected_item)['values'][0]

            filename = filedialog.asksaveasfilename(
                title="Сохранить данные студента как XML",
                defaultextension=".xml",
                filetypes=(("XML files", "*.xml"),)
            )

            if filename:
                with open(filename, 'w') as file:
                    file.write('<?xml version="1.0" encoding="UTF-8"?>\n')
                    file.write('<students>\n')
                    host = 'localhost'
                    user = 'lupach'
                    password = '228'
                    database = 'kek'
                    connection = pymysql.connect(
                        host=host,
                        user=user,
                        password=password,
                        database=database,
                        cursorclass=pymysql.cursors.DictCursor
                    )

                    try:
                        with connection.cursor() as cursor:
                            sql_select_student = "SELECT * FROM students WHERE id = %s"
                            cursor.execute(sql_select_student, student_id)
                            student_data = cursor.fetchone()

                            if student_data:
                                file.write('\t<student>\n')
                                for key, value in student_data.items():
                                    file.write(f'\t\t<{key}>{value}</{key}>\n')
                                file.write('\t</student>\n')
                    except pymysql.Error as e:
                        print(f"Ошибка при получении данных студента из базы данных: {e}")
                    finally:
                        connection.close()

                    file.write('</students>\n')
                    messagebox.showinfo("Успех", "Данные студента успешно сохранены в XML файл.")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка сохранения данных студента в XML файл: {e}")

    def update_page_info(self):
        total_records = len(self.table_data)
        start_index = (self.current_page - 1) * self.page_size + 1
        end_index = min(start_index + self.page_size - 1, total_records)
        self.page_info_label.config(
            text=f"Страница {self.current_page}/{self.total_pages}, " +
                 f"Отображается {start_index}-{end_index} из {total_records} записей")

    def change_page_size(self):
        try:
            new_page_size = int(self.page_size_entry.get())
            if new_page_size <= 0:
                messagebox.showerror("Ошибка", "Число записей на странице должно быть положительным.")
                return
            self.page_size = new_page_size
            self.update_table_with_pagination()
            self.update_page_info()
        except ValueError:
            messagebox.showerror("Ошибка", "Пожалуйста, введите корректное число записей на странице.")

    def update_table_with_pagination(self):
        start_index = (self.current_page - 1) * self.page_size
        end_index = min(start_index + self.page_size, len(self.table_data))

        for row in self.table.get_children():
            self.table.delete(row)

        for student_row in self.table_data[start_index:end_index]:
            student_values = [student_row['id'], student_row['last_name'], student_row['first_name'],
                              student_row['middle_name'], student_row['group_name'],
                              student_row['sem1_public_works'], student_row['sem2_public_works'],
                              student_row['sem3_public_works'], student_row['sem4_public_works'],
                              student_row['sem5_public_works'], student_row['sem6_public_works'],
                              student_row['sem7_public_works'], student_row['sem8_public_works']]
            self.table.insert("", tk.END, values=student_values)

        self.total_pages = (len(self.table_data) + self.page_size - 1) // self.page_size

        self.update_page_control_buttons()

        self.update_page_info()

    def update_page_control_buttons(self):
        self.total_pages = (len(self.table_data) + self.page_size - 1) // self.page_size

        self.first_page_button.config(state="normal" if self.current_page > 1 else "disabled")
        self.prev_page_button.config(state="normal" if self.current_page > 1 else "disabled")
        self.next_page_button.config(state="normal" if self.current_page < self.total_pages else "disabled")
        self.last_page_button.config(state="normal" if self.current_page < self.total_pages else "disabled")

    def go_to_first_page(self):
        self.current_page = 1
        self.update_table_with_pagination()

    def go_to_previous_page(self):
        self.current_page -= 1
        self.update_table_with_pagination()

    def go_to_next_page(self):
        self.current_page += 1
        self.update_table_with_pagination()

    def go_to_last_page(self):
        self.current_page = self.total_pages
        self.update_table_with_pagination()

    def fetch_students_from_db(self):
        connection = pymysql.connect(host=self.host,
                                     user=self.user,
                                     password=self.password,
                                     database=self.database,
                                     cursorclass=pymysql.cursors.DictCursor)

        try:
            with connection.cursor() as cursor:
                sql_select_students = """
                SELECT * FROM students
                """
                cursor.execute(sql_select_students)
                self.table_data = cursor.fetchall()
                self.update_main_table()

        except pymysql.Error as e:
            print(f"Ошибка при получении списка студентов из базы данных: {e}")

        finally:
            connection.close()

    def update_main_table(self):
        for row in self.table.get_children():
            self.table.delete(row)

        for student_row in self.table_data:
            student_values = [student_row['id'], student_row['last_name'], student_row['first_name'],
                              student_row['middle_name'], student_row['group_name'],
                              student_row['sem1_public_works'], student_row['sem2_public_works'],
                              student_row['sem3_public_works'], student_row['sem4_public_works'],
                              student_row['sem5_public_works'], student_row['sem6_public_works'],
                              student_row['sem7_public_works'], student_row['sem8_public_works']]
            self.table.insert("", tk.END, values=student_values)

    def add_student_to_db(self, student_data):
        connection = pymysql.connect(host=self.host,
                                     user=self.user,
                                     password=self.password,
                                     database=self.database,
                                     cursorclass=pymysql.cursors.DictCursor)

        try:
            with connection.cursor() as cursor:
                sql_insert_student = """
                INSERT INTO students (last_name, first_name, middle_name, group_name, 
                sem1_public_works, sem2_public_works, sem3_public_works, sem4_public_works, 
                sem5_public_works, sem6_public_works, sem7_public_works, sem8_public_works) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(sql_insert_student, student_data)
                connection.commit()
                messagebox.showinfo("Успех", "Студент успешно добавлен в базу данных.")

        except pymysql.Error as e:
            print(f"Ошибка при добавлении студента в базу данных: {e}")
            messagebox.showerror("Ошибка", "Произошла ошибка при добавлении студента в базу данных.")

        finally:
            connection.close()

    def add_to_table(self, last_name_entry, first_name_entry, middle_name_entry, group_entry, semester_entries,
                     student_dialog):
        last_name = last_name_entry.get()
        first_name = first_name_entry.get()
        middle_name = middle_name_entry.get()
        group_name = group_entry.get()

        if not group_name:
            messagebox.showerror("Ошибка", "Пожалуйста, введите номер группы.")
            return

        semester_values_data = []
        for entry in semester_entries:
            semester_value = entry.get()
            if not semester_value:
                semester_value = "0"
            semester_values_data.append(semester_value)

        student_data = (last_name, first_name, middle_name, group_name, *semester_values_data)
        self.add_student_to_db(student_data)
        self.fetch_students_from_db()
        student_dialog.destroy()

    def add_student(self):
        student_dialog = tk.Toplevel(self.main_window)
        student_dialog.title("Добавление студента")
        student_dialog.geometry("320x450")

        ttk.Label(student_dialog, text="Фамилия:").grid(row=0, column=0, padx=5, pady=5)
        ttk.Label(student_dialog, text="Имя:").grid(row=1, column=0, padx=5, pady=5)
        ttk.Label(student_dialog, text="Отчество:").grid(row=2, column=0, padx=5, pady=5)
        ttk.Label(student_dialog, text="Группа:").grid(row=3, column=0, padx=5, pady=5)

        last_name_entry = ttk.Entry(student_dialog)
        first_name_entry = ttk.Entry(student_dialog)
        middle_name_entry = ttk.Entry(student_dialog)
        group_entry = ttk.Entry(student_dialog)

        last_name_entry.grid(row=0, column=1, padx=5, pady=5)
        first_name_entry.grid(row=1, column=1, padx=5, pady=5)
        middle_name_entry.grid(row=2, column=1, padx=5, pady=5)
        group_entry.grid(row=3, column=1, padx=5, pady=5)

        semester_entries = []
        for i in range(1, 9):
            label = ttk.Label(student_dialog, text=f"{i} сем(общ. раб):")
            label.grid(row=i + 3, column=0, padx=5, pady=5)
            entry = ttk.Entry(student_dialog)
            entry.grid(row=i + 3, column=1, padx=5, pady=5)
            semester_entries.append(entry)

        add_button = ttk.Button(student_dialog, text="Добавить",
                                command=lambda: self.add_to_table(last_name_entry, first_name_entry, middle_name_entry,
                                                                  group_entry, semester_entries, student_dialog))
        add_button.grid(row=12, column=0, columnspan=2, pady=10)


class StudentXMLHandler(xml.sax.ContentHandler):
    def __init__(self, student_table_instance):
        super().__init__()
        self.student_table = student_table_instance
        self.current_data = ""
        self.student_info = {}
        self.students_data = []

    def startElement(self, tag, attributes):
        self.current_data = tag
        if tag == "student":
            self.student_info = {}

    def characters(self, content):
        if self.current_data in self.student_info:
            self.student_info[self.current_data] += content
        else:
            self.student_info[self.current_data] = content

    def endElement(self, tag):
        if tag == "student":
            self.students_data.append((
                self.student_info.get("last_name", ""),
                self.student_info.get("first_name", ""),
                self.student_info.get("middle_name", ""),
                self.student_info.get("group_name", ""),
                self.student_info.get("sem1_public_works", ""),
                self.student_info.get("sem2_public_works", ""),
                self.student_info.get("sem3_public_works", ""),
                self.student_info.get("sem4_public_works", ""),
                self.student_info.get("sem5_public_works", ""),
                self.student_info.get("sem6_public_works", ""),
                self.student_info.get("sem7_public_works", ""),
                self.student_info.get("sem8_public_works", ""),
            ))

    def endDocument(self):
        for data in self.students_data:
            self.student_table.add_student_to_db(data)


if __name__ == "__main__":
    root = tk.Tk()
    my_table = ttk.Treeview(root)
    my_table_data = []
    db_config = {'host': 'localhost', 'user': 'lupach', 'password': '228', 'database': 'kek'}

    app = StudentTable(root, db_config)
    app.fetch_students_from_db()
    root.mainloop()
