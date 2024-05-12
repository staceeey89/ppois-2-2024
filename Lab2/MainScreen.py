from PyQt5.QtWidgets import QWidget, QPushButton, QToolButton, QMenu, QAction, QMainWindow
from Design import Design


class MainScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(-10, -30, 500, 700)

        self.watch_button = QPushButton(self)
        self.search_button = QPushButton(self)
        self.add_button = QPushButton(self)
        self.delete_button = QPushButton(self)
        self.select_file_button = QPushButton(self)
        self.tree_button = QPushButton(self)

        Design.design_button(self.watch_button, 173, 118, "Просмотр",
                             153, 39, 15, "#514E4E")
        Design.design_button(self.search_button, 173, 224, "Поиск",
                             153, 39, 15, "#514E4E")
        Design.design_button(self.add_button, 173, 330, "Добавление",
                             153, 39, 15, "#514E4E")
        Design.design_button(self.delete_button, 173, 436, "Удаление",
                             153, 39, 15, "#514E4E")
        Design.design_button(self.select_file_button, 173, 542, "Выбор файла")
        Design.design_button(self.tree_button, 173, 613, "Дерево",
                             153, 39, 15, "#514E4E")

    def activate_buttons(self):
        Design.design_button(self.watch_button, 173, 118, "Просмотр",
                             153, 39, 15, "#572774")
        Design.design_button(self.search_button, 173, 224, "Поиск",
                             153, 39, 15, "#572774")
        Design.design_button(self.add_button, 173, 330, "Добавление",
                             153, 39, 15, "#572774")
        Design.design_button(self.delete_button, 173, 436, "Удаление",
                             153, 39, 15, "#572774")
        Design.design_button(self.tree_button, 173, 613, "Дерево",
                             153, 39, 15, "#572774")