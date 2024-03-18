from PyQt5.QtWidgets import QWidget, QPushButton

from Design import Design


class SearchScreen(QWidget):
    def __init__(self, last_name_group_screen, last_name_opt_screen, group_opt_screen):
        super().__init__()
        self.setGeometry(-10, -30, 500, 700)
        self.search_last_name_grop_button = QPushButton(self)
        self.search_last_name_opt_button = QPushButton(self)
        self.search_group_opt_button = QPushButton(self)
        self.home_button = QPushButton(self)

        Design.design_button(self.search_last_name_grop_button, 86, 172,
                             "Поиск по фамилии и номеру группы", 328, 39)
        Design.design_button(self.search_last_name_opt_button, 86, 266,
                             "Поиск по фамилии и кол-ву работы", 328, 39)
        Design.design_button(self.search_group_opt_button, 86, 360,
                             "Поиск по номеру группы и колву работы", 328, 39)
        Design.design_home_button(self.home_button, 25, 614)

        self.search_last_name_grop_button.disconnect()
        self.search_last_name_grop_button.clicked.connect(lambda:
                            self.hide_search_screen_and_show_last_name_group_screen(last_name_group_screen))

        self.search_last_name_opt_button.disconnect()
        self.search_last_name_opt_button.clicked.connect(lambda:
                            self.hide_search_screen_and_show_last_name_opt_screen(last_name_opt_screen))

        self.search_group_opt_button.disconnect()
        self.search_group_opt_button.clicked.connect(lambda:
                            self.hide_search_screen_and_show_group_opt_screen(group_opt_screen))

        self.hide()

    def hide_search_screen_and_show_last_name_group_screen(self, last_name_group_screen):
        self.hide()
        last_name_group_screen.show()

    def hide_search_screen_and_show_last_name_opt_screen(self, last_name_opt_screen):
        self.hide()
        last_name_opt_screen.show()

    def hide_search_screen_and_show_group_opt_screen(self, group_opt_screen):
        self.hide()
        group_opt_screen.show()
