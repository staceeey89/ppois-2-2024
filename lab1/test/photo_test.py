import unittest
from attraction import Attraction
from geo_coordinate import GeoCoordinate
from photo import Photo


class TestPhoto(unittest.TestCase):

    def test_init(self):
        attraction = Attraction("Eiffel Tower", GeoCoordinate(48.8582, 2.2945), 1889)
        photo = Photo(attraction, 1080, 1920, 5)

        self.assertEqual(photo.attraction, attraction)
        self.assertEqual(photo.height, 1080)
        self.assertEqual(photo.width, 1920)
        self.assertEqual(photo.beautiful_level, 5)

    def test_negative_size(self):
        attraction = Attraction("Eiffel Tower", GeoCoordinate(48.8582, 2.2945), 1889)

        with self.assertRaises(ValueError):
            Photo(attraction, -1, 1920, 5)

        with self.assertRaises(ValueError):
            Photo(attraction, 1080, -1, 5)

    def test_browsing_photo(self):
        attraction = Attraction("Eiffel Tower", GeoCoordinate(48.8582, 2.2945), 1889)
        photo = Photo(attraction, 1080, 1920, 5)

        self.assertEqual(photo.browsing_photo(), attraction)


if __name__ == '__main__':
    unittest.main()
