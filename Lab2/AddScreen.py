from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout
from Design import Design
from AddOptChanger import AddOptChanger


class AddScreen(QWidget):
    def __init__(self, xml, data_base, controller):
        super().__init__()
        self.setGeometry(0, 0, 500, 700)

        self.sem1 = AddOptChanger(0, 62, "1")
        self.sem2 = AddOptChanger(0, 62, "2")
        self.sem3 = AddOptChanger(0, 62, "3")
        self.sem4 = AddOptChanger(0, 62, "4")
        self.sem5 = AddOptChanger(0, 62, "5")

        self.sem6 = AddOptChanger(0, 25, "6")
        self.sem7 = AddOptChanger(0, 25, "7")
        self.sem8 = AddOptChanger(0, 25, "8")
        self.sem9 = AddOptChanger(0, 25, "9")
        self.sem10 = AddOptChanger(0, 25, "10")

        self.layout = QVBoxLayout()  # Создайте один основной макет типа QVBoxLayout
        self.layout1 = QHBoxLayout()  # Подмакет 1
        self.layout2 = QHBoxLayout()

        self.layout1.addWidget(self.sem1)
        self.layout1.addWidget(self.sem2)
        self.layout1.addWidget(self.sem3)
        self.layout1.addWidget(self.sem4)
        self.layout1.addWidget(self.sem5)

        self.layout2.addWidget(self.sem6)
        self.layout2.addWidget(self.sem7)
        self.layout2.addWidget(self.sem8)
        self.layout2.addWidget(self.sem9)
        self.layout2.addWidget(self.sem10)

        self.layout.addLayout(self.layout1)
        self.layout.addSpacing(-400)
        self.layout.addLayout(self.layout2)

        self.setLayout(self.layout)

        self.input_first_name_field = QLineEdit(self)
        self.input_last_name_field = QLineEdit(self)
        self.input_patronymic_field = QLineEdit(self)
        self.input_group_field = QLineEdit(self)
        self.input_first_name_text = QLabel(self)
        self.input_last_name_text = QLabel(self)
        self.input_patronymic_text = QLabel(self)
        self.input_group_text = QLabel(self)
        self.home_button = QPushButton(self)
        self.add_button = QPushButton(self)
        self.result_text = QLabel(self)
        self.opt_text = QLabel(self)

        Design.design_input_field(self.input_first_name_field, 25, 393, 236, 33)
        self.input_first_name_field.setMaxLength(12)
        Design.design_input_field(self.input_last_name_field, 25, 465, 236, 33)
        self.input_last_name_field.setMaxLength(12)
        Design.design_input_field(self.input_patronymic_field, 25, 539, 236, 33)
        self.input_patronymic_field.setMaxLength(12)
        Design.design_input_field(self.input_group_field, 25, 613, 236, 33)

        self.input_group_field.setValidator(QIntValidator())
        self.input_group_field.setMaxLength(6)

        Design.design_home_button(self.home_button, 400, 614)

        Design.design_text(self.input_first_name_text, 35, 373,
                           "Введите имя студента:", 15, 180, 20)
        Design.design_text(self.input_last_name_text, 35, 446,
                           "Введите фамилию студента:", 15, 216, 20)
        Design.design_text(self.input_patronymic_text, 35, 519,
                           "Введите отчество студента:", 15, 212, 20)
        Design.design_text(self.result_text, 50, 300, "", 24, 450)
        Design.design_text(self.opt_text, 35, 250, "ОПТ за семестры", 20, 174)
        Design.design_text(self.input_group_text, 35, 580, "Введите группу:", 15, 130)

        Design.design_button(self.add_button, 307, 462, "Добавить")

        self.add_button.disconnect()
        self.add_button.clicked.connect(lambda: self.add_user(xml, data_base, controller))

        self.hide()

    def add_user_in_database(self, data_base, controller):
        if data_base.add_new_user(self.input_first_name_field.text(), self.input_last_name_field.text(),
                                  self.input_patronymic_field.text(), self.input_group_field.text(),
                                  int(self.sem1.combo_box.currentText()), int(self.sem2.combo_box.currentText()),
                                  int(self.sem3.combo_box.currentText()), int(self.sem4.combo_box.currentText()),
                                  int(self.sem5.combo_box.currentText()), int(self.sem6.combo_box.currentText()),
                                  int(self.sem7.combo_box.currentText()), int(self.sem8.combo_box.currentText()),
                                  int(self.sem9.combo_box.currentText()), int(self.sem10.combo_box.currentText()),
                                  controller):

            self.clear_input_fields()
            self.result_text.setText("Пользователь добавлен.")
        else:
            self.clear_input_fields()
            self.result_text.setText("Невозможно добавить пользователя.")

    def add_user_in_xml(self, xml):
        if xml.add_user_xml(self.input_first_name_field.text(), self.input_last_name_field.text(),
                                  self.input_patronymic_field.text(), self.input_group_field.text(),
                                  int(self.sem1.combo_box.currentText()), int(self.sem2.combo_box.currentText()),
                                  int(self.sem3.combo_box.currentText()), int(self.sem4.combo_box.currentText()),
                                  int(self.sem5.combo_box.currentText()), int(self.sem6.combo_box.currentText()),
                                  int(self.sem7.combo_box.currentText()), int(self.sem8.combo_box.currentText()),
                                  int(self.sem9.combo_box.currentText()), int(self.sem10.combo_box.currentText())):
            xml.update_users()
            self.result_text.setText("Пользователь добавлен.")
        else:
            self.result_text.setText("Невозможно добавить пользователя.")

    def add_user(self, xml, data_base, controller):
        if controller.check_bd_or_xml_file():
            self.add_user_in_xml(xml)
        else:
            self.add_user_in_database(data_base, controller)

    def clear_input_fields(self):
        self.input_first_name_field.clear()
        self.input_last_name_field.clear()
        self.input_patronymic_field.clear()
        self.input_group_field.clear()
