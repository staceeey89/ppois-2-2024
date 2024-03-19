from __future__ import annotations

import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showerror, showwarning, showinfo

from view.center_window import center_window


class SearchStudentsWindow(tk.Toplevel):
    def __init__(self, master, application):
        super().__init__(master=master)
        self.title("Search students")
        self.application = application

        self.search_by_group = tk.BooleanVar()
        self.search_by_name = tk.BooleanVar()
        self.search_by_limits = tk.BooleanVar()

        self.abs_other_min = tk.StringVar()
        self.abs_other_max = tk.StringVar()
        self.abs_sick_min = tk.StringVar()
        self.abs_sick_max = tk.StringVar()
        self.abs_unjust_min = tk.StringVar()
        self.abs_unjust_max = tk.StringVar()

        self.search_name = tk.StringVar()

        center_window(self, 230, 380)

        # search by name
        name_frame = ttk.LabelFrame(self, text="Student name")
        tk.Checkbutton(name_frame, variable=self.search_by_name).pack(side=tk.LEFT)

        ttk.Entry(name_frame, textvariable=self.search_name).pack(side=tk.LEFT)
        name_frame.pack(pady=10)

        # search by group
        all_groups = self.application.repo.get_groups()
        groups_numbers = [str(group.number) for group in all_groups]
        self.groups_dict = {key: value for key, value in zip(groups_numbers, all_groups)}

        group_frame = ttk.LabelFrame(self, text="Student group")
        group_checkbox = tk.Checkbutton(group_frame, variable=self.search_by_group)
        group_checkbox.pack(side=tk.LEFT)

        self.group_combobox = ttk.Combobox(group_frame, values=groups_numbers)
        if len(groups_numbers) > 0:
            self.group_combobox.set(groups_numbers[0])
        self.group_combobox.pack(side=tk.RIGHT)
        group_frame.pack(pady=10)

        # search by ranges
        absences_frame = ttk.LabelFrame(self, text="Absences")
        absences_checkbox = tk.Checkbutton(absences_frame, variable=self.search_by_limits)
        absences_checkbox.pack(side=tk.TOP)

        sick_frame = ttk.LabelFrame(absences_frame, text="Sick")
        self.absences_sick_min_entry = ttk.Entry(sick_frame, width=6, textvariable=self.abs_sick_min)
        self.absences_sick_min_entry.pack(side=tk.LEFT, padx=3)
        self.absences_sick_max_entry = ttk.Entry(sick_frame, width=6, textvariable=self.abs_sick_max)
        self.absences_sick_max_entry.pack(side=tk.LEFT, padx=3)
        sick_frame.pack(pady=3)

        other_frame = ttk.LabelFrame(absences_frame, text="Other")
        self.absences_other_min_entry = ttk.Entry(other_frame, width=6, textvariable=self.abs_other_min)
        self.absences_other_min_entry.pack(side=tk.LEFT, padx=3)
        self.absences_other_max_entry = ttk.Entry(other_frame, width=6, textvariable=self.abs_other_max)
        self.absences_other_max_entry.pack(side=tk.LEFT, padx=3)
        other_frame.pack(pady=3)

        unjust_frame = ttk.LabelFrame(absences_frame, text="Unjust")
        self.absences_unjust_min_entry = ttk.Entry(unjust_frame, width=6, textvariable=self.abs_unjust_min)
        self.absences_unjust_min_entry.pack(side=tk.LEFT, padx=3)
        self.absences_unjust_max_entry = ttk.Entry(unjust_frame, width=6, textvariable=self.abs_unjust_max)
        self.absences_unjust_max_entry.pack(side=tk.LEFT, padx=3)
        unjust_frame.pack(pady=3)

        absences_frame.pack(pady=10)

        search_button = ttk.Button(self, text="Search students", command=self.search_students)
        search_button.pack(pady=10)

        self.search_by_name.set(False)
        self.search_by_group.set(True)
        self.search_by_limits.set(False)

        self.abs_other_min.set('0')
        self.abs_other_max.set('10')
        self.abs_sick_min.set('0')
        self.abs_sick_max.set('10')
        self.abs_unjust_min.set('0')
        self.abs_unjust_max.set('10')

        if len(groups_numbers) == 0:
            tk.messagebox.showinfo(title='Error', message='No groups found')
            self.destroy()

    def search_students(self):
        limits = {
            'sick': [int(self.abs_sick_min.get()), int(self.abs_sick_max.get())],
            'other': [int(self.abs_other_min.get()), int(self.abs_other_max.get())],
            'unjust': [int(self.abs_unjust_min.get()), int(self.abs_unjust_max.get())]
        }

        self.application.search_criteria.group = self.groups_dict[self.group_combobox.get()]\
            if self.search_by_group.get() else None
        self.application.search_criteria.name = self.search_name.get() if self.search_by_name.get() else None
        self.application.search_criteria.page_number = 1
        self.application.search_criteria.criteria = limits if self.search_by_limits.get() else None

        self.application.update_students_data()

