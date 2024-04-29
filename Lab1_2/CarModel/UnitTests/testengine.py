import unittest
from engine import Engine

class TestEngine(unittest.TestCase):

    def setUp(self):

        self.engine = Engine(100, "MAN Diesel", 2023)

    def test_initial_state(self):
       
        self.assertEqual(self.engine.get_max_fuel_level(), 100)
        self.assertEqual(self.engine.get_fuel_level(), 0)
        self.assertEqual(self.engine.get_vendor(), "MAN Diesel")
        self.assertEqual(self.engine.get_creation_year(), 2023)
        self.assertEqual(self.engine.get_state(), 9)
        self.assertFalse(self.engine.is_oil())

        engine_str = "{'Vendor': 'MAN Diesel', 'Creation year': 2023, 'State': 9, " + \
                     "'Fuel level': 0, 'Max fuel level': 100, 'Oil': False}"
        
        self.assertEqual(str(self.engine), engine_str)

    def test_maximize_fuel_level(self):

        self.engine.maximize_fuel_level()
        self.assertEqual(self.engine.get_fuel_level(), 100)

    def test_fuel_waste(self):
        
        self.engine.maximize_fuel_level()
        self.engine.fuel_waste()
        self.assertAlmostEqual(self.engine.get_fuel_level(), 95, delta=0.01)

    def test_set_oil(self):

        self.engine.set_oil(True)
        self.assertTrue(self.engine.is_oil())

if __name__ == '__main__':
    unittest.main()