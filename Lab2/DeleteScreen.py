from PyQt5.QtWidgets import QWidget, QPushButton

from Design import Design


class DeleteScreen(QWidget):
    def __init__(self, del_last_name_group_screen, del_last_name_opt_screen, del_group_opt_screen):
        super().__init__()
        self.setGeometry(-10, -30, 500, 700)

        self.del_last_name_group_button = QPushButton(self)
        self.del_last_name_opt_button = QPushButton(self)
        self.del_group_opt_button = QPushButton(self)
        self.home_button = QPushButton(self)

        Design.design_button(self.del_last_name_group_button, 86, 172,
                             "Удаление по фамилии и номеру группы", 340, 39)
        Design.design_button(self.del_last_name_opt_button, 86, 266,
                             "Удаление по фамилии и кол-ву работы", 340, 39)
        Design.design_button(self.del_group_opt_button, 86, 360,
                             "Удаление по номеру группы и кол-ву работы", 340, 39)
        Design.design_home_button(self.home_button, 25, 614)

        self.del_last_name_group_button.disconnect()
        self.del_last_name_group_button.clicked.connect(lambda:
                            self.hide_delete_screen_and_show_del_last_name_group_screen(del_last_name_group_screen))

        self.del_last_name_opt_button.disconnect()
        self.del_last_name_opt_button.clicked.connect(lambda:
                            self.hide_delete_screen_and_show_del_last_name_opt_screen(del_last_name_opt_screen))

        self.del_group_opt_button.disconnect()
        self.del_group_opt_button.clicked.connect(lambda:
            self.hide_delete_scree_and_show_del_group_opt_screen(del_group_opt_screen))

        self.hide()

    def hide_delete_screen_and_show_del_last_name_group_screen(self, del_last_name_group_screen):
        self.hide()
        del_last_name_group_screen.show()

    def hide_delete_screen_and_show_del_last_name_opt_screen(self, del_last_name_opt_screen):
        self.hide()
        del_last_name_opt_screen.show()

    def hide_delete_scree_and_show_del_group_opt_screen(self, del_group_opt_screen):
        self.hide()
        del_group_opt_screen.show()