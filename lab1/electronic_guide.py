import random


from geo_map import GeoMap
from data_base import DateBase
from geo_coordinate import GeoCoordinate
from path import Path
from photo import Photo


class ElectronicGuide(GeoMap):
    def __init__(self, list_of_attraction: list, current_coordinate: GeoCoordinate):
        coordinate_to_naming = dict()
        naming_to_attraction = dict()
        naming_to_information = dict()
        naming_to_photo = dict()

        for attraction in list_of_attraction:
            coordinate_to_naming[attraction.coordinate] = attraction.naming
            naming_to_attraction[attraction.naming] = attraction
            naming_to_information[attraction.naming] = DateBase.get_information(attraction)
            naming_to_photo[attraction.naming] = Photo(attraction, int(random.random() % 100), int(random.random() % 100), int(random.random()%100))

        super().__init__(coordinate_to_naming)

        self.current_coordinate = current_coordinate
        self.naming_to_attraction = naming_to_attraction
        self.naming_to_information = naming_to_information
        self.naming_to_photo = naming_to_photo

    def browsing_photo(self, naming: str):
        return self.naming_to_photo[naming]

    def get_path(self, naming_start: str, naming_finish: str):
        coordinate_start = GeoCoordinate(0, 0)
        coordinate_finish = GeoCoordinate(0, 0)
        flag_start = False
        flag_finish = False

        for key, value in self.coordinate_to_naming:
            if value == naming_start:
                coordinate_start = key
                flag_start = True
            if value == naming_finish:
                coordinate_finish = key
                flag_finish = True

        if not flag_start or not flag_finish:
            raise ValueError("Incorrect naming")

        return Path(coordinate_start, coordinate_finish)

    def movement(self, next_naming: str):
        next_coordinate = GeoCoordinate(0,0)
        flag = False

        for key, value in self.coordinate_to_naming:
            if value == next_naming:
                next_coordinate = key
                flag = True

        if not flag:
            raise ValueError("Incorrect naming")

        self.current_coordinate = next_coordinate

    def get_information(self, naming: str):
        return self.naming_to_information[naming]

    def feedback_publication(self, text: str):
        current_attraction = self.naming_to_attraction[self.coordinate_to_naming[self.current_coordinate]]
        DateBase.feedback_publication(current_attraction, text)

