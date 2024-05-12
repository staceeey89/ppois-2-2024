import shutil
import tkinter as tk
import tkinter.filedialog
from tkinter import filedialog
import os
from tkinter import messagebox
from View.AddStudentDialog import AddStudentDialog
from View.DeleteDialog import DeleteDialog
from View.AddGroupDialog import AddGroupDialog
from View.SearchDialog import SearchDialog
from View.ShowTable import ShowTable
from Model.StudentsDB import StudentsDB

class MainDialog:
    def __init__(self, controller):
        self.controller = controller
        self.root = tk.Tk()
        self.root.title("Главная")
        self.root.state('zoomed')
        self.root.minsize(800, 600)

        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        # Create File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Файл", menu=file_menu)
        file_menu.add_command(label="Сохранить в XML", command=self.__save_to_xml)
        file_menu.add_command(label="Загрузить из XML", command=self.__load_from_xml)
        file_menu.add_command(label="Сохранить в sqlite3", command=self.__save_data)
        file_menu.add_command(label="Загрузить sqlite3", command=self.__load_data)
        file_menu.add_separator()
        file_menu.add_command(label="Выход", command=self.root.quit)

        # Create Actions menu
        actions_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Действия", menu=actions_menu)
        actions_menu.add_command(label="Добавить студента", command=self.__add_student)
        actions_menu.add_command(label="Удалить студента", command=self.__delete_student)
        actions_menu.add_command(label="Добавить группу", command=self.__add_group)
        actions_menu.add_command(label="Поиск", command=self.__search)

        self.file_label = tk.Label(self.root, text="")
        self.file_label.pack()

        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(expand=True, fill='both')

        self.table = ShowTable(self.main_frame, controller, self.controller.get_all_data())
        self.table.pack(expand=True, fill='both')

        add_button = tk.Button(self.main_frame, text="Добавить студента", command=self.__add_student)
        add_button.pack()

        delete_button = tk.Button(self.main_frame, text="Удалить студента", command=self.__delete_student)
        delete_button.pack()

        add_group_button = tk.Button(self.main_frame, text="Добавить группу", command=self.__add_group)
        add_group_button.pack()

        search_button = tk.Button(self.main_frame, text="Поиск", command=self.__search)
        search_button.pack()

        save_button = tk.Button(self.main_frame, text="Сохранить в XML", command=self.__save_to_xml)
        save_button.pack()

        load_button = tk.Button(self.main_frame, text="Загрузить в XML", command=self.__load_from_xml)
        load_button.pack()

        self.save_button = tk.Button(self.root, text="Сохранить в sqlite3", command=self.__save_data)
        self.save_button.pack()

        self.load_button = tk.Button(self.root, text="Загрузить в sqlite3", command=self.__load_data)
        self.load_button.pack()

        self.new_file_button = tk.Button(self.root, text="Новый файл", command=self.__create_new_file)
        self.new_file_button.pack()
        self.file_label.config(text="Файл не выбран")
        self.root.mainloop()

    def __call(self):
        self.table.set_data(self.controller.get_all_data())

    def __add_student(self):
        if self.controller.open_page("AddStudentDialog"):
            AddStudentDialog(self.controller,self.__call)

    def __delete_student(self):
        if self.controller.open_page("DeleteDialog"):
            DeleteDialog(self.controller, self.__call)

    def __add_group(self):
        if self.controller.open_page("AddGroupDialog"):
            AddGroupDialog(self.controller)

    def __search(self):
        if self.controller.open_page("SearchDialog"):
            SearchDialog(self.controller)

    def __save_to_xml(self):
        database = self.controller.database
        if database is None:
            tk.messagebox.showerror("Ошибка", "База данных не была открыта.")
            return
        file_path = tk.filedialog.asksaveasfilename(defaultextension=".xml")
        if file_path:
            self.controller.database.export_all_tables_to_xml(file_path)
            messagebox.showinfo("Сохранение", "Данные успешно сохранены в XML файл.")

    def __load_from_xml(self):
        file_path = tk.filedialog.askopenfilename(filetypes=[("XML files", "*.xml")])
        if file_path:
            if self.controller.database is None:
                db_file_name = os.path.splitext(file_path)[0] + ".db"
                self.controller.database = StudentsDB(db_file_name)
                self.__update_file_label(file_path)
                self.table.set_data(self.controller.get_all_data())
            self.controller.database.import_all_tables_from_xml(file_path)
            messagebox.showinfo("Загрузка", "Данные успешно загружены из XML файла.")
            self.table.set_data(self.controller.get_all_data())
            self.update_file_label(file_path)

    def __save_data(self):
        if self.controller.database is None:
            tk.messagebox.showerror("Ошибка", "База данных не была открыта.")
            return
        dest_file_path = filedialog.asksaveasfilename(defaultextension=".db", filetypes=[("SQLite Database", "*.db")])
        if not dest_file_path:
            return
        try:
            cursor = self.controller.database.conn.cursor()
            cursor.execute("PRAGMA database_list;")
            database_info = cursor.fetchone()
            src_file_path = database_info[2]
            cursor.close()

            shutil.copyfile(src_file_path, dest_file_path)
            tk.messagebox.showinfo("Успех", "База данных успешно сохранена.")
        except Exception as e:
            tk.messagebox.showerror("Ошибка", f"Произошла ошибка при сохранении базы данных: {str(e)}")

    def __load_data(self):
        file_path = filedialog.askopenfilename(filetypes=[("SQLite Database", "*.db")])

        if file_path:
            self.controller.database = StudentsDB(file_path)
            self.__update_file_label(file_path)
            self.table.set_data(self.controller.get_all_data())


    def __create_new_file(self):
        file_path = tk.filedialog.asksaveasfilename(defaultextension=".db", filetypes=[("SQLite Database", "*.db")])
        if file_path:
            self.controller.database=StudentsDB(file_path)
            self.table.set_data(self.controller.get_all_data())
            self.__update_file_label(file_path)
            messagebox.showinfo("Успех", f"Файл успешно создан по пути: {file_path}")


    def __update_file_label(self, file_path):
        filename = os.path.basename(file_path)
        self.file_label.config(text=f"Выбранный файл: {filename}")

