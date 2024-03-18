
class AmusementPark:
    def __init__(self, name:str):
        self.name = name
        self.attractions = list()

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def attractions(self):
        return self._attractions

    @attractions.setter
    def attractions(self, attractions):
        self._attractions = attractions

    def add_attraction(self, attraction):
        self._attractions.append(attraction)

    def check_attraction_availability(self, attraction_name):
        for attraction in self._attractions:
            if attraction.name == attraction_name:
                if len(attraction.queue.visitors) < attraction.capacity:
                    return True
                else:
                    return False
        raise Exception(f"Attraction '{attraction_name}' not found in the park.")

















