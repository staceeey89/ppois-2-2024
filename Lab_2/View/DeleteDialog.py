from View.WidgetGPASubject import WidgetGPASubgect
from View.WidgetGroup import WidgetSearchByGroup
from View.WidgetSubjectGrade import WidgetSubgectGrade
from View.ShowTable import ShowTable
from tkinter import *

class DeleteDialog:
    def __init__(self, controller,callback):
        self.controller = controller
        self.root = Tk()
        self.root.title("Удаление студентов")
        self.root.state('zoomed')
        self.root.minsize(800, 600)
        self.callback=callback
        self.radio_var = IntVar()
        self.radio_var.set(1)
        self.search_widget=None
        Radiobutton(self.root, text="Поиск по номеру группы",
                    variable=self.radio_var, value="1",
                    command=lambda: self.toggle_search_widget(1)).pack(anchor=W)
        Radiobutton(self.root, text="Поиск по предмету и балу",
                    variable=self.radio_var, value="2",
                    command=lambda: self.toggle_search_widget(2)).pack(anchor=W)
        Radiobutton(self.root, text="Поиск по предмету и среднему балу",
                    variable=self.radio_var, value="3",
                    command=lambda: self.toggle_search_widget(3)).pack(anchor=W)

        self.table_frame = Frame(self.root)
        self.table_frame.pack(expand=True, fill='both')
        self.toggle_search_widget(3)
        self.root.protocol("WM_DELETE_WINDOW", self.__close)
        self.root.mainloop()

    def __close(self):
        self.callback()
        self.controller.close_page("DeleteDialog")
        self.root.destroy()

    def toggle_search_widget(self, value):
        if self.search_widget:
            self.search_widget.destroy()
        if value == 1:
            self.search_widget = WidgetSearchByGroup(self.controller,mode='delete',master=self.root)
            self.search_widget.pack()
        if value == 2:
            self.search_widget = WidgetSubgectGrade(self.controller,mode='delete',master=self.root)
            self.search_widget.pack()
        elif value == 3:
            self.search_widget = WidgetGPASubgect(self.controller,mode='delete',master=self.root)
            self.search_widget.pack()
