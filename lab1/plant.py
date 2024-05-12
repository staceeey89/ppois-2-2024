

class Plant:
    def __init__(self, name: str):
        self.name = name
        self.is_planted = False
        self.well_groomed = False
        self.is_watering = False
        self.is_dunged = False

    def planting(self):
        self.is_planted = True
        print("вы посадили растение " + self.name)

    def take_care_of(self):
        self.well_groomed = True
        print("вы полите грядки")

    def watering(self):
        self.is_watering = True

    def fertilizing(self):
        self.is_dunged = True
