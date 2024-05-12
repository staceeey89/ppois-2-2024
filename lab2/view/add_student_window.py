from __future__ import annotations

import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showerror, showwarning, showinfo

from view.center_window import center_window


class AddStudentWindow(tk.Toplevel):
    def __init__(self, master, application):
        super().__init__(master=master)
        self.title("Add student")
        self.application = application

        center_window(self, 250, 170)

        name_frame = ttk.LabelFrame(self, text="Student name")
        self.name_entry = ttk.Entry(name_frame)
        self.name_entry.pack()
        name_frame.pack(pady=10)

        all_groups = self.application.repo.get_groups()
        groups_numbers = [str(group.number) for group in all_groups]
        self.groups_dict = {key: value for key, value in zip(groups_numbers, all_groups)}

        group_frame = ttk.LabelFrame(self, text="Student group")
        self.group_combobox = ttk.Combobox(group_frame, values=groups_numbers)
        if len(groups_numbers) > 0:
            self.group_combobox.set(groups_numbers[0])
        self.group_combobox.pack()
        group_frame.pack(pady=10)

        add_button = ttk.Button(self, text="Add student", command=self.add_student)
        add_button.pack(pady=10)

        if len(groups_numbers) == 0:
            tk.messagebox.showinfo(title='Error', message='No groups found')
            self.destroy()

    def add_student(self):
        if len(self.name_entry.get()) == 0:
            return

        student_group = self.groups_dict[self.group_combobox.get()]
        self.application.repo.add_student(self.name_entry.get(), student_group.id)

        self.application.update_students_data()
        self.destroy()

