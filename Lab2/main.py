import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QToolButton, QMenu, QAction
from AppScreen import AppScreen


class Application(QMainWindow):
    def __init__(self):
        super().__init__()
        self.app_screen = AppScreen()
        self.create_tool_bar()
        self.setGeometry(0, 0, 500, 700)
        self.setFixedSize(500, 700)
        self.setStyleSheet("background-color: black")
        self.app_screen.setParent(self)

        self.app_screen.show()
        self.show()

    def create_tool_bar(self):
        # создаем панель инструментов
        toolbar = self.addToolBar('Tools')

        watch_tool_button = QToolButton()
        search_tool_button = QToolButton()
        add_tool_button = QToolButton()
        delete_tool_button = QToolButton()
        select_file_tool_button = QToolButton()
        tree_button = QToolButton()

        # создаем кнопку с выпадающим списком
        watch_tool_button.setText('Просмотр')

        search_tool_button.setText("Поиск")
        search_menu = QMenu(self)
        search_last_name_group_action = QAction("Поиск по фамилии и номеру группы", self)
        search_last_name_opt_action = QAction("Поиск по фамилии и кол-ву работы", self)
        search_group_opt_action = QAction("Поиск по номеру группы и кол-ву работы", self)
        search_menu.addAction(search_last_name_group_action)
        search_menu.addAction(search_last_name_opt_action)
        search_menu.addAction(search_group_opt_action)
        search_tool_button.setMenu(search_menu)
        search_tool_button.setPopupMode(QToolButton.MenuButtonPopup)
        search_menu.setStyleSheet("background-color: white")

        add_tool_button.setText("Добавление")

        delete_tool_button.setText("Удаление")
        delete_menu = QMenu(self)
        del_last_name_group_action = QAction("Удаление по фамилии и номеру группы", self)
        del_last_name_opt_action = QAction("Удаление по фамилии и пол-ву работы", self)
        del_group_opt_action = QAction("Удаление по номеру группы и кол-ву работы", self)
        delete_menu.addAction(del_last_name_group_action)
        delete_menu.addAction(del_last_name_opt_action)
        delete_menu.addAction(del_group_opt_action)
        delete_tool_button.setMenu(delete_menu)
        delete_tool_button.setPopupMode(QToolButton.MenuButtonPopup)
        delete_menu.setStyleSheet("background-color: white")

        select_file_tool_button.setText("Выбор файла")
        tree_button.setText("Дерево")

        toolbar.addWidget(watch_tool_button)
        toolbar.addWidget(add_tool_button)
        toolbar.addWidget(select_file_tool_button)
        toolbar.addWidget(tree_button)
        toolbar.addWidget(search_tool_button)
        toolbar.addWidget(delete_tool_button)

        toolbar.setStyleSheet("background-color: white")

        watch_tool_button.disconnect()
        watch_tool_button.clicked.connect(self.show_watch_screen)

        add_tool_button.disconnect()
        add_tool_button.clicked.connect(self.show_add_screen)

        select_file_tool_button.disconnect()
        select_file_tool_button.clicked.connect(self.show_select_file_screen)

        search_last_name_group_action.disconnect()
        search_last_name_group_action.triggered.connect(self.show_last_name_group_screen)

        search_last_name_opt_action.disconnect()
        search_last_name_opt_action.triggered.connect(self.show_last_name_opt_screen)

        search_group_opt_action.disconnect()
        search_group_opt_action.triggered.connect(self.show_group_opt_screen)

        del_last_name_group_action.disconnect()
        del_last_name_group_action.triggered.connect(self.show_del_last_name_group_screen)

        del_last_name_opt_action.disconnect()
        del_last_name_opt_action.triggered.connect(self.show_del_last_name_opt_screen)

        del_group_opt_action.disconnect()
        del_group_opt_action.triggered.connect(self.show_del_group_opt_screen)

        search_tool_button.disconnect()
        search_tool_button.clicked.connect(self.show_search_screen)

        delete_tool_button.disconnect()
        delete_tool_button.clicked.connect(self.show_delete_screen)

        tree_button.disconnect()
        tree_button.clicked.connect(self.show_tree_screen)

    def hide_all(self):
        self.app_screen.del_group_opt_screen.hide()
        self.app_screen.del_last_name_opt_screen.hide()
        self.app_screen.del_last_name_group_screen.hide()
        self.app_screen.delete_screen.hide()
        self.app_screen.group_opt_screen.hide()
        self.app_screen.last_name_opt_screen.hide()
        self.app_screen.main_screen.hide()
        self.app_screen.select_file_screen.hide()
        self.app_screen.add_screen.hide()
        self.app_screen.watch_screen.hide()
        self.app_screen.search_screen.hide()
        self.app_screen.last_name_group_screen.hide()

        self.app_screen.select_file_screen.input_file_name_field.clear()
        if self.app_screen.controller.open_file_name != "":
            self.app_screen.main_screen.activate_buttons()
        self.app_screen.add_screen.clear_input_fields()
        self.app_screen.last_name_group_screen.clear_records()
        self.app_screen.last_name_group_screen.input_last_name_field.clear()
        self.app_screen.last_name_group_screen.input_group_field.clear()
        self.app_screen.last_name_opt_screen.clear_records()
        self.app_screen.last_name_opt_screen.input_last_name_field.clear()
        self.app_screen.last_name_opt_screen.input_low_opt_field.clear()
        self.app_screen.last_name_opt_screen.input_high_opt_field.clear()
        self.app_screen.group_opt_screen.clear_records()
        self.app_screen.group_opt_screen.input_group_field.clear()
        self.app_screen.group_opt_screen.input_low_opt_field.clear()
        self.app_screen.group_opt_screen.input_high_opt_field.clear()
        self.app_screen.del_last_name_group_screen.input_group_field.clear()
        self.app_screen.del_last_name_group_screen.input_group_field.clear()
        self.app_screen.del_last_name_opt_screen.input_last_name_field.clear()
        self.app_screen.del_last_name_opt_screen.input_low_opt_field.clear()
        self.app_screen.del_last_name_opt_screen.input_high_opt_field.clear()
        self.app_screen.del_group_opt_screen.input_group_field.clear()
        self.app_screen.del_group_opt_screen.input_low_opt_field.clear()
        self.app_screen.del_group_opt_screen.input_high_opt_field.clear()
        self.app_screen.tree_screen.hide()

    def show_del_group_opt_screen(self):
        if self.check_connect_file():
            self.hide_all()
            self.app_screen.del_group_opt_screen.show()

    def show_del_last_name_opt_screen(self):
        if self.check_connect_file():
            self.hide_all()
            self.app_screen.del_last_name_opt_screen.show()

    def show_del_last_name_group_screen(self):
        if self.check_connect_file():
            self.hide_all()
            self.app_screen.del_last_name_group_screen.show()

    def show_delete_screen(self):
        if self.check_connect_file():
            self.hide_all()
            self.app_screen.delete_screen.show()

    def show_group_opt_screen(self):
        if self.check_connect_file():
            self.hide_all()
            self.app_screen.group_opt_screen.show()

    def show_last_name_opt_screen(self):
        if self.check_connect_file():
            self.hide_all()
            self.app_screen.last_name_opt_screen.show()

    def show_main_screen(self):
        self.hide_all()
        self.app_screen.main_screen.show()

    def show_select_file_screen(self):
        self.hide_all()
        self.app_screen.select_file_screen.show()

    def show_add_screen(self):
        if self.check_connect_file():
            self.hide_all()
            self.app_screen.add_screen.show()

    def show_watch_screen(self):
        if self.check_connect_file():
            self.hide_all()
            if not self.app_screen.controller.check_bd_or_xml_file():
                self.app_screen.watch_screen.set_num_pages_bd(self.app_screen.controller, self.app_screen.data_base)
            else:
                self.app_screen.watch_screen.set_num_pages_xml(self.app_screen.controller, self.app_screen.xml)

            self.app_screen.watch_screen.start_printing(self.app_screen.data_base,
                                                        self.app_screen.controller, self.app_screen.xml)
            self.app_screen.watch_screen.show()

    def show_search_screen(self):
        if self.check_connect_file():
            self.hide_all()
            self.app_screen.search_screen.show()

    def show_last_name_group_screen(self):
        if self.check_connect_file():
            self.hide_all()
            self.app_screen.last_name_group_screen.show()

    def show_tree_screen(self):
        self.hide_all()
        self.app_screen.tree_screen.show()

    def check_connect_file(self):
        if self.app_screen.controller.open_file_name != "":
            return True
        else:
            return False


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Application()
    window.show()
    sys.exit(app.exec_())
