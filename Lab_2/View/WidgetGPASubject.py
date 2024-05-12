import tkinter as tk
from tkinter import messagebox
from typing import List

class WidgetGPASubgect(tk.Frame):
    def __init__(self,controller,mode='search',tablewidget = None, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.master =  master
        self.table = tablewidget
        self.controller = controller
        self.mode = mode
        self.min_label = tk.Label(self, text="Минимальный средний бал:")
        self.min_entry = tk.Entry(self)
        self.min_label.grid(row=0, column=0, sticky="w")
        self.min_entry.grid(row=0, column=1, sticky="w")

        self.max_label = tk.Label(self, text="Максимальный средний бал:")
        self.max_entry = tk.Entry(self)
        self.max_label.grid(row=1, column=0, sticky="w")
        self.max_entry.grid(row=1, column=1, sticky="w")

        self.subject_label = tk.Label(self, text="Предмет:")
        self.subject_label.grid(row=2, column=0, sticky="w")

        self.subject_listbox = tk.Listbox(self)

        all_subjects = self.controller.database.get_exam_names()
        for subject in all_subjects:
            self.subject_listbox.insert(tk.END, subject)
        self.subject_listbox.grid(row=3, column=0, columnspan=2, sticky="nsew")
        button_text = "Найти" if mode == 'search' else "Удалить"
        self.find_button = tk.Button(self, text=button_text, command=self.find)
        self.find_button.grid(row=4, column=0, columnspan=2, sticky="nsew")

    def find(self)->List[int]:
        try:
            self.controller.validate_grades(self.min_entry.get(),self.max_entry.get())
            min_grade_str = self.min_entry.get()
            max_grade_str = self.max_entry.get()

            min_grade = float(min_grade_str)
            max_grade = float(max_grade_str)

            selected_item = self.subject_listbox.curselection()
            if selected_item:
                selected_item = self.subject_listbox.get(selected_item[0])
                list_id= self.controller.database.get_students_by_average_grade_range(min_grade, max_grade, selected_item)
                if len(list_id) ==0:
                    messagebox.showinfo("внимание", "записи по данному запросу не найдены",parent=self.master)
                else:
                    if self.mode =='search' and not self.table is None:
                        self.table.set_data(list_id)
                    elif self.mode =='delete':
                        self.controller.delete_student(list_id,self.master)
            else:
                messagebox.showerror("Ошибка", "Выберите предмет.",parent=self.master)
        except ValueError as e:
            error_message = str(e)
            messagebox.showerror("Ошибка", error_message,parent=self.master)