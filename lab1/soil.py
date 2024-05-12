

class Soil:
    def __init__(self, type_: str):
        self.soil_type = type_
        self.is_watered = False
        self.is_dunged = False

    def watering(self):
        self.is_watered = True

    def fertilizing(self):
        self.is_dunged = True


