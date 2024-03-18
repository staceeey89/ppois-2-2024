from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QLineEdit
import os
from Design import Design


class SelectFileScreen(QWidget):
    def __init__(self, controller, data_base, xml):
        super().__init__()
        self.setGeometry(-10, -30, 500, 700)
        self.result_text = QLabel(self)
        self.text_of_input = QLabel(self)
        self.input_file_name_field = QLineEdit(self)
        self.find_bd_button = self.find_bd_button = QPushButton(self)
        self.find_xml_button = QPushButton(self)
        self.home_button = QPushButton(self)

        Design.design_text(self.result_text, 185, 82, "", 20)
        Design.design_text(self.text_of_input, 102, 203, "Введите название файла (без расширения):",
                           15, 360)

        Design.design_input_field(self.input_file_name_field, 102, 227)

        Design.design_button(self.find_bd_button, 173, 350, "Найти бд")
        Design.design_button(self.find_xml_button, 173, 436, "Найти xml")

        Design.design_home_button(self.home_button, 25, 614)

        self.find_bd_button.disconnect()
        self.find_bd_button.clicked.connect(lambda: self.select_bd_file(controller, data_base))

        self.find_xml_button.disconnect()
        self.find_xml_button.clicked.connect(lambda: self.select_xml_file(controller, xml))

        self.hide()

    # Находит бд файл
    def select_bd_file(self, controller, data_base):
        if controller.connect_bd_file(data_base, f"data/{self.input_file_name_field.text()}.db"):
            if data_base.exist_users_table(controller):
                self.result_text.setText("БД Файл выбран.")
                self.result_text.adjustSize()
                self.input_file_name_field.clear()
                return True
            else:
                self.result_text.setText("Нет таблицы 'Users'.")
                self.result_text.adjustSize()
                self.input_file_name_field.clear()
                return False
        else:
            self.result_text.setText("Файла нет.")
            self.result_text.adjustSize()
            self.input_file_name_field.clear()
            return False

    def select_xml_file(self, controller, xml):
        if controller.connect_xml_file(xml, f"data/{self.input_file_name_field.text()}.xml"):
            self.result_text.setText("XML Файл выбран.")
            self.result_text.adjustSize()
            self.input_file_name_field.clear()
            xml.update_users()
            return True
        else:
            self.result_text.setText("Файла нет.")
            self.result_text.adjustSize()
            self.input_file_name_field.clear()
            return False

