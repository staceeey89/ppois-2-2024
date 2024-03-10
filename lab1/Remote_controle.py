from Television import *
class Remote_control(Television):
    def __init__(self, _model: str, _price: str, _color: str, tv):
        super().__init__(_model, _price, _color)
        self.tv = tv

    def turn_tv_on(self):
        self.tv._protected_turn_on()

    def turn_tv_off(self):
        self.tv._protected_turn_off()

    def choose_new_channel(self, tv_channel: str):
        self.tv_channel = tv_channel
        self.tv._protected_choose_channel(tv_channel)
        self.tv._protected_check_channel()

    def print_data(self):
        print('Remote control info')
        print('_' * 42)
        print('|Model:', self._model, '|Color:', self._color, '|Price:', self._price)
        print('_' * 42)