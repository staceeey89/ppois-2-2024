from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import QWidget, QLineEdit, QLabel, QPushButton

from Design import Design


class DelLastNameOptScreen(QWidget):
    def __init__(self, data_base, controller, xml):
        super().__init__()
        self.setGeometry(-10, -30, 500, 700)

        self.input_last_name_field = QLineEdit(self)
        self.input_low_opt_field = QLineEdit(self)
        self.last_name_text = QLabel(self)
        self.low_opt_text = QLabel(self)
        self.input_high_opt_field = QLineEdit(self)
        self.high_opt_text = QLabel(self)
        self.delete_button = QPushButton(self)
        self.home_button = QPushButton(self)
        self.result_text = QLabel(self)

        Design.design_input_field(self.input_last_name_field, 160, 173, 160, 30)
        Design.design_input_field(self.input_low_opt_field, 160, 268, 160, 30)
        Design.design_input_field(self.input_high_opt_field, 160, 366, 160, 30)
        self.input_last_name_field.setMaxLength(12)
        self.input_low_opt_field.setMaxLength(3)
        self.input_low_opt_field.setValidator(QIntValidator())
        self.input_high_opt_field.setMaxLength(3)
        self.input_high_opt_field.setValidator(QIntValidator())

        Design.design_text(self.last_name_text, 160, 153, "Введите фамилию:",
                           15, 130, 17)
        Design.design_text(self.low_opt_text, 160, 248, "Введите нижний предел::",
                           15, 170, 17)
        Design.design_text(self.high_opt_text, 160, 346, "Введите верхний предел:",
                           15, 180, 17)
        Design.design_text(self.result_text, 129, 74, "", 24, 350)

        Design.design_button(self.delete_button, 174, 646, "Удалить")
        Design.design_home_button(self.home_button, 25, 647)

        self.delete_button.disconnect()
        self.delete_button.clicked.connect(lambda: self.print_del(data_base, controller, xml))

        self.hide()

    def print_del(self, data_base, controller, xml):
        try:
            if not controller.check_bd_or_xml_file():
                del_num = data_base.delete_last_name_opt(self.input_last_name_field.text(),
                                    int(self.input_low_opt_field.text()), int(self.input_high_opt_field.text()))
            else:
                del_num = xml.delete_users_last_name_opt(self.input_last_name_field.text(),
                                    int(self.input_low_opt_field.text()), int(self.input_high_opt_field.text()))
            if del_num == 0:
                self.result_text.setText("Ничего не удалено.")
            else:
                self.result_text.setText(f"Удаление {del_num} элементов.")
        except ValueError:
            self.result_text.setText("Ничего не удалено.")
            self.input_last_name_field.clear()
            self.input_low_opt_field.clear()
            self.input_high_opt_field.clear()
        self.input_last_name_field.clear()
        self.input_low_opt_field.clear()
        self.input_high_opt_field.clear()
