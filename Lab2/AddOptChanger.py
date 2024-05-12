from PyQt5.QtWidgets import QWidget, QComboBox, QLabel
from Design import Design


class AddOptChanger(QWidget):
    def __init__(self, x_pos=0, y_pos=0, text=""):
        super().__init__()
        self.counter_opt_text = QLabel(self)
        self.combo_box = QComboBox(self)

        Design.design_text(self.counter_opt_text, x_pos, y_pos-25, text)
        Design.design_combo_box(self.combo_box, x_pos, y_pos)

        for i in range(1, 21):
            self.combo_box.addItem(str(i))