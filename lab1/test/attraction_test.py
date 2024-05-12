import unittest
from geo_coordinate import GeoCoordinate
from attraction import Attraction


class TestAttraction(unittest.TestCase):

    def test_init(self):
        coordinate = GeoCoordinate(40.7128, 74.0060)
        attraction = Attraction("Statue of Liberty", coordinate, 1886)

        self.assertEqual(attraction.naming, "Statue of Liberty")
        self.assertEqual(attraction.coordinate, coordinate)
        self.assertEqual(attraction.date_of_building, 1886)

    def test_negative_date(self):
        with self.assertRaises(ValueError):
            Attraction("Statue of Liberty", GeoCoordinate(40.7128, 74.0060), -1)


if __name__ == '__main__':
    unittest.main()
