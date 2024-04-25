from attraction import Attraction


class GeoMap:
    def __init__(self, coordinate_to_naming: dict):

        self.coordinate_to_naming = coordinate_to_naming

    def add_attraction(self, attraction: Attraction):
        coordinate = attraction.coordinate
        naming = attraction.naming

        if coordinate in self.coordinate_to_naming:
            raise ValueError("Coordinate already exist")

        if naming in self.coordinate_to_naming.values():
            raise ValueError("Naming already exist")

        self.coordinate_to_naming[coordinate] = naming

    def remove_attraction(self, attraction: Attraction):
        coordinate = attraction.coordinate

        if coordinate is not self.coordinate_to_naming:
            raise ValueError("Such a place does not exist")

        del self.coordinate_to_naming[coordinate]
