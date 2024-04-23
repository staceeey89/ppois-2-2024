import tkinter as tk
from controller.contoller import Controller

class View:
    def __init__(self, controller: Controller):
        self.controller = controller
        self.root = tk.Tk()
        self.limit_for_main_table = 10
        self.root.geometry("1100x500")
        self.root.title("Sportsman info")
        self.f_for_buttons = tk.Frame(self.root)
        self.f_for_table = tk.Frame(self.root)
        self.f_for_pages_buttons = tk.Frame(self.root)

    def create_main_window(self):
        pass

    def start(self):
        self.create_main_window()
        self.root.mainloop()

