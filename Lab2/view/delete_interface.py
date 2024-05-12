from tkinter import *
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as mb

class DeleteInterface:
    def __init__(self, model_base, parent):
        self.parent = parent
        self.window1 = tk.Toplevel()
        self.window1.title("Окно удаления")
        self.window1.geometry()
        self.frame = tk.Frame(self.window1)
        self.frame.grid()
        self.model_base = model_base

        self.frame_for_radiobuttons = tk.Frame(self.frame)  # второй фрейм

        self.frame_for_combo1 = ttk.Frame(self.frame, relief=SOLID, padding=[5, 5])  # третий фрейм
        self.frame_for_combo2 = ttk.Frame(self.frame, relief=SOLID, padding=[5, 5])  # четвертый фрейм
        self.frame_for_combo3 = ttk.Frame(self.frame, relief=SOLID, padding=[5, 5])  # пятый фрейм

        self.check = IntVar(value=0)
        ttk.Radiobutton(self.frame_for_radiobuttons, text="По фамилии пациента или адресу прописки", value=1, variable=self.check, command=self.__create_combo1).grid(row=1, column=0, padx=100)
        ttk.Radiobutton(self.frame_for_radiobuttons, text="По дате рождения", value=2, variable=self.check, command=self.__create_combo2).grid(row=1, column=50, padx=150)
        ttk.Radiobutton(self.frame_for_radiobuttons, text="По имени врача или дате последнего приёма", value=3, variable=self.check, command=self.__create_combo3).grid(row=1, column=60, padx=150)
        self.frame_for_radiobuttons.grid(row=1, column=0, columnspan=70)  # использование второго фрейма

        self.combobox1 = None
        self.combobox2 = None
        tk.Button(self.frame, text="Удалить", command=self.delete_command).grid(row=4, column=2, pady=5)

        self.window1.mainloop()

    def __create_combo1(self):
        page_val = self.__combo_func("patient_surname")
        self.first_element1 = StringVar(value=page_val[0])
        self.combobox1 = ttk.Combobox(self.frame_for_combo1, textvariable=self.first_element1, values=self.__combo_func("patient_surname"))
        self.combobox1.grid(row=2, column=0)

        page_val = self.__combo_func("registration_address")
        self.first_element2 = StringVar(value=page_val[0])
        self.combobox2 = ttk.Combobox(self.frame_for_combo1, textvariable=self.first_element2, values=self.__combo_func("registration_address"))
        self.combobox2.grid(row=2, column=1)

        self.frame_for_combo1.grid(row=2, column=2, columnspan=20) # использование третьего фрейма

    def __create_combo2(self):
        page_val = self.__combo_func("birthday_date")
        self.first_element3 = StringVar(value=page_val[0])
        self.combobox1 = ttk.Combobox(self.frame_for_combo2, textvariable=self.first_element3, values=self.__combo_func("birthday_date"))
        self.combobox1.grid(row=2, column=2)

        self.frame_for_combo2.grid(row=2, column=22, columnspan=20) # использование четвертого фрейма

    def __create_combo3(self):
        page_val = self.__combo_func("doctor_name")
        self.first_element4 = StringVar(value=page_val[0])
        self.combobox1 = ttk.Combobox(self.frame_for_combo3, textvariable=self.first_element4, values=self.__combo_func("doctor_name"))
        self.combobox1.grid(row=2, column=3)

        page_val = self.__combo_func("appointment_date")
        self.first_element5 = StringVar(value=page_val[0])
        self.combobox2 = ttk.Combobox(self.frame_for_combo3, textvariable=self.first_element5, values=self.__combo_func("appointment_date"))
        self.combobox2.grid(row=2, column=4)

        self.frame_for_combo3.grid(row=2, column=47, columnspan=20) # использование третьего фрейма

    def __combo_func(self, param: str):
        val = []
        for i in self.model_base.help_search(param):
            val.append(*i)
        return val

    def delete_command(self):
        if self.combobox2 is None:
            num_deleted = self.model_base.delete(self.check.get(), self.combobox1.get())
        else:
            num_deleted = self.model_base.delete(self.check.get(), self.combobox1.get(), self.combobox2.get())

        if num_deleted > 0:
            msg = f"{num_deleted} records deleted."
        else:
            msg = "Не найдено записей, соответствующих указанным критериям."
        mb.showinfo("Информация", msg)
        self.parent.total_pages = self.parent.calculate_total_pages()
        self.parent.update_page_label()
        self.parent.load_page(self.parent.list_on_page)
