class ControlButtons:
    def __init__(self):
        self.start_b: bool = False
        self.using_power: int = 0

    def change_power(self, wishful_power: int):
        self.using_power = wishful_power
        print(f"Мощность {self.using_power} Вт назначена.")
