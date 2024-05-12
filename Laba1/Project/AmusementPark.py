
class AmusementPark:
    def __init__(self, name):
        self.name: str = name
        self.attractions = []

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value


















