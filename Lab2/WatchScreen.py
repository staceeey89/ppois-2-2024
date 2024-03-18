from PyQt5.QtWidgets import QPushButton, QWidget, QLabel
from Design import Design


class WatchScreen(QWidget):
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

        Design.design_button(self.left_button, 194, 647, "<", 30, 30)
        Design.design_button(self.right_button, 275, 647, ">", 30, 30)
        Design.design_button(self.last_page_button, 320, 647, str(self.num_pages), 30, 30)
        Design.design_home_button(self.home_button, 25, 647)

        Design.design_text(self.current_page_text, 239, 647, "", 13, 25)

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

        self.hide()

    def set_num_pages_bd(self, controller, data_base):
        self.num_pages = controller.calculate_num_pages_bd(data_base)

    def set_num_pages_xml(self, controller, xml):
        self.num_pages = controller.calculate_num_pages_xml(xml)

    def clear_records(self):
        if len(self.list_records) > 1:
            for i in range(1, len(self.list_records)):
                for j in range(0, len(self.list_records[i])):
                    self.list_records[i][j].hide()
            self.list_records[0:len(self.list_records) - 1] = []

    def print_users(self, data_base, controller, xml):
        if not controller.check_bd_or_xml_file():
            self.print_users_bd(data_base, controller)
        else:
            self.print_users_xml(xml, controller)

    def print_users_bd(self, data_base, controller):
        self.x_pos = 15
        self.y_pos = 87
        self.temp_counter = 0
        self.num_pages = controller.calculate_num_pages_bd(data_base)
        self.current_page_text.setText(f"{self.counter_pages}/{self.num_pages}")
        self.last_page_button.setText(str(self.num_pages))
        self.clear_records()
        while self.counter_users < len(data_base.get_users()) and self.temp_counter < 10:
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
            self.counter_users += 1

            self.x_pos = 15
            self.y_pos += 50

    def print_users_xml(self, xml, controller):
        counter = 1
        self.x_pos = 15
        self.y_pos = 87
        self.temp_counter = 0
        self.num_pages = controller.calculate_num_pages_xml(xml)
        self.current_page_text.setText(f"{self.counter_pages}/{self.num_pages}")
        self.last_page_button.setText(str(self.num_pages))
        self.clear_records()
        while self.counter_users < xml.get_num_users() and self.temp_counter < 10:
            counter = 1
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
                                       str(xml.get_users()[self.counter_users][f"term{counter}"]),
                                       11, 50, 15)
                    counter += 1
                    self.list_records[self.temp_counter + 1][i].show()
                    self.x_pos += 21

            self.temp_counter += 1
            self.counter_users += 1

            self.x_pos = 15
            self.y_pos += 50

    def check_one_page(self):
        if self.num_pages == 1:
            return False
        else:
            return True

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
            self.print_users(data_base, controller, xml)

    def turn_left_page(self, data_base, controller, xml):
        if self.num_pages == 0:
            return
        if self.check_one_page():
            if self.counter_pages - 1 < 1:
                self.clear_records()
                self.counter_pages = self.num_pages
                if not controller.check_bd_or_xml_file():
                    self.counter_users = (data_base.find_num_watch_pages() -
                                          controller.get_users_on_last_page(data_base, xml))
                else:
                    self.counter_users = (xml.get_num_users() -
                                          controller.get_users_on_last_page(data_base, xml))
            else:
                self.clear_records()
                self.counter_pages -= 1
                self.counter_users -= (10 + self.temp_counter)
            self.print_users(data_base, controller, xml)

    def turn_last_page(self, data_base, controller, xml):
        if self.num_pages == 0:
            return
        if self.check_one_page():
            self.clear_records()
            self.counter_pages = self.num_pages
            if not controller.check_bd_or_xml_file():
                self.counter_users = (data_base.find_num_watch_pages() -
                                  controller.get_users_on_last_page(data_base, xml))
            else:
                self.counter_users = (xml.get_num_users() -
                                  controller.get_users_on_last_page(data_base, xml))
            self.print_users(data_base, controller, xml)

    def start_printing(self, data_base, controller, xml):
        self.counter_users = 0
        self.counter_pages = 1
        self.print_users(data_base, controller, xml)
