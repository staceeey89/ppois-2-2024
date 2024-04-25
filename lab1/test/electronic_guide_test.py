import unittest


from attraction import Attraction
from geo_map import GeoMap
from data_base import DateBase
from geo_coordinate import GeoCoordinate
from path import Path
from photo import Photo
from electronic_guide import ElectronicGuide


class TestElectronicGuide(unittest.TestCase):

    def setUp(self):
        attraction1 = Attraction("Eiffel Tower", GeoCoordinate(48.8582, 2.2945), 1889)
        attraction2 = Attraction("Statue of Liberty", GeoCoordinate(40.6892, -74.0445), 1886)
        list_of_attraction = [attraction1, attraction2]
        self.geomap = GeoMap(dict())
        self.electronic_guide = ElectronicGuide(list_of_attraction, GeoCoordinate(40.6892, -74.0445))

    def test_browsing_photo(self):
        photo = self.electronic_guide.browsing_photo("Eiffel Tower")
        self.assertIsInstance(photo, Photo)

    def test_get_path(self):
        path = self.electronic_guide.get_path("Eiffel Tower", "Statue of Liberty")
        self.assertIsInstance(path, Path)

    def test_movement(self):
        self.electronic_guide.movement("Eiffel Tower")
        self.assertNotEqual(self.electronic_guide.current_coordinate, GeoCoordinate(40.6892, -74.0445))

    def test_get_information(self):
        information = self.electronic_guide.get_information("Eiffel Tower")
        self.assertIsInstance(information, str)

    def test_feedback_publication(self):
        text = "Great place!"
        self.electronic_guide.feedback_publication(text)
        current_attraction = self.electronic_guide.naming_to_attraction["Eiffel Tower"]
        self.assertEqual(DateBase.attraction_to_feedback[current_attraction], text)


if __name__ == '__main__':
    unittest.main()