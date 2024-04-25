import unittest


from geo_coordinate import GeoCoordinate
from attraction import Attraction
from geo_map import GeoMap


class TestGeoMap(unittest.TestCase):

    def setUp(self):
        self.coordinate_to_naming = {}
        self.geomap = GeoMap(self.coordinate_to_naming)

    def test_add_attraction(self):
        attraction = Attraction("Eiffel Tower", GeoCoordinate(48.8582, 2.2945), 1889)

        self.geomap.add_attraction(attraction)
        self.assertEqual(self.geomap.coordinate_to_naming[attraction.coordinate], attraction.naming)

        # Ensure a ValueError is raised when adding an attraction with an existing coordinate
        with self.assertRaises(ValueError):
            self.geomap.add_attraction(attraction)

        # Ensure a ValueError is raised when adding an attraction with an existing name
        attraction2 = Attraction("Statue of Liberty", GeoCoordinate(40.6892, 74.0445), 1886)
        with self.assertRaises(ValueError):
            self.geomap.add_attraction(attraction2)

    def test_remove_attraction(self):
        attraction = Attraction("Eiffel Tower", GeoCoordinate(48.8582, 2.2945), 1889)

        self.geomap.add_attraction(attraction)
        self.geomap.remove_attraction(attraction)

        # Ensure a ValueError is raised when removing an attraction that does not exist
        with self.assertRaises(ValueError):
            self.geomap.remove_attraction(attraction)


if __name__ == '__main__':
    unittest.main()