from tkinter import messagebox, filedialog
from model.model import StudentModel
from view.view import StudentAttendanceView
from controller.xml_parser import XMLParser, XMLWriter


class StudentAttendanceController:
    def __init__(self, db_file_path):
        self.model = StudentModel(db_file_path)
        self.view = StudentAttendanceView(db_file_path, self)

        self.view.load_from_file_handler = self.load_from_file
        self.view.save_to_file_handler = self.save_to_file
        self.view.show_tree_window_handler = self.show_tree_window
        self.view.search_records_handler = self.search_records
        self.view.add_record_handler = self.add_record
        self.view.delete_records_handler = self.delete_records
        self.view.change_page_size_handler = self.change_page_size
        self.view.quit_handler = self.quit

    def load_from_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("XML files", "*.xml")])
        if file_path:
            try:
                students_data = XMLParser.parse(file_path)
                self.view.insert_data_into_table(students_data)
                self.model.update_students(students_data)
                messagebox.showinfo("Успех", "Данные успешно загружены из файла.")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Ошибка загрузки файла: {str(e)}")

    def save_to_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".xml", filetypes=[("XML files", "*.xml")])
        if file_path:
            students_data = self.view.get_students_data_from_treeview()
            try:
                XMLWriter.save(file_path, students_data)
                messagebox.showinfo("Успех", "Данные успешно сохранены в файле.")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Ошибка сохранения файла: {str(e)}")

    def show_tree_window(self):
        self.view.show_tree_window()

    def search_records(self):
        self.view.search_records()

    def add_record(self):
        self.view.add_record()

    def delete_records(self):
        self.view.delete_records()

    def change_page_size(self):
        self.view.change_page_size()

    def quit(self):
        self.model.close_connection()
        self.view.quit()
