from tkinter import *
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as mb


class SearchInterface:
    def __init__(self, model_base):
        self.window1 = tk.Toplevel()
        self.window1.title("Окно поиска")
        self.window1.geometry()
        self.frame = tk.Frame(self.window1)
        self.frame.grid()
        self.model_base = model_base

        main_frame = ttk.Labelframe(self.frame, text="Медицинские карты", padding=[5, 5]) # первый фрейм
        columns = ("patient_surname", "patient_name", "registration_address", "birthday_date", "appointment_date",
                   "doctor_surname", "doctor_name", "doctor_statement")
        self.search_table = ttk.Treeview(main_frame, columns=columns, show="headings")
        self.search_table.heading(0, text="Фамилия пациента", anchor=W)
        self.search_table.heading(1, text="Имя пациента", anchor=W)
        self.search_table.heading(2, text="Адрес прописки", anchor=W)
        self.search_table.heading(3, text="Дата рождения", anchor=W)
        self.search_table.heading(4, text="Дата приема", anchor=W)
        self.search_table.heading(5, text="Фамилия врача", anchor=W)
        self.search_table.heading(6, text="Имя врача", anchor=W)
        self.search_table.heading(7, text="Заключение", anchor=W)
        self.search_table.grid(row=0, column=0, columnspan=6, pady=20)
        main_frame.grid(row=0, column=0, columnspan=60) # использование первого фрейма

        self.frame_for_radiobuttons = tk.Frame(self.frame) # второй фрейм

        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=self.search_table.yview)
        scrollbar.grid(row=0, column=6, sticky="ns")

        self.search_table.configure(yscrollcommand=scrollbar.set)

        self.frame_for_combo1 = ttk.Frame(self.frame, relief=SOLID, padding=[5, 5]) # третий фрейм
        self.frame_for_combo2 = ttk.Frame(self.frame, relief=SOLID, padding=[5, 5]) # четвертый фрейм
        self.frame_for_combo3 = ttk.Frame(self.frame, relief=SOLID, padding=[5, 5])  # пятый фрейм

        self.check = IntVar(value=0)
        ttk.Radiobutton(self.frame_for_radiobuttons, text="По фамилии пациента или адресу прописки", value=1, variable=self.check, command=self.__create_combo1).grid(row=1, column=0, padx=100)
        ttk.Radiobutton(self.frame_for_radiobuttons, text="По дате рождения", value=2, variable=self.check, command=self.__create_combo2).grid(row=1, column=50, padx=150)
        ttk.Radiobutton(self.frame_for_radiobuttons, text="По имени врача или дате последнего приёма", value=3, variable=self.check, command=self.__create_combo3).grid(row=1, column=60, padx=150)
        self.frame_for_radiobuttons.grid(row=1, column=0, columnspan=70)  # использование второго фрейма

        self.combobox1 = None
        self.combobox2 = None
        self.min_money = IntVar(value=100)
        self.max_money = IntVar(value=100)
        tk.Button(self.frame, text="Искать", command=self.search_command).grid(row=4, column=2, pady=5)

        self._view_loading()

        self.window1.mainloop()

    def _view_loading(self, new_model=None):
        for item in self.search_table.get_children():
            self.search_table.delete(item)

        if new_model is not None:
            lis_base = new_model
        else:
            lis_base = self.model_base.loading()

        for i in lis_base:
            self.search_table.insert("", tk.END, values=i)

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

    def __combo_func(self, param: str):
        val = []
        for i in self.model_base.help_search(param):
            val.append(*i)
        return val

    def __create_combo2(self):
        page_val = self.__combo_func("birthday_date")
        self.first_element3 = StringVar(value=page_val[0])
        self.combobox1 = ttk.Combobox(self.frame_for_combo2, textvariable=self.first_element3, values=self.__combo_func("birthday_date"))
        self.combobox1.grid(row=2, column=2)

        self.frame_for_combo2.grid(row=2, column=18, columnspan=20) # использование четвертого фрейма

    def __create_combo3(self):
        page_val = self.__combo_func("doctor_name")
        self.first_element4 = StringVar(value=page_val[0])
        self.combobox1 = ttk.Combobox(self.frame_for_combo3, textvariable=self.first_element4, values=self.__combo_func("doctor_name"))
        self.combobox1.grid(row=2, column=3)

        page_val = self.__combo_func("appointment_date")
        self.first_element5 = StringVar(value=page_val[0])
        self.combobox2 = ttk.Combobox(self.frame_for_combo3, textvariable=self.first_element5, values=self.__combo_func("appointment_date"))
        self.combobox2.grid(row=2, column=4)

        self.frame_for_combo3.grid(row=2, column=37, columnspan=20) # использование третьего фрейма

    def search_command(self):
        if self.combobox2 is None:
            new_model = self.model_base.search(self.check.get(), self.combobox1.get())
        else:
            new_model = self.model_base.search(self.check.get(), self.combobox1.get(), self.combobox2.get())
        self._view_loading(new_model)
