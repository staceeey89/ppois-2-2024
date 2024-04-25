from geo_coordinate import GeoCoordinate
from check_data_type import check_data_type


class Attraction:
    def __init__(self, naming: str, coordinate: GeoCoordinate, date_of_building: int):

        if date_of_building <= 0:
            raise ValueError("Negative date")

        self.naming = naming
        self.coordinate = coordinate
        self.date_of_building = date_of_building
