class Screen:
    def __init__(self):
        self.britness: int = 50
        self.contrast: int = 50
        self.saturation: int = 50

    def add_britness(self, level: int):
        self.britness = level
        print(f'Britness(Яркость) added to level {level}')

    def add_contrast(self, level: int):
        self.contrast = level
        print(f'Contrast(Контрастность) added to level {level}')

    def add_saturation(self, level: int):
        self.saturation = level
        print(f'Saturation(Насыщенность) added to level {level}')
