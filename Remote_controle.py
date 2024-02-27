from Television import *
class Remote_control(Television):
    def __init__(self, model: str, price: str, color: str, tv):
        super().__init__(model, price, color)
        self.tv = tv

    def turn_tv_on(self):
        self.tv.turn_on()

    def turn_tv_off(self):
        self.tv.turn_off()

    def choose_new_channel(self, tv_channel: str):
        self.tv_channel = tv_channel
        self.tv.choose_channel(tv_channel)
        self.tv.check_channel()

    def print_data(self):
        print('Remote control info')
        print('_' * 42)
        print('|Model:', self.model, '|Color:', self.color, '|Price:', self.price)
        print('_' * 42)