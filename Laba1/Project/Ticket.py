import random
class Ticket:
    def __init__(self, attraction):
        self.number = random.randint(1000, 9999)
        self._attraction = attraction


    @property
    def attraction(self):
        return self._attraction

    @attraction.setter
    def attraction(self, value):
        self._attraction = value




