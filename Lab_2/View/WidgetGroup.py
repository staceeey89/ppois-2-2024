import tkinter as tk
from tkinter import messagebox
from typing import List

class WidgetSearchByGroup(tk.Frame):
    def __init__(self,controller,mode='search',tablewidget = None, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.master = master
        self.table = tablewidget
        self.controller = controller
        self.mode = mode
        self.subject_label = tk.Label(self, text="Группы:")
        self.subject_label.grid(row=2, column=0, sticky="w")

        self.groups_listbox = tk.Listbox(self)

        all_groups = self.controller.database.get_all_group_numbers()
        for subject in all_groups:
            self.groups_listbox.insert(tk.END, subject)
        self.groups_listbox.grid(row=3, column=0, columnspan=2, sticky="nsew")

        button_text = "Найти" if mode == 'search' else "Удалить"
        self.find_button = tk.Button(self, text=button_text, command=self.find)
        self.find_button.grid(row=4, column=0, columnspan=2, sticky="nsew")

    def find(self)->List[int]:
        try:
            selected_item = self.groups_listbox.curselection()
            if selected_item:
                selected_item = self.groups_listbox.get(selected_item[0])
                list_id= self.controller.database.get_students_in_group(selected_item)
                if len(list_id) == 0:
                    messagebox.showinfo("внимание", "записи по данному запросу не найдены", parent=self.master)
                else:
                    if self.mode == 'search' and not self.table is None:
                        self.table.set_data(list_id)
                    elif self.mode == 'delete':
                        self.controller.delete_student(list_id, self.master)
            else:
                messagebox.showerror("Ошибка", "Выберите группу.",parent=self.master)
        except ValueError as e:
            error_message = str(e)
            messagebox.showerror("Ошибка", error_message,parent=self.master)