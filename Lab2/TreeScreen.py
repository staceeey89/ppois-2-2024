from PyQt5.QtGui import QPen, QColor
from PyQt5.QtWidgets import QWidget, QPushButton, QGraphicsScene, QGraphicsView, QFrame, QLabel

from Design import Design


class TreeScreen(QWidget):
    def __init__(self, data_base, controller, xml):
        super().__init__()
        self.setGeometry(-10, -30, 500, 700)
        self.user_list_elements = []
        self.y_pos = 253
        self.x_pos = 91
        self.num_pages = 0
        self.counter_pages = 1
        self.counter_users = -1
        self.main_elements_flag = False
        self.terms_elements_flag = False

        self.left_button = QPushButton(self)
        self.right_button = QPushButton(self)
        self.last_page_button = QPushButton(self)
        self.current_page_text = QLabel(self)
        self.first_page_button = QPushButton(self)
        self.all_users = QLabel(self)

        Design.design_button(self.left_button, 194, 647, "<", 30, 30)
        Design.design_button(self.right_button, 275, 647, ">", 30, 30)
        Design.design_button(self.last_page_button, 320, 647, str(self.num_pages), 30, 30)
        Design.design_button(self.first_page_button, 160, 647, "1", 30, 30)
        Design.design_text(self.current_page_text, 225, 647, "0/0", 13, 35)
        Design.design_text(self.all_users, 80, 647, "", 13, 75)

        self.user_list_elements.append(QPushButton(self))
        Design.design_button(self.user_list_elements[0], 37, 43, "user",
                             83, 24, 12, fn_size=11)

        for i in range(1, 16):
            self.user_list_elements.append([])

        self.user_list_elements[1].append(QPushButton(self))
        Design.design_button(self.user_list_elements[1][0], 61, 78, "first_name",
                             83, 24, 12, fn_size=11)
        self.user_list_elements[2].append(QPushButton(self))
        Design.design_button(self.user_list_elements[2][0], 61, 113, "last_name",
                             83, 24, 12, fn_size=11)
        self.user_list_elements[3].append(QPushButton(self))
        Design.design_button(self.user_list_elements[3][0], 61, 148, "patronymic",
                             83, 24, 12, fn_size=11)
        self.user_list_elements[4].append(QPushButton(self))
        Design.design_button(self.user_list_elements[4][0], 61, 183, "user_group",
                             83, 24, 12, fn_size=11)
        self.user_list_elements[5].append(QPushButton(self))
        Design.design_button(self.user_list_elements[5][0], 61, 218, "terms",
                             83, 24, 12, fn_size=11)

        for i in range(6, 16):
            self.user_list_elements[i].append(QPushButton(self))
            Design.design_button(self.user_list_elements[i][0], self.x_pos, self.y_pos, f"term{i-5}",
                                 83, 24, 12, fn_size=11)
            self.y_pos += 35

        self.home_button = QPushButton(self)
        Design.design_home_button(self.home_button, 47, 625)

        for i in range(1, 16):
            self.user_list_elements[i][0].hide()

        self.user_list_elements[0].disconnect()
        self.user_list_elements[0].clicked.connect(self.hide_show_main_elements)

        self.user_list_elements[5][0].disconnect()
        self.user_list_elements[5][0].clicked.connect(self.hide_show_terms_elements)

        self.left_button.disconnect()
        self.left_button.clicked.connect(lambda: self.turn_left_page(data_base, controller, xml))

        self.right_button.disconnect()
        self.right_button.clicked.connect(lambda: self.turn_right_page(data_base, controller, xml))

        self.last_page_button.disconnect()
        self.last_page_button.clicked.connect(lambda: self.turn_last_page(data_base, controller, xml))

        self.first_page_button.disconnect()
        self.first_page_button.clicked.connect(lambda: self.turn_first_page(data_base, controller, xml))

        self.hide()

    def hide_show_main_elements(self):
        if self.main_elements_flag:
            self.hide_main_elements()
            self.main_elements_flag = False
        else:
            self.show_main_elements()
            self.main_elements_flag = True

    def hide_show_terms_elements(self):
        if self.terms_elements_flag:
            self.hide_terms_elements()
            self.hide_term_data()
            self.terms_elements_flag = False
        else:
            self.show_terms_elements()
            self.terms_elements_flag = True

    def show_main_elements(self):
        for i in range(1, 6):
            self.user_list_elements[i][0].show()

        self.user_list_elements[1][0].disconnect()
        self.user_list_elements[1][0].clicked.connect(self.hide_show_first_name)

        self.user_list_elements[2][0].disconnect()
        self.user_list_elements[2][0].clicked.connect(self.hide_show_last_name)

        self.user_list_elements[3][0].disconnect()
        self.user_list_elements[3][0].clicked.connect(self.hide_show_patronymic)

        self.user_list_elements[4][0].disconnect()
        self.user_list_elements[4][0].clicked.connect(self.hide_show_group)


    def hide_show_first_name(self):
        if self.user_list_elements[1][1].isVisible():
            self.user_list_elements[1][1].hide()
        else:
            self.user_list_elements[1][1].show()

    def hide_show_last_name(self):
        if self.user_list_elements[2][1].isVisible():
            self.user_list_elements[2][1].hide()
        else:
            self.user_list_elements[2][1].show()

    def hide_show_patronymic(self):
        if self.user_list_elements[3][1].isVisible():
            self.user_list_elements[3][1].hide()
        else:
            self.user_list_elements[3][1].show()

    def hide_show_group(self):
        if self.user_list_elements[4][1].isVisible():
            self.user_list_elements[4][1].hide()
        else:
            self.user_list_elements[4][1].show()

    def hide_show_term(self, num):
        if self.user_list_elements[num][1].isVisible():
            self.user_list_elements[num][1].hide()
        else:
            self.user_list_elements[num][1].show()

    def hide_main_elements(self):
        for i in range(1, 6):
            self.user_list_elements[i][0].hide()
        self.hide_main_data()
        self.terms_elements_flag = False
        self.hide_terms_elements()

    def hide_main_data(self):
        if len(self.user_list_elements[1]) <= 1:
            return
        for i in range(1, 5):
            self.user_list_elements[i][1].hide()

    def hide_term_data(self):
        if len(self.user_list_elements[1]) <= 1:
            return
        for i in range(6, 16):
            self.user_list_elements[i][1].hide()

    def show_terms_elements(self):
        for i in range(6, 16):
            self.user_list_elements[i][0].show()

            self.user_list_elements[6][0].disconnect()
            self.user_list_elements[6][0].clicked.connect(lambda: self.hide_show_term(6))

            self.user_list_elements[7][0].disconnect()
            self.user_list_elements[7][0].clicked.connect(lambda: self.hide_show_term(7))

            self.user_list_elements[8][0].disconnect()
            self.user_list_elements[8][0].clicked.connect(lambda: self.hide_show_term(8))

            self.user_list_elements[9][0].disconnect()
            self.user_list_elements[9][0].clicked.connect(lambda: self.hide_show_term(9))

            self.user_list_elements[10][0].disconnect()
            self.user_list_elements[10][0].clicked.connect(lambda: self.hide_show_term(10))

            self.user_list_elements[11][0].disconnect()
            self.user_list_elements[11][0].clicked.connect(lambda: self.hide_show_term(11))

            self.user_list_elements[12][0].disconnect()
            self.user_list_elements[12][0].clicked.connect(lambda: self.hide_show_term(12))

            self.user_list_elements[13][0].disconnect()
            self.user_list_elements[13][0].clicked.connect(lambda: self.hide_show_term(13))

            self.user_list_elements[14][0].disconnect()
            self.user_list_elements[14][0].clicked.connect(lambda: self.hide_show_term(14))

            self.user_list_elements[15][0].disconnect()
            self.user_list_elements[15][0].clicked.connect(lambda: self.hide_show_term(15))

    def clear_user_list(self):
        if len(self.user_list_elements[1]) <= 1:
            return
        for i in range(1, 16):
            if i != 5:
                self.user_list_elements[i].pop(1)

    def hide_terms_elements(self):
        for i in range(6, 16):
            self.user_list_elements[i][0].hide()
        self.hide_term_data()

    def fill_elements(self, data_base, xml, controller):
        self.clear_user_list()
        if not controller.check_bd_or_xml_file():
            self.fill_elements_bd(data_base)
        else:
            self.fill_elements_xml(xml)
        self.current_page_text.setText(f"{self.counter_pages}/{self.num_pages}")
        self.last_page_button.setText(str(self.num_pages))

    def fill_elements_bd(self, data_base):
        self.num_pages = data_base.get_num_users()
        self.x_pos = 164
        self.y_pos = 73
        self.counter_users += 1
        for i in range(1, 5):
            self.user_list_elements[i].append(QLabel(self))
            Design.design_text(self.user_list_elements[i][1], self.x_pos, self.y_pos,
                               f"{data_base.get_users()[self.counter_users][i - 1]}", 15, 140)
            self.y_pos += 35

        self.y_pos += 35
        self.x_pos += 30

        for i in range(6, 16):
            self.user_list_elements[i].append(QLabel(self))
            Design.design_text(self.user_list_elements[i][1], self.x_pos, self.y_pos,
                               f"{str(data_base.get_users()[self.counter_users][i - 2])}", 15, 140)
            self.y_pos += 35

    def fill_elements_xml(self, xml):
        self.num_pages = xml.get_num_users()
        self.x_pos = 164
        self.y_pos = 73
        self.counter_users += 1
        list_att = ["first_name", "last_name", "patronymic", "user_group"]
        for i in range(1, 5):
            self.user_list_elements[i].append(QLabel(self))
            Design.design_text(self.user_list_elements[i][1], self.x_pos, self.y_pos,
                               f"{xml.get_users()[self.counter_users][list_att[i-1]]}", 15, 140)
            self.y_pos += 35

        self.y_pos += 35
        self.x_pos += 30

        for i in range(6, 16):
            self.user_list_elements[i].append(QLabel(self))
            Design.design_text(self.user_list_elements[i][1], self.x_pos, self.y_pos,
                               f"{str(xml.get_users()[self.counter_users][f"term{i-5}"])}", 15, 140)
            self.y_pos += 35

    # Отображение страниц

    def turn_first_page(self, data_base, controller, xml):
        if self.num_pages == 0 or self.num_pages == 1:
            return
        self.hide_main_elements()
        self.clear_user_list()
        self.counter_pages = 1
        self.counter_users = -1
        self.fill_elements(data_base, xml, controller)

    def turn_right_page(self, data_base, controller, xml):
        if self.num_pages == 0 or self.num_pages == 1:
            return
        self.hide_main_elements()
        if self.counter_pages + 1 > self.num_pages:
            self.clear_user_list()
            self.counter_pages = 1
            self.counter_users = -1
        else:
            self.clear_user_list()
            self.counter_pages += 1
        self.fill_elements(data_base, xml, controller)

    def turn_left_page(self, data_base, controller, xml):
        if self.num_pages == 0 or self.num_pages == 1:
            return
        self.hide_main_elements()
        if self.counter_pages - 1 < 1:
            self.clear_user_list()
            self.counter_pages = self.num_pages
            if controller.check_bd_or_xml_file():
                self.counter_users = xml.get_num_users()-2
            else:
                self.counter_users = data_base.get_num_users() - 2
        else:
            self.clear_user_list()
            self.counter_pages -= 1
            self.counter_users -= 1
        self.fill_elements(data_base, xml, controller)

    def turn_last_page(self, data_base, controller, xml):
        if self.num_pages == 0 or self.num_pages == 1:
            return
        self.hide_main_elements()
        self.clear_user_list()
        self.counter_pages = self.num_pages
        if not controller.check_bd_or_xml_file():
            self.counter_users = data_base.get_num_users() - 2
        else:
            self.counter_users = xml.get_num_users() - 2
        self.fill_elements(data_base, xml, controller)

    def start_printing(self, data_base, xml, controller):
        self.counter_pages = 1
        self.counter_users = -1
        self.fill_elements(data_base, xml, controller)
        self.hide_main_data()
        self.hide_term_data()
        self.show()