from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import QWidget, QLineEdit, QLabel, QPushButton

from Design import Design


class DelLastNameGroupScreen(QWidget):
    def __init__(self, data_base, controller, xml):
        super().__init__()
        self.setGeometry(-10, -30, 500, 700)

        self.input_last_name_field = QLineEdit(self)
        self.input_group_field = QLineEdit(self)
        self.last_name_text = QLabel(self)
        self.group_text = QLabel(self)
        self.delete_button = QPushButton(self)
        self.home_button = QPushButton(self)
        self.result_text = QLabel(self)

        Design.design_input_field(self.input_last_name_field, 160, 173, 160, 30)
        Design.design_input_field(self.input_group_field, 160, 268, 160, 30)
        self.input_last_name_field.setMaxLength(12)
        self.input_group_field.setMaxLength(6)
        self.input_group_field.setValidator(QIntValidator())

        Design.design_text(self.last_name_text, 160, 153, "Введите фамилию:",
                           15, 130, 17)
        Design.design_text(self.group_text, 160, 248, "Введите номер группы:",
                           15, 170, 17)
        Design.design_text(self.result_text, 129, 74, "", 24, 350)

        Design.design_button(self.delete_button, 174, 646, "Удалить")
        Design.design_home_button(self.home_button, 25, 647)

        self.delete_button.disconnect()
        self.delete_button.clicked.connect(lambda: self.print_del(data_base, controller, xml))

        self.hide()

    def print_del(self, data_base, controller, xml):
        try:
            if not controller.check_bd_or_xml_file():
                del_num = data_base.delete_last_name_group(self.input_last_name_field.text(),
                                                           self.input_group_field.text())
            else:
                del_num = xml.delete_users_last_name_group(self.input_last_name_field.text(),
                                                            self.input_group_field.text())
            if del_num == 0:
                self.result_text.setText("Ничего не удалено.")
            else:
                self.result_text.setText(f"Удаление {del_num} элементов.")
        except ValueError:
            self.result_text.setText("Ничего не удалено.")
            self.input_last_name_field.clear()
            self.input_group_field.clear()
        self.input_last_name_field.clear()
        self.input_group_field.clear()