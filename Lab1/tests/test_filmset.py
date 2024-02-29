import unittest
from FilmSet import FilmSet


class FilmSetTestCase(unittest.TestCase):

    def test_getter_filmset(self):
        film_set = FilmSet("horror")
        self.assertEqual(film_set.get_film_set_type(), "horror")
