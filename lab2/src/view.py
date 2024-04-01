import tkinter as tk
from tkinter import *
from controller import Controller
import time


class View():
    def __init__(self):
        self.root = None
        self.widgets = []
        self.image_labels = []
        self.controller = Controller()
        self.entry6 = None

    def create_window(self):
        self.root = tk.Tk()
        self.root.title("Стартовое окно")
        self.root.geometry("960x720")
        self.root.resizable(width=False, height=False)

    def start_window(self):
        self.additional_window_open = False
        self.bg_image = tk.PhotoImage(file="../images/main_window.png")
        bg_label = tk.Label(self.root, image=self.bg_image)
        bg_label.image = self.bg_image
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        self.root.geometry("+{}+{}".format(420, 130))

        self.entry = tk.Entry(self.root, font=("Times New Roman", 16), background="#EAEAEA", foreground="black",
                              justify="left", borderwidth=1, relief="solid")
        self.entry.place(x=30, y=65, width=365, height=50)
        self.entry.insert(tk.END, "../database/")
        self.widgets.append(self.entry)

        label = tk.Label(self.root, text="Укажите путь для файла загрузки:", font=("Times New Roman", 12), bg="white",
                         fg="black",
                         highlightthickness=0, borderwidth=1, relief="solid")
        label.place(x=30, y=42)
        self.widgets.append(label)

        button_image = tk.PhotoImage(file="../images/button_send.png")
        send_button = tk.Button(self.root, image=button_image, borderwidth=0, command=self.send_link_to_file,
                                relief="solid")
        send_button.place(x=397, y=64)
        self.widgets.append(send_button)

        button_create_new = tk.Button(self.root, text="Создать новую информационную таблицу",
                                      font=("Times New Roman", 14), bg="white", fg="black",
                                      command=self.create_database_window)
        button_create_new.place(x=31, y=130)
        self.widgets.append(button_create_new)

        self.root.mainloop()

    def send_link_to_file(self):
        text = self.entry.get()
        if text:
            if self.controller.check_original_file(text):
                self.create_exeption_window()
                self.entry.insert(tk.END, "../database/")
            else:
                self.clear_window()
                self.correct_input_file_path()
                self.change_to_main_window()

    def correct_input_file_path(self):
        for i in range(1, 5):
            our_image = PhotoImage(file=f"../images/load_step{i}.png")
            our_label = tk.Label(self.root, image=our_image)
            our_label.place(x=0, y=0, relwidth=1, relheight=1)
            self.root.update()
            time.sleep(0.5)
            self.image_labels.append(our_label)
            if i == 4:
                our_image = PhotoImage(file="../images/file_founded.png")
                our_label = tk.Label(self.root, image=our_image)
                our_label.place(x=0, y=0, relwidth=1, relheight=1)
                self.root.update()
                time.sleep(1.3)
                self.image_labels.append(our_label)
        self.clear_images()

    def clear_images(self):
        for label in self.image_labels:
            label.destroy()
        self.image_labels = []

    def create_exeption_window(self):
        additional_window = tk.Toplevel(self.root)
        additional_window.geometry("450x200")
        additional_window.title("Исключение")
        additional_window.resizable(width=False, height=False)
        additional_window.geometry("+{}+{}".format(655, 400))
        bg_image = tk.PhotoImage(file="../images/exception_window.png")
        bg_label = tk.Label(additional_window, image=bg_image)
        bg_label.image = bg_image
        bg_label.place(relx=0, rely=0, relwidth=1, relheight=1)
        continue_button = tk.Button(additional_window, text="Продолжить", command=additional_window.destroy)
        continue_button.place(relx=0.5, rely=0.9, anchor="center")
        self.entry.delete(0, 'end')

    def clear_window(self):
        for widget in self.widgets:
            widget.destroy()
        self.widgets = []

    def create_database_window(self):
        self.clear_window()
        self.root.title("Создание базы данных")
        self.entry = tk.Entry(self.root, font=("Times New Roman", 16), background="#EAEAEA", foreground="black",
                              justify="left", borderwidth=1, relief="solid")
        self.entry.place(x=30, y=65, width=365, height=50)
        self.widgets.append(self.entry)
        label = tk.Label(self.root, text="Введите название файла:", font=("Times New Roman", 12), bg="white",
                         fg="black",
                         highlightthickness=0, borderwidth=1, relief="solid")
        label.place(x=30, y=42)
        self.widgets.append(label)
        button_db = tk.Button(self.root, borderwidth=1, text="Назад", command=self.go_to_start_window,
                              relief="solid", font=("Times New Roman", 12))
        button_db.place(x=900, y=680)
        self.widgets.append(button_db)
        button_db = tk.Button(self.root, borderwidth=1, text="Создать файл DB", command=self.get_file_name_for_db,
                              relief="solid", font=("Times New Roman", 12))
        button_db.place(x=31, y=134)
        self.widgets.append(button_db)
        button_xml = tk.Button(self.root, borderwidth=1, text="Создать файл XML", command=self.get_file_name_for_xml,
                               relief="solid", font=("Times New Roman", 12))
        button_xml.place(x=171, y=134)
        self.widgets.append(button_xml)

    def go_to_start_window(self):
        self.clear_window()
        self.start_window()

    def file_exist(self, file_name):
        self.entry.delete(0, tk.END)
        self.entry.insert(tk.END, "Файл с таким именем уже существует")
        self.root.update()
        time.sleep(1.3)
        self.entry.delete(0, tk.END)
        self.entry.insert(tk.END, file_name)

    def get_file_name_for_db(self):
        file_name = self.entry.get()
        result = self.controller.create_db_file(file_name)
        if result is not None:
            flag, self.file_path = result
        else:
            flag = False
            self.file_path = ""
            self.change_to_main_window()
        if flag:
            self.file_exist(file_name)
            self.add_delete_button()
            # file exist

    def get_file_name_for_xml(self):
        file_name = self.entry.get()
        result = self.controller.create_xml_file(file_name)
        if result is not None:
            flag, self.file_path = result
        else:
            flag = False
            self.file_path = ""
            self.change_to_main_window()
        if flag:
            self.file_exist(file_name)
            self.add_delete_button()
        # file exist

    def add_delete_button(self):
        button_delete = tk.Button(self.root, borderwidth=1, text="Удалить файл с таким именем",
                                  command=self.get_file_path_to_delete(),
                                  relief="solid", font=("Times New Roman", 12))
        button_delete.place(x=31, y=174)

    def get_file_path_to_delete(self):
        self.controller.delete_file(self.file_path)
        self.entry.delete(0, tk.END)

    def change_to_main_window(self):
        self.open = False
        self.additional_window_delete_open = False
        for widget in self.root.winfo_children():
            widget.destroy()
        self.root.title("Информационное табло")
        self.per_page = 10
        bg_label = tk.Label(self.root, image=self.bg_image)
        bg_label.image = self.bg_image
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        frame = tk.Frame(self.root)
        frame.pack(side=tk.TOP, fill=tk.X)
        button1 = tk.Button(frame, text="Дерево", command=self.window_for_tree)
        button1.pack(side=tk.LEFT)
        button2 = tk.Button(frame, text="Добавить", command=self.window_for_add_to_database)
        button2.pack(side=tk.LEFT)
        button3 = tk.Button(frame, text="Удалить", command=self.window_for_delete)
        button3.pack(side=tk.LEFT)
        button4 = tk.Button(frame, text="Поиск", command=self.window_for_search)
        button4.pack(side=tk.LEFT)
        button5 = tk.Button(frame, text="Выход", command=self.exit)
        button5.pack(side=tk.LEFT)
        button = tk.Button(self.root,text="->",command=self.set_per_page,borderwidth=1,relief="solid")
        button.place(x=767,y=372,width=20,height=24)
        self.entry_per_page = tk.Entry(self.root,borderwidth=1,relief="solid")
        self.entry_per_page.delete(0,tk.END)
        self.entry_per_page.insert(0,self.per_page)
        self.entry_per_page.place(x=640,y=372,height=24)
        self.info_train_board()

    def exit(self):
        self.controller.model.close_connect(self.controller.type)
        self.start_window()

    def window_for_tree(self):
        if not self.additional_window_open and not self.open:
            self.open = True
            self.additional_window_open = True
            self.additional_window = tk.Toplevel(self.root)
            self.additional_window.geometry("830x350")
            self.additional_window.title("Дерево")
            self.additional_window.resizable(width=False, height=False)
            tree_text = tk.Text(self.additional_window, wrap=tk.WORD)
            tree_text.pack(fill=tk.BOTH, expand=True)
            tree_text.insert(tk.END, self.controller.create_tree())
            scrollbar = tk.Scrollbar(self.additional_window, orient=tk.VERTICAL, command=tree_text.yview)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            tree_text.config(yscrollcommand=scrollbar.set)
            self.additional_window.protocol("WM_DELETE_WINDOW", self.close_tree)

    def close_tree(self):
        self.open = False
        self.additional_window_open = False
        self.additional_window.destroy()
    def window_for_delete(self):
        if not self.additional_window_open and not self.open:
            self.open = True
            self.additional_window_delete_open = True
            self.additional2_window = tk.Toplevel(self.root)
            self.additional2_window.geometry("830x400")
            self.additional2_window.title("Окно удаления")
            self.additional2_window.resizable(width=False, height=False)
            bg_image = tk.PhotoImage(file="../images/window_data2.png")
            bg_label = tk.Label(self.additional2_window, image=bg_image)
            bg_label.image = bg_image
            bg_label.place(relx=0, rely=0, relwidth=1, relheight=1)
            self.text_added = None
            self.add_entry_fileds(self.additional2_window)
            label6 = tk.Label(self.additional2_window, text="Время в пути",
                              font=("Times New Roman", 12),
                              fg="black", bg="#EAEAEA")
            label6.place(x=15, y=311)
            self.set_entry_num_2(self.additional2_window)
            self.additional2_window.protocol("WM_DELETE_WINDOW", self.clear_entries2)
            button_find = tk.Button(self.additional2_window, text="Удалить",
                                    command=self.find_info_to_delete,
                                    borderwidth=1, relief="solid",
                                    background="#EAEAEA")
            button_find.place(x=156, y=368)
            self.label_delete = tk.Label()

    def find_info_to_delete(self):
        if self.label_delete:
            self.label_delete.destroy()
        columns = []
        columns.append(self.entry6.get())
        columns.append(self.entry7.get())
        columns.append(self.entry8.get())
        columns.append(self.entry9.get())
        columns.append(self.entry10.get())
        columns.append(self.entry11.get())
        text = self.controller.check_delete_info(columns)
        self.label_delete = tk.Label(self.additional2_window, text=text,
                              font=("Times New Roman", 20),borderwidth=1,relief="solid",
                              fg="black", bg="#EAEAEA")
        self.label_delete.place(x=240,y=120)
        self.controller.create_info_board(self.root, self.per_page)
    def set_per_page(self):
        if self.entry_per_page.get().isdigit():
            # self.controller.destroy_table()
            per_page = int(self.entry_per_page.get())
            self.controller.table.label_table.destroy()
            self.controller.create_info_board(self.root,per_page)
            self.per_page = per_page
        else:
            self.entry_per_page.delete(0,tk.END)
            self.entry_per_page.insert(0,self.per_page)


    def info_train_board(self):
        self.controller.create_info_board(self.root,self.per_page)

    def window_for_search(self):
        if not self.additional_window_delete_open and not self.open:
            self.open = True
            self.additional_window_open = True
            self.additional2_window = tk.Toplevel(self.root)
            self.additional2_window.geometry("830x400")
            self.additional2_window.title("Окно поиска")
            self.additional2_window.resizable(width=False, height=False)
            bg_image = tk.PhotoImage(file="../images/window_data2.png")
            bg_label = tk.Label(self.additional2_window, image=bg_image)
            bg_label.image = bg_image
            bg_label.place(relx=0, rely=0, relwidth=1, relheight=1)
            self.text_added = None
            self.add_entry_fileds(self.additional2_window)
            label6 = tk.Label(self.additional2_window, text="Время в пути",
                              font=("Times New Roman", 12),
                              fg="black", bg="#EAEAEA")
            label6.place(x=15, y=311)
            self.set_entry_num_2(self.additional2_window)
            self.additional2_window.protocol("WM_DELETE_WINDOW", self.clear_entries2)
            button_find = tk.Button(self.additional2_window, text="Поиск",
                                    command=self.get_search_parametrs,
                                    borderwidth=1, relief="solid",
                                    background="#EAEAEA")
            button_find.place(x=156, y=368)
            self.controller.window_add_into_database(self.additional2_window, 220, 90)

    def clear_entries2(self):
        self.open = False
        self.entry6.destroy()
        self.entry7.destroy()
        self.entry8.destroy()
        self.entry9.destroy()
        self.entry10.destroy()
        self.entry11.destroy()
        self.additional2_window.destroy()
        self.additional_window_open = False
        self.additional_window_delete_open = False
    def get_search_parametrs(self):
        data = []
        data.append(self.entry6)
        data.append(self.entry7)
        data.append(self.entry8)
        data.append(self.entry9)
        data.append(self.entry10)
        data.append(self.entry11)
        if self.controller.check_correct_input_data(data):
            return
        data = self.controller.get_data(data)
        self.controller.get_result_of_search(data,self.additional2_window,220,90)

    def window_for_add_to_database(self):
        if not self.additional_window_delete_open and not self.open:
            self.open = True
            self.additional_window_open = True
            self.additional_window = tk.Toplevel(self.root)
            self.additional_window.geometry("830x350")
            self.additional_window.title("Добавить запись")
            self.additional_window.resizable(width=False, height=False)
            self.set_data_window(self.additional_window)
            self.text_added = None
            self.add_entry_fileds(self.additional_window)
            self.set_entry_num_1(self.additional_window)
            continue_button = tk.Button(self.additional_window, text="Добавить",
                                        command=self.send_info_to_database,
                                        borderwidth=1, relief="solid",
                                        background="#EAEAEA")
            continue_button.place(x=139, y=308)
            label_data_info = tk.Label(self.additional_window, text="Формат ввода даты и времени\nYYYY-MM-DD HH:MM",
                                       font=("Times New Roman", 12),
                                       fg="black", borderwidth=1, relief="solid",
                                       highlightthickness=0)
            label_data_info.place(x=220, y=290)
            self.controller.window_add_into_database(self.additional_window, 220, 75)
            self.additional_window.protocol("WM_DELETE_WINDOW", self.clear_entries)

    def clear_entries(self):
        self.open = False
        self.entry1.destroy()
        self.entry2.destroy()
        self.entry3.destroy()
        self.entry4.destroy()
        self.entry5.destroy()
        self.additional_window.destroy()
        self.additional_window_open = False

    def send_info_to_database(self):
        data = [self.entry1, self.entry2, self.entry3, self.entry4, self.entry5]
        self.text_added = self.controller.add_to_database(data, self.additional_window, self.text_added)
        self.controller.window_add_into_database(self.additional_window, 220, 75)
        self.info_train_board()

    def add_entry_fileds(self, root):
        start_pos_x = 15
        entry_width = 185
        entry_height = 20
        label1 = tk.Label(root, text="Номер поезда", font=("Times New Roman", 12), bg="#EAEAEA",
                          fg="black",
                          highlightthickness=0)
        label1.place(x=start_pos_x, y=11)
        label2 = tk.Label(root, text="Станция отправления", font=("Times New Roman", 12),
                          bg="#EAEAEA",
                          fg="black",
                          highlightthickness=0)
        label2.place(x=start_pos_x, y=71)
        label3 = tk.Label(root, text="Дата и время отправления", font=("Times New Roman", 12),
                          bg="#EAEAEA",
                          fg="black",
                          highlightthickness=0)
        label3.place(x=start_pos_x, y=131)
        label4 = tk.Label(root, text="Станция прибытия", font=("Times New Roman", 12), bg="#EAEAEA",
                          fg="black",
                          highlightthickness=0)
        label4.place(x=start_pos_x, y=191)
        label5 = tk.Label(root, text="Дата и время прибытия", font=("Times New Roman", 12),
                          bg="#EAEAEA",
                          fg="black",
                          highlightthickness=0)
        label5.place(x=start_pos_x, y=251)

    def set_entry_num_1(self,root):
        start_pos_x = 15
        entry_width = 185
        entry_height = 20
        self.entry1 = tk.Entry(root, font=("Times New Roman", 12), background="#EAEAEA",
                               foreground="black",
                               justify="left", borderwidth=1, relief="solid")
        self.entry1.place(x=start_pos_x, y=35, width=entry_width, height=entry_height)
        self.entry2 = tk.Entry(root, font=("Times New Roman", 12), background="#EAEAEA",
                               foreground="black",
                               justify="left", borderwidth=1, relief="solid")
        self.entry2.place(x=start_pos_x, y=95, width=entry_width, height=entry_height)
        self.entry3 = tk.Entry(root, font=("Times New Roman", 12), background="#EAEAEA",
                               foreground="black",
                               justify="left", borderwidth=1, relief="solid")
        self.entry3.place(x=start_pos_x, y=155, width=entry_width, height=entry_height)
        self.entry4 = tk.Entry(root, font=("Times New Roman", 12), background="#EAEAEA",
                               foreground="black",
                               justify="left", borderwidth=1, relief="solid")
        self.entry4.place(x=start_pos_x, y=215, width=entry_width, height=entry_height)
        self.entry5 = tk.Entry(root, font=("Times New Roman", 12), background="#EAEAEA",
                               foreground="black",
                               justify="left", borderwidth=1, relief="solid")
        self.entry5.place(x=start_pos_x, y=275, width=entry_width, height=entry_height)

    def set_entry_num_2(self,root):
        start_pos_x = 15
        entry_width = 185
        entry_height = 20
        self.entry6 = tk.Entry(root, font=("Times New Roman", 12), background="#EAEAEA",
                               foreground="black",
                               justify="left", borderwidth=1, relief="solid")
        self.entry6.place(x=start_pos_x, y=35, width=entry_width, height=entry_height)
        self.entry7 = tk.Entry(root, font=("Times New Roman", 12), background="#EAEAEA",
                               foreground="black",
                               justify="left", borderwidth=1, relief="solid")
        self.entry7.place(x=start_pos_x, y=95, width=entry_width, height=entry_height)
        self.entry8 = tk.Entry(root, font=("Times New Roman", 12), background="#EAEAEA",
                               foreground="black",
                               justify="left", borderwidth=1, relief="solid")
        self.entry8.place(x=start_pos_x, y=155, width=entry_width, height=entry_height)
        self.entry9 = tk.Entry(root, font=("Times New Roman", 12), background="#EAEAEA",
                               foreground="black",
                               justify="left", borderwidth=1, relief="solid")
        self.entry9.place(x=start_pos_x, y=215, width=entry_width, height=entry_height)
        self.entry10 = tk.Entry(root, font=("Times New Roman", 12), background="#EAEAEA",
                               foreground="black",
                               justify="left", borderwidth=1, relief="solid")
        self.entry10.place(x=start_pos_x, y=275, width=entry_width, height=entry_height)
        self.entry11 = tk.Entry(self.additional2_window, font=("Times New Roman", 12), background="#EAEAEA",
                               foreground="black",
                               justify="left", borderwidth=1, relief="solid")
        self.entry11.place(x=15, y=335, width=185, height=20)

    def set_data_window(self, root):
        bg_image = tk.PhotoImage(file="../images/window_data.png")
        bg_label = tk.Label(root, image=bg_image)
        bg_label.image = bg_image
        bg_label.place(relx=0, rely=0, relwidth=1, relheight=1)
