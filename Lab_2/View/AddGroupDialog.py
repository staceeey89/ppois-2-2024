import tkinter as tk
from tkinter import messagebox


class AddGroupDialog():
    def __init__(self, controller):
        self.controller = controller
        self.root = tk.Toplevel()
        self.root.title("Добавления новой группы")
        self.root.state('zoomed')
        self.root.minsize(800, 600)

        # Номер группы и название предмета
        self.group_label = tk.Label(self.root, text="Номер групп\n(6-значное число):")
        self.group_label.grid(row=0, column=0, padx=5, pady=5)
        self.group_number_entry = tk.Entry(self.root)
        self.group_number_entry.grid(row=0, column=1, padx=5, pady=5)

        self.subject_label = tk.Label(self.root, text="Название предмета:")
        self.subject_label.grid(row=1, column=0, padx=5, pady=5)
        self.subject_entry = tk.Entry(self.root)
        self.subject_entry.grid(row=1, column=1, padx=5, pady=5)
        self.add_subject_button = tk.Button(self.root, text="Добавить предмет", command=self.add_subject)
        self.add_subject_button.grid(row=1, column=2, padx=5, pady=5)

        self.subject_list_label = tk.Label(self.root, text="Добавленные предметы:")
        self.subject_list_label.grid(row=2, column=0, padx=5, pady=5)
        self.subject_listbox = tk.Listbox(self.root)
        self.subject_listbox.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

        # Listbox и подпись для экзаменов
        self.exam_label = tk.Label(self.root, text="Существующие предметы:")
        self.exam_label.grid(row=2, column=2, padx=5, pady=5)
        self.exam_listbox = tk.Listbox(self.root)
        self.exam_listbox.grid(row=3, column=2, padx=5, pady=5)

        self.populate_exam_listbox()
        self.exam_listbox.bind("<Double-Button-1>", self.move_exam_to_subject_listbox)

        # Кнопка добавления группы
        self.add_group_button = tk.Button(self.root, text="Добавить группу", command=self.add_group)
        self.add_group_button.grid(row=4, column=0, columnspan=3, padx=5, pady=5)

        self.root.protocol("WM_DELETE_WINDOW", self.__close)
        self.root.mainloop()

    def create_context_menu(self):
        self.context_menu = tk.Menu(self.root, tearoff=0)
        self.context_menu.add_command(label="Удалить", command=self.delete_subject)

        self.subject_listbox.bind("<Button-3>", self.show_context_menu)

    def show_context_menu(self, event):
        selected_index = self.subject_listbox.curselection()
        if selected_index:
            self.context_menu.post(event.x_root, event.y_root)

    def delete_subject(self):
        selected_index = self.subject_listbox.curselection()
        if selected_index:
            selected_exam = self.subject_listbox.get(selected_index)
            if self.controller.database.check_exam_exist(selected_exam):
                self.exam_listbox.insert(tk.END,
                                         selected_exam)
            self.subject_listbox.delete(selected_index)

    def populate_exam_listbox(self):
        unique_exam_names = self.controller.database.get_unique_exam_names()
        for exam_name in unique_exam_names:
            self.exam_listbox.insert(tk.END, exam_name)

    def move_exam_to_subject_listbox(self, event):
        selected_index = self.exam_listbox.curselection()
        if selected_index:
            selected_exam = self.exam_listbox.get(selected_index)
            self.subject_listbox.insert(tk.END, selected_exam)
            self.exam_listbox.delete(selected_index)

    def __close(self):
        self.controller.close_page("AddGroupDialog")
        self.root.destroy()

    def add_subject(self):
        subject = self.subject_entry.get()
        try:
            self.controller.validate_exam_name(subject)
        except ValueError as error:
            self.root.grab_set()
            messagebox.showerror("Error", str(error), parent=self.root)
        else:
            self.subject_listbox.insert(tk.END, subject)
            self.subject_entry.delete(0, tk.END)

    def add_group(self):
        subjects = self.subject_listbox.get(0, tk.END)
        try:
            if subjects:
                group_number = self.group_number_entry.get()
                self.controller.validate_group_number(group_number)
                if self.controller.database.check_group_exists(group_number):
                    messagebox.showwarning("Ошибка", "Группа с таким номером уже существует", parent=self.root)
                else:
                    messagebox.showinfo("Success", "Группа добавлена", parent=self.root)
                    self.controller.add_group(group_number, subjects)
                    self.root.grab_release()
                    self.root.destroy()
            else:
                raise ValueError("Добавьте хотя бы один предмет в группу.")
        except ValueError as e:
            error_message = str(e)
            messagebox.showwarning("Ошибка", error_message, parent=self.root)
