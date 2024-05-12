from tkinter import *
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as mb
from datetime import datetime
from tkcalendar import *


class AddInterface:
    def __init__(self, model_base,parent):
        self.parent = parent
        self.window1 = tk.Toplevel()
        self.window1.title("Окно добавления")
        self.window1.geometry()
        self.frame = tk.Frame(self.window1)
        self.frame.grid()
        self.model_base = model_base

        new_entry_frame = ttk.Labelframe(self.frame, text="Добавить новую медицинскую карту", padding=[4, 8])

        tk.Label(new_entry_frame, text="Фамилия пациента").grid(row=2, column=0, pady=10)
        self.patient_surname = tk.Entry(new_entry_frame)
        self.patient_surname.grid(row=3, column=0, pady=10)
        tk.Label(new_entry_frame, text="Имя пациента").grid(row=2, column=1, pady=10)
        self.patient_name = tk.Entry(new_entry_frame)
        self.patient_name.grid(row=3, column=1, pady=10)
        tk.Label(new_entry_frame, text="Адрес прописки").grid(row=2, column=2, pady=10)
        self.registration_address = tk.Entry(new_entry_frame)
        self.registration_address.grid(row=3, column=2, pady=10)
        tk.Label(new_entry_frame, text="Дата рождения").grid(row=2, column=3, pady=10)
        self.birthday_date = DateEntry(new_entry_frame)
        self.birthday_date.grid(row=3, column=3, pady=10)
        tk.Label(new_entry_frame, text="Дата приема").grid(row=2, column=4, pady=10)
        self.appointment_date = DateEntry(new_entry_frame)
        self.appointment_date.grid(row=3, column=4, pady=10)
        tk.Label(new_entry_frame, text="Фамилия врача").grid(row=2, column=5, pady=10)
        self.doctor_surname = tk.Entry(new_entry_frame)
        self.doctor_surname.grid(row=3, column=5, pady=10)
        tk.Label(new_entry_frame, text="Имя врача").grid(row=2, column=6, pady=10)
        self.doctor_name = tk.Entry(new_entry_frame)
        self.doctor_name.grid(row=3, column=6, pady=10)
        tk.Label(new_entry_frame, text="Заключение").grid(row=2, column=7, pady=10)
        self.doctor_statement = tk.Entry(new_entry_frame)
        self.doctor_statement.grid(row=3, column=7, pady=10)

        tk.Button(new_entry_frame, text="Ввод", command=self._gui_new_entries).grid(row=4, column=3, pady=20)

        new_entry_frame.grid(row=4, column=2, columnspan=7)

        self.window1.mainloop()

    def _gui_new_entries(self):
        try:
            self.model_base.check_date(self.birthday_date.get())
            self.model_base.check_date(self.appointment_date.get())
            self.model_base.check_statement(self.doctor_statement.get())
            self.model_base.check_registration(self.registration_address.get())
            self.model_base.check_surname_name(self.patient_surname.get())
            self.model_base.check_surname_name(self.patient_name.get())
            self.model_base.check_surname_name(self.doctor_surname.get())
            self.model_base.check_surname_name(self.doctor_name.get())
        except Exception as e:
            msg = str(e)
            mb.showinfo("Информация", msg)
            print(e)
            return

        new_entry_data = (
            self.patient_surname.get(), self.patient_name.get(), self.registration_address.get(),
            self.birthday_date.get(),
            self.appointment_date.get(), self.doctor_surname.get(), self.doctor_name.get(), self.doctor_statement.get())

        self.model_base.new_entry(new_entry_data)
        self.parent.total_pages = self.parent.calculate_total_pages()
        self.parent.update_page_label()
        self.parent.load_page(self.parent.list_on_page)
