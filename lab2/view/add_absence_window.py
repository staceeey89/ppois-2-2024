from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from controller.db_repository import DbRepository
from model.absence import Absence
from view.center_window import center_window


class AddAbsenceWindow(tk.Toplevel):
    def __init__(self, master, application):
        super().__init__(master=master)
        self.title("Add absence")
        self.application = application

        center_window(self, 200, 150)

        all_reasons = self.application.repo.get_absence_reasons()
        reasons_numbers = [str(reason.name) for reason in all_reasons]
        self.reasons_dict = {key: value for key, value in zip(reasons_numbers, all_reasons)}

        group_frame = ttk.LabelFrame(self, text="Absence reason")
        self.group_combobox = ttk.Combobox(group_frame, values=reasons_numbers)
        self.group_combobox.set(reasons_numbers[0])
        self.group_combobox.pack()
        group_frame.pack(pady=10)

        add_button = ttk.Button(self, text="Add absence", command=self.add_absence)
        add_button.pack(pady=10)

    def add_absence(self):
        self.application.repo.add_absence(self.application.selected_student_id,
                                          self.reasons_dict[self.group_combobox.get()].id)

        self.application.update_absences_data()
        self.application.update_students_data()

