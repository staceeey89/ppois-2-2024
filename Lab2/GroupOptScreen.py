from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import QPushButton, QWidget, QLabel, QLineEdit, QComboBox
from Design import Design


class GroupOptScreen(QWidget):
    def __init__(self, controller, data_base, xml):
        super().__init__()
        self.setGeometry(-10, -30, 500, 700)
        self.y_pos = 57
        self.x_pos = 15
        self.temp_counter = 0
        self.num_pages = 0
        self.counter_pages = 1
        self.counter_users = 0
        self.list_records = []
        self.list_records.append([])

        self.left_button = QPushButton(self)
        self.right_button = QPushButton(self)
        self.last_page_button = QPushButton(self)
        self.current_page_text = QLabel(self)
        self.home_button = QPushButton(self)
        self.search_button = QPushButton(self)
        self.input_group_field = QLineEdit(self)
        self.input_high_opt_field = QLineEdit(self)
        self.input_low_opt_field = QLineEdit(self)
        self.group_text = QLabel(self)
        self.high_opt_text = QLabel(self)
        self.low_opt_text = QLabel(self)

        self.first_page_button = QPushButton(self)
        self.all_users = QLabel(self)
        self.users_page = QLabel(self)
        self.number_users_page = QComboBox(self)

        Design.design_combo_box(self.number_users_page, 25, 25, 45, 30)
        Design.design_button(self.left_button, 343, 647, "<", 30, 30)
        Design.design_button(self.right_button, 422, 647, ">", 30, 30)
        Design.design_button(self.last_page_button, 463, 647, str(self.num_pages), 30, 30)
        Design.design_button(self.search_button, 200, 646, "Найти", 130)
        Design.design_home_button(self.home_button, 25, 647)

        Design.design_input_field(self.input_group_field, 15, 607, 129, 25, 10)
        Design.design_input_field(self.input_high_opt_field, 351, 607, 129, 25, 10)
        Design.design_input_field(self.input_low_opt_field, 187, 607, 129, 25, 10)

        Design.design_text(self.current_page_text, 375, 647, "0/0", 13, 35)
        Design.design_text(self.group_text, 15, 592, "Введите группу:",
                           11, 108, 13)
        Design.design_text(self.high_opt_text, 351, 592, "Введите вверхний предел:",
                           11, 129, 13, )
        Design.design_text(self.low_opt_text, 187, 592, "Введите нижний предел:",
                           11, 129, 13)

        Design.design_text(self.all_users, 80, 647, "", 13, 75)
        Design.design_text(self.users_page, 80, 30, "", 13, 100)
        Design.design_button(self.first_page_button, 160, 647, "1", 30, 30)

        for i in range(1, 11):
            self.number_users_page.addItem(str(i))

        self.input_group_field.setMaxLength(6)
        self.input_group_field.setValidator(QIntValidator())
        self.input_low_opt_field.setMaxLength(3)
        self.input_low_opt_field.setValidator(QIntValidator())
        self.input_high_opt_field.setMaxLength(3)
        self.input_high_opt_field.setValidator(QIntValidator())

        for i in range(0, 12):
            if i == 0:
                self.list_records[0].append(QLabel(self))
                Design.design_text(self.list_records[0][i], self.x_pos, self.y_pos, "ФИО")
                self.x_pos += 180
            elif i == 1:
                self.list_records[0].append(QLabel(self))
                Design.design_text(self.list_records[0][i], self.x_pos, self.y_pos, "Группа")
                self.x_pos += 100
            else:
                self.list_records[0].append(QLabel(self))
                Design.design_text(self.list_records[0][i], self.x_pos, self.y_pos, str(i - 1))
                self.x_pos += 20

        self.x_pos = 15
        self.y_pos += 30

        self.right_button.disconnect()
        self.right_button.clicked.connect(lambda: self.turn_right_page(data_base, controller, xml))

        self.left_button.disconnect()
        self.left_button.clicked.connect(lambda: self.turn_left_page(data_base, controller, xml))

        self.last_page_button.disconnect()
        self.last_page_button.clicked.connect(lambda: self.turn_last_page(data_base, controller, xml))

        self.search_button.disconnect()
        self.search_button.clicked.connect(lambda: self.print_search_users(data_base, controller, xml))

        self.first_page_button.disconnect()
        self.first_page_button.clicked.connect(lambda: self.turn_first_page(data_base, controller, xml))

        self.number_users_page.disconnect()
        self.number_users_page.currentIndexChanged.connect(lambda: self.start_printing(data_base, controller, xml))

        self.hide()

    def clear_records(self):
        if len(self.list_records) > 1:
            for i in range(1, len(self.list_records)):
                for j in range(0, len(self.list_records[i])):
                    self.list_records[i][j].hide()
            self.list_records[0:len(self.list_records) - 1] = []

    def print_users_bd(self, data_base, controller, xml):
        self.x_pos = 15
        self.y_pos = 87
        self.temp_counter = 0
        self.num_pages = controller.get_search_group_opt_pages(data_base, str(self.input_group_field.text()),
                                                               int(self.input_low_opt_field.text()),
                                                               int(self.input_high_opt_field.text()), xml,
                                                               int(self.number_users_page.currentText()))
        self.current_page_text.setText(f"{self.counter_pages}/{self.num_pages}")
        self.last_page_button.setText(str(self.num_pages))
        self.clear_records()
        while (self.counter_users < len(data_base.get_users()) and self.temp_counter
               < int(self.number_users_page.currentText())):
            if (str(data_base.get_users()[self.counter_users][3]) == str(self.input_group_field.text()) and
                    int(self.input_low_opt_field.text()) <= data_base.get_user_opt(self.counter_users)
                    <= int(self.input_high_opt_field.text())):
                self.list_records.append([])
                for i in range(0, 14):
                    if i == 0:
                        self.list_records[self.temp_counter + 1].append(QLabel(self))
                        Design.design_text(self.list_records[self.temp_counter + 1][i], self.x_pos, self.y_pos,
                                           str(data_base.get_users()[self.counter_users][i]),
                                           11, 60, 15)
                        self.list_records[self.temp_counter + 1][i].show()
                        self.x_pos += 40
                    elif i == 1:
                        self.list_records[self.temp_counter + 1].append(QLabel(self))
                        Design.design_text(self.list_records[self.temp_counter + 1][i], self.x_pos, self.y_pos,
                                           str(data_base.get_users()[self.counter_users][i]),
                                           11, 60, 15)
                        self.list_records[self.temp_counter + 1][i].show()
                        self.x_pos -= 40
                        self.y_pos += 15
                    elif i == 2:
                        self.list_records[self.temp_counter + 1].append(QLabel(self))
                        Design.design_text(self.list_records[self.temp_counter + 1][i], self.x_pos, self.y_pos,
                                           str(data_base.get_users()[self.counter_users][i]),
                                           11, 60, 15)
                        self.list_records[self.temp_counter + 1][i].show()
                        self.y_pos -= 15
                        self.x_pos += 185
                    elif i == 3:
                        self.list_records[self.temp_counter + 1].append(QLabel(self))
                        Design.design_text(self.list_records[self.temp_counter + 1][i], self.x_pos, self.y_pos,
                                           str(data_base.get_users()[self.counter_users][i]),
                                           11, 50, 15)
                        self.list_records[self.temp_counter + 1][i].show()
                        self.x_pos += 90
                    else:
                        self.list_records[self.temp_counter + 1].append(QLabel(self))
                        Design.design_text(self.list_records[self.temp_counter + 1][i], self.x_pos, self.y_pos,
                                           str(data_base.get_users()[self.counter_users][i]),
                                           11, 50, 15)
                        self.list_records[self.temp_counter + 1][i].show()
                        self.x_pos += 21

                self.temp_counter += 1
                self.x_pos = 15
                self.y_pos += 50

            self.counter_users += 1

        self.all_users.setText(f"Всего {str(data_base.get_num_users_search_group_opt(self.input_group_field.text(),
                                    int(self.input_low_opt_field.text()), int(self.input_high_opt_field.text())))}")
        self.users_page.setText(f"На странице {self.temp_counter}")

    def print_users_xml(self, xml, controller, data_base):
        self.x_pos = 15
        self.y_pos = 87
        self.temp_counter = 0
        self.num_pages = controller.get_search_group_opt_pages(data_base, str(self.input_group_field.text()),
                                                               int(self.input_low_opt_field.text()),
                                                               int(self.input_high_opt_field.text()),
                                                               xml,int(self.number_users_page.currentText()))
        self.current_page_text.setText(f"{self.counter_pages}/{self.num_pages}")
        self.last_page_button.setText(str(self.num_pages))
        self.clear_records()
        while (self.counter_users < xml.get_num_users() and self.temp_counter
               < int(self.number_users_page.currentText())):
            if (str(xml.get_users()[self.counter_users]["user_group"]) == str(self.input_group_field.text()) and
                    int(self.input_low_opt_field.text()) <= xml.get_user_opt(self.counter_users)
                    <= int(self.input_high_opt_field.text())):
                self.list_records.append([])
                for i in range(0, 14):
                    if i == 0:
                        self.list_records[self.temp_counter + 1].append(QLabel(self))
                        Design.design_text(self.list_records[self.temp_counter + 1][i], self.x_pos, self.y_pos,
                                           str(xml.get_users()[self.counter_users]["first_name"]),
                                           11, 60, 15)
                        self.list_records[self.temp_counter + 1][i].show()
                        self.x_pos += 40
                    elif i == 1:
                        self.list_records[self.temp_counter + 1].append(QLabel(self))
                        Design.design_text(self.list_records[self.temp_counter + 1][i], self.x_pos, self.y_pos,
                                           str(xml.get_users()[self.counter_users]["last_name"]),
                                           11, 60, 15)
                        self.list_records[self.temp_counter + 1][i].show()
                        self.x_pos -= 40
                        self.y_pos += 15
                    elif i == 2:
                        self.list_records[self.temp_counter + 1].append(QLabel(self))
                        Design.design_text(self.list_records[self.temp_counter + 1][i], self.x_pos, self.y_pos,
                                           str(xml.get_users()[self.counter_users]["patronymic"]),
                                           11, 60, 15)
                        self.list_records[self.temp_counter + 1][i].show()
                        self.y_pos -= 15
                        self.x_pos += 185
                    elif i == 3:
                        self.list_records[self.temp_counter + 1].append(QLabel(self))
                        Design.design_text(self.list_records[self.temp_counter + 1][i], self.x_pos, self.y_pos,
                                           str(xml.get_users()[self.counter_users]["user_group"]),
                                           11, 50, 15)
                        self.list_records[self.temp_counter + 1][i].show()
                        self.x_pos += 90
                    else:
                        self.list_records[self.temp_counter + 1].append(QLabel(self))
                        Design.design_text(self.list_records[self.temp_counter + 1][i], self.x_pos, self.y_pos,
                                           str(xml.get_users()[self.counter_users][f"term{i - 3}"]),
                                           11, 50, 15)
                        self.list_records[self.temp_counter + 1][i].show()
                        self.x_pos += 21

                self.temp_counter += 1
                self.x_pos = 15
                self.y_pos += 50

            self.counter_users += 1
        self.all_users.setText(f"Всего {str(xml.get_num_users_search_group_opt(
            self.input_group_field.text(), int(self.input_low_opt_field.text()),
            int(self.input_high_opt_field.text())))}")
        self.users_page.setText(f"На странице {self.temp_counter}")

    def print_users(self, data_base, controller, xml):
        if not controller.check_bd_or_xml_file():
            self.print_users_bd(data_base, controller, xml)
        else:
            self.print_users_xml(xml, controller, data_base)

    def print_search_users(self, data_base, controller, xml):
        self.clear_records()
        self.counter_users = 0
        self.counter_pages = 1
        try:
            if int(self.input_low_opt_field.text()) > int(self.input_high_opt_field.text()):
                self.input_low_opt_field.clear()
                self.input_high_opt_field.clear()
                self.counter_pages = 0
                self.num_pages = 0
                self.current_page_text.setText(f"{self.counter_pages}/{self.num_pages}")
                self.last_page_button.setText(f"{self.num_pages}")
            else:
                self.print_users(data_base, controller, xml)
        except ValueError:
            self.input_low_opt_field.clear()
            self.input_high_opt_field.clear()

    def check_one_page(self):
        if self.num_pages == 1:
            return False
        else:
            return True

    def turn_first_page(self, data_base, controller, xml):
        if self.num_pages == 0:
            return
        self.clear_records()
        self.counter_pages = 1
        self.counter_users = 0
        self.print_users(data_base, controller, xml)

    def turn_right_page(self, data_base, controller, xml):
        if self.num_pages == 0:
            return
        if self.check_one_page():
            if self.counter_pages + 1 > self.num_pages:
                self.clear_records()
                self.counter_pages = 1
                self.counter_users = 0
            else:
                self.clear_records()
                self.counter_pages += 1
            try:
                self.print_users(data_base, controller, xml)
            except ValueError:
                self.input_low_opt_field.clear()
                self.input_high_opt_field.clear()

    def turn_left_page(self, data_base, controller, xml):
        if self.num_pages == 0:
            return
        if self.check_one_page():
            if not controller.check_bd_or_xml_file():
                self.turn_left_page_bd(data_base, xml, controller)
            else:
                self.turn_left_page_xml(data_base, xml, controller)
            try:
                self.print_users(data_base, controller, xml)
            except ValueError:
                self.input_low_opt_field.clear()
                self.input_high_opt_field.clear()

    def turn_left_page_xml(self, data_base, xml, controller):
        if self.counter_pages - 1 < 1:
            self.clear_records()
            self.counter_pages = self.num_pages
            self.counter_users = (xml.get_num_users() -
                                  xml.get_pos_users_group_opt(
                                      controller.get_users_on_last_page_group_opt(data_base,
                                                                                  self.input_group_field.text(),
                                                                                  int(self.input_low_opt_field.text()),
                                                                                  int(self.input_high_opt_field.text()),
                                                                                  xml,
                                                                                  int(self.number_users_page.currentText())),
                                      self.input_group_field.text(),
                                      int(self.input_low_opt_field.text()),
                                      int(self.input_high_opt_field.text()),
                                      xml.get_users()[xml.get_num_users()-1]))
        else:
            self.clear_records()
            self.counter_pages -= 1
            self.counter_users -= xml.get_pos_users_group_opt(int(self.number_users_page.currentText())
                                                              + self.temp_counter,
                                                              self.input_group_field.text(),
                                                              int(self.input_low_opt_field.text()),
                                                              int(self.input_high_opt_field.text()),
                                                              xml.get_users()[xml.get_num_users()-1])

    def turn_left_page_bd(self, data_base, xml, controller):
        if self.counter_pages - 1 < 1:
            self.clear_records()
            self.counter_pages = self.num_pages
            self.counter_users = (data_base.find_num_watch_pages() -
                                  data_base.get_pos_users_group_opt(
                                      controller.get_users_on_last_page_group_opt(data_base,
                                                                                  self.input_group_field.text(),
                                                                                  int(self.input_low_opt_field.text()),
                                                                                  int(self.input_high_opt_field.text()),
                                                                                  xml,
                                                                                  int(self.number_users_page.currentText())),
                                      self.input_group_field.text(),
                                      int(self.input_low_opt_field.text()),
                                      int(self.input_high_opt_field.text()),
                                      data_base.get_users()[len(data_base.get_users())-1]))
        else:
            self.clear_records()
            self.counter_pages -= 1
            self.counter_users -= data_base.get_pos_users_group_opt(int(self.number_users_page.currentText())
                                                                    + self.temp_counter,
                                                                    self.input_group_field.text(),
                                                                    int(self.input_low_opt_field.text()),
                                                                    int(self.input_high_opt_field.text()),
                                                                    data_base.get_users()[self.counter_users-1])

    def turn_last_page(self, data_base, controller, xml):
        if self.num_pages == 0:
            return
        if self.check_one_page():
            if not controller.check_bd_or_xml_file():
                self.turn_last_page_bd(data_base, xml, controller)
            else:
                self.turn_last_page_xml(data_base, xml, controller)
            try:
                self.print_users(data_base, controller, xml)
            except ValueError:
                self.input_low_opt_field.clear()
                self.input_high_opt_field.clear()

    def turn_last_page_bd(self, data_base, xml, controller):
        self.clear_records()
        self.counter_pages = self.num_pages
        self.counter_users = (data_base.find_num_watch_pages() -
                              data_base.get_pos_users_group_opt(
                              controller.get_users_on_last_page_group_opt(data_base,
                                                                          self.input_group_field.text(),
                                                                          int(self.input_low_opt_field.text()),
                                                                          int(self.input_high_opt_field.text()),
                                                                          xml,
                                                                          int(self.number_users_page.currentText())),
                              self.input_group_field.text(),
                              int(self.input_low_opt_field.text()),
                              int(self.input_high_opt_field.text()),
                              data_base.get_users()[data_base.get_num_users()-1]))

    def turn_last_page_xml(self, data_base, xml, controller):
        self.clear_records()
        self.counter_pages = self.num_pages
        self.counter_users = (xml.get_num_users() -
                              xml.get_pos_users_group_opt(
                                  controller.get_users_on_last_page_group_opt(data_base,
                                                                              self.input_group_field.text(),
                                                                              int(self.input_low_opt_field.text()),
                                                                              int(self.input_high_opt_field.text()),
                                                                              xml,
                                                                              int(self.number_users_page.currentText())),
                                  self.input_group_field.text(),
                                  int(self.input_low_opt_field.text()),
                                  int(self.input_high_opt_field.text()),
                                  xml.get_users()[xml.get_num_users()-1]))

    def start_printing(self, data_base, controller, xml):
        self.num_pages = 0
        self.counter_users = 0
        self.counter_pages = 1
        self.clear_records()
        try:
            self.print_users(data_base, controller, xml)
        except ValueError:
            self.input_low_opt_field.clear()
            self.input_high_opt_field.clear()

    def zero_page(self):
        self.num_pages = 0
        self.counter_users = 0
        self.counter_pages = 1
