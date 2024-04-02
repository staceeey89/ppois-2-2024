import tkinter as tk
from tkinter import messagebox


class AddStudentDialog:
    def __init__(self, controller,callback):
        self.controller = controller
        self.callback = callback
        self.root = tk.Toplevel()
        self.root.title("Добавление студента")
        self.root.state('zoomed')
        self.root.minsize(800, 600)

        # Создаем Canvas и привязываем к нему Scrollbar
        self.canvas = tk.Canvas(self.root)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.v_scrollbar = tk.Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
        self.v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.configure(yscrollcommand=self.v_scrollbar.set)

        # Создаем внутренний фрейм на Canvas
        self.inner_frame = tk.Frame(self.canvas)
        self.inner_frame_id = self.canvas.create_window((0, 0), window=self.inner_frame, anchor=tk.NW)

        # Добавляем все элементы на внутренний фрейм
        self.add_elements()
        self.root.lift()
        # Обновляем прокрутку при изменении размеров
        self.inner_frame.bind("<Configure>", self.on_frame_configure)
        self.canvas.bind("<Configure>", self.on_canvas_configure)
        self.subject_entries = []
        self.root.protocol("WM_DELETE_WINDOW", self.__close)
        self.root.mainloop()

    def __close(self):
        self.callback()
        self.controller.close_page("AddStudentDialog")
        self.root.destroy()

    def on_canvas_configure(self, event):
        self.canvas.itemconfig(self.inner_frame_id, width=event.width)

    def add_elements(self):
        self.full_name_label = tk.Label(self.inner_frame, text="ФИО:")
        self.full_name_entry = tk.Entry(self.inner_frame)

        self.group_id_label = tk.Label(self.inner_frame, text="Номер группы:")
        self.groups_listbox = tk.Listbox(self.inner_frame, selectmode=tk.SINGLE)
        self.groups_listbox.bind("<<ListboxSelect>>", self.on_group_select)

        self.add_button = tk.Button(self.inner_frame, text="Добавить", command=self.validate_and_add_student)

        # Заполнение списка групп
        self.update_groups_listbox()

        # Размещение элементов с использованием grid()
        self.full_name_label.grid(row=0, column=0, sticky=tk.E)
        self.full_name_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
        self.group_id_label.grid(row=1, columnspan=2, pady=(10, 0))
        self.groups_listbox.grid(row=2, columnspan=2, padx=5, pady=5, sticky=tk.NSEW)
        self.add_button.grid(row=3, columnspan=2, pady=10)

    def update_groups_listbox(self):
        all_group_numbers = self.controller.database.get_all_group_numbers()
        for group_number in all_group_numbers:
            self.groups_listbox.insert(tk.END, group_number)
        self.groups_listbox["exportselection"] = False

    def on_group_select(self, event):
        selected_index = self.groups_listbox.curselection()
        if selected_index:
            selected_group = self.groups_listbox.get(selected_index)
            self.subjects = self.controller.database.get_subjects_by_group_number(int(selected_group))
            self.create_subject_entries()

    def create_subject_entries(self):
        # Создаем отдельный фрейм для меток и полей ввода
        if hasattr(self, 'subject_frame'):
            self.subject_frame.destroy()
        self.subject_frame = tk.Frame(self.inner_frame)
        self.subject_frame.grid(row=4, columnspan=2, padx=5, pady=5, sticky=tk.W)

        self.subject_entries = []
        for i, subject in enumerate(self.subjects):
            label = tk.Label(self.subject_frame, text=subject)
            label.grid(row=i, column=0, sticky=tk.E)
            entry = tk.Entry(self.subject_frame)
            entry.grid(row=i, column=1, padx=5, pady=5, sticky=tk.W)
            self.subject_entries.append((subject, entry))

    def validate_and_add_student(self):
        full_name = self.full_name_entry.get()
        try:
            self.controller.validate_student_data(full_name)

            if not self.subject_entries:
                messagebox.showerror("Ошибка", "Нет выбрана группа",parent=self.root)
                return

            grades = []
            for subject, entry in self.subject_entries:
                grade_str = entry.get()
                self.controller.validate_grade_input(subject, grade_str)
                grades.append((subject, int(grade_str)))

            group_number = self.groups_listbox.get(self.groups_listbox.curselection())
            self.controller.validate_group_number(group_number)

            self.controller.database.add_student(full_name, int(group_number), grades)
            messagebox.showinfo("Успех", "Студент успешно добавлен",parent=self.root)

        except ValueError as e:
            error_message = str(e)
            messagebox.showerror("Ошибка", error_message,parent=self.root)

    def on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
