import tkinter as tk
from tkinter import ttk
from View.PaginationControl import PaginationControl

class ShowTable(tk.Frame):
    def __init__(self, parent, controller, list_id):
        super().__init__(parent)
        self.controller = controller
        self.pack(expand=True, fill='both')
        self.table_frame = tk.Frame(self)
        self.pagination_frame = tk.Frame(self)
        self.table_frame.pack(expand=True, fill='both')
        self.pagination_frame.pack()
        self.v_scrollbar = ttk.Scrollbar(self.table_frame, orient="vertical")
        self.v_scrollbar.pack(side="right", fill="y")
        self.h_scrollbar = ttk.Scrollbar(self.table_frame, orient="horizontal")
        self.h_scrollbar.pack(side="bottom", fill="x")
        if not list_id is None:
            self.set_data(list_id)
        #self.load_data()
    def get_length(self,input_list):
        total = 0
        for item in input_list:
            if isinstance(item, list):
                total += len(item)
            else:
                total += 1
        return total

    def get_list(self,input_list):
        flattened_list = []
        for item in input_list:
            if isinstance(item, list):
                flattened_list.extend(self.get_list(item))
            else:
                flattened_list.append(item)
        return flattened_list

    def set_data(self, list_id: list[int]):
        self.items_count = self.get_length(list_id)
        self.students_info = []
        for student_id in self.get_list(list_id):
            student_info = self.controller.database.get_student_info(student_id)
            self.students_info.append(student_info)

        self.load_data()
        if hasattr(self, 'pagination_control') and self.pagination_control.winfo_exists():
            self.pagination_control.destroy()
        self.pagination_control = PaginationControl(self.pagination_frame, self, 10)
        self.pagination_control.pack()


    def add_scrollbar(self):
        self.v_scrollbar.configure(command=self.table.yview)
        self.table.configure(yscrollcommand=self.v_scrollbar.set)
        self.h_scrollbar.configure(command=self.table.xview)
        self.table.configure(xscrollcommand=self.h_scrollbar.set)

    def load_data(self,start_index=None, end_index=None, tree=False):
        if self.students_info is None or len(self.students_info)==0:
            if hasattr(self, 'table') and self.table.winfo_exists():
                self.table.destroy()
            self.table = ttk.Treeview(self.table_frame, columns=('Group Number', 'Average'), show='tree',
                                      selectmode='none')
            self.add_scrollbar()
            return
        if hasattr(self, 'table') and self.table.winfo_exists():
            self.table.destroy()
        if start_index is None:
            start_index = 0
        if end_index is None:
            end_index = self.items_count
        if tree:
            self.__load_data_in_tree(self.students_info[start_index:end_index])
        else:
            self.__load_data_table(self.students_info[start_index:end_index])
        self.table.pack(expand=True, fill='both')
        self.add_scrollbar()



    def __load_data_table(self, students_info):
        self.table = ttk.Treeview(self.table_frame, show='headings', selectmode='none')
        max_grades_count = max(len(student[3]) for student in students_info)
        self.table['columns'] = ('Name', 'Group Number', 'Average')
        for i in range(max_grades_count):
            name_column = f'Name_{i + 1}'
            grade_column = f'Grade_{i + 1}'
            self.table['columns'] += (name_column, grade_column)
        for i in range(max_grades_count):
            name_column = f'Name_{i + 1}'
            grade_column = f'Grade_{i + 1}'
            self.table.heading(name_column, text=f'Наименование')
            self.table.heading(grade_column, text=f'Балл')
            self.table.column(name_column, width=100)
            self.table.column(grade_column, width=40)
        # Set column widths
        self.table.heading('Name', text='ФИО')
        self.table.heading('Group Number', text='группа')
        self.table.heading('Average', text='ср.бал')
        self.table.column('Average', width=45)
        self.table.column('Name', width=150)
        self.table.column('Group Number', width=60)

        for student_info in students_info:
            student_data = [student_info[0], student_info[1], round(student_info[2],2)]
            for grade_info in student_info[3]:
                student_data.extend(grade_info)
            self.table.insert('', 'end', values=student_data)


    def __load_data_in_tree(self, students_info):
        self.table = ttk.Treeview(self.table_frame, columns=('Group Number', 'Average'), show='tree', selectmode='none')
        self.table.heading('#0', text='Name')
        for student_info in students_info:
            student_data_level_1 = [student_info[0]]
            student_node = self.table.insert('', 'end', text=student_data_level_1[0])

            student_data_level_2 = [f"Группа: {student_info[1]}"]
            self.table.insert(student_node, 'end', text=student_data_level_2[0], values=student_data_level_2[1:],
                             open=False)

            student_data_level_2 = [f"Средний балл: {round(student_info[2], 2)}"]
            self.table.insert(student_node, 'end', text=student_data_level_2[0], values=student_data_level_2[1:],
                             open=False)
            for i, grade_info in enumerate(student_info[3], start=1):
                exam_data = f'{grade_info[0]}: {grade_info[1]}'
                self.table.insert(student_node, 'end', text=exam_data)
