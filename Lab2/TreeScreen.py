from PyQt5.QtGui import QPen, QColor
from PyQt5.QtWidgets import QWidget, QPushButton, QGraphicsScene, QGraphicsView, QFrame

from Design import Design


class TreeScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(-10, -30, 500, 700)
        self.user_button = QPushButton(self)
        self.first_name_button = QPushButton(self)
        self.last_name_button = QPushButton(self)
        self.patronymic_button = QPushButton(self)
        self.user_group_button = QPushButton(self)
        self.terms_button = QPushButton(self)
        self.home_button = QPushButton(self)
        self.list_terms = []
        self.attribute_flag = False
        self.terms_flag = False

        Design.design_button(self.user_button, 225, 35, "user", 65, 65)
        Design.design_button(self.first_name_button, 9, 106, "first_name", 119,
                             50, 15, "#514E4E")
        Design.design_button(self.last_name_button, 191, 138, "last_name", 119,
                             50, 15, "#514E4E")
        Design.design_button(self.patronymic_button, 349, 107, "patronymic", 119
                             , 50, 15, "#514E4E")
        Design.design_button(self.user_group_button, 68, 242, "user_group", 119,
                             50, 15, "#514E4E")
        Design.design_button(self.terms_button, 315, 242, "terms", 119, 50)
        Design.design_home_button(self.home_button, 47, 625)

        self.x_pos = 306
        self.y_pos = 304

        for i in range(1, 11):
            self.list_terms.append(QPushButton(self))
            if i % 2 != 0:
                Design.design_button(self.list_terms[i - 1], self.x_pos, self.y_pos, f"term{i}",
                                     65, 65, 15, "#514E4E")
            else:
                self.x_pos += 72
                Design.design_button(self.list_terms[i - 1], self.x_pos, self.y_pos, f"term{i}",
                                     65, 65, 15, "#514E4E")
                self.x_pos -= 72
                self.y_pos += 77

        self.hide_show_attributes()

        self.user_button.disconnect()
        self.user_button.clicked.connect(self.change_condition_attributes)

        self.terms_button.disconnect()
        self.terms_button.clicked.connect(self.change_condition_terms)

        self.hide()

    def change_condition_attributes(self):
        if self.attribute_flag:
            self.attribute_flag = False
            self.terms_flag = False
        else:
            self.attribute_flag = True
        self.hide_show_attributes()

    def change_condition_terms(self):
        if self.terms_flag:
            self.terms_flag = False
        else:
            self.terms_flag = True
        self.hide_show_terms()

    def hide_show_attributes(self):
        if self.attribute_flag:
            self.first_name_button.show()
            self.last_name_button.show()
            self.patronymic_button.show()
            self.user_group_button.show()
            self.terms_button.show()
        else:
            self.first_name_button.hide()
            self.last_name_button.hide()
            self.patronymic_button.hide()
            self.user_group_button.hide()
            self.terms_button.hide()
            self.hide_show_terms()

    def hide_show_terms(self):
        if self.terms_flag:
            for term in self.list_terms:
                term.show()
        else:
            for term in self.list_terms:
                term.hide()
