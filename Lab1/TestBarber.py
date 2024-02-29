import unittest
from client import Client
from barber import Barber
from HairClipper import HairClipper
from CurlingIron import CurlingIron


class TestBarber(unittest.TestCase):
    def setUp(self):
        self.barber = Barber("John")
        self.client_short_thin = Client("John", "2", "9", "1", "2", "1")
        self.client_long_thick = Client("Pit", "2", "9", "1", "20", "2")
        new_hair_clipper = HairClipper()
        self.barber.add_instrument(new_hair_clipper)
        new_curling_iron = CurlingIron()
        self.barber.add_instrument(new_curling_iron)

    def test_make_haircut_short_hair(self):
        response = self.barber.make_haircut(self.client_short_thin)
        self.assertIn("Выполняется стрижка коротких волос", response)

    def test_make_haircut_long_hair(self):
        response = self.barber.make_haircut(self.client_long_thick)
        self.assertIn("Выполняется стрижка длинных волос", response)

    def test_make_hair_styling_short_hair(self):
        curling_iron = CurlingIron()
        self.barber.add_instrument(curling_iron)
        response = self.barber.make_hair_styling(self.client_short_thin)
        self.assertIn("Выполняется укладка коротких волос", response)

    def test_make_hair_styling_long_hair(self):
        response = self.barber.make_hair_styling(self.client_short_thin)
        self.assertIn("Для тонких волос используется плойка с температурой 80 градусов", response)

    def test_make_consultation_long_thick_hair(self):
        response = self.barber.make_consultation(self.client_long_thick)
        self.assertIn("Выполнена консультация по уходу за длинными плотными волосами", response)

    def test_available(self):
        self.assertTrue(self.barber.available)
        self.barber.available = False
        self.assertFalse(self.barber.available)

    def test_add_instrument(self):
        clipper = HairClipper()
        self.barber.add_instrument(clipper)
        self.assertIn(clipper, self.barber.instruments)
        self.assertNotIn("NotAnInstrument", self.barber.instruments)

    def test_name(self):
        self.assertEqual(self.barber.name, "John")


if __name__ == '__main__':
    unittest.main()
