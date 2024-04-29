import unittest
from typegearsseason import Season
from wheels import Wheels

class TestWheels(unittest.TestCase):

    def setUp(self):

        self.wheels = Wheels(Season.summer, "Michelin", 2023)

    def test_initial_state(self):
    
        self.assertEqual(self.wheels.get_vendor(), "Michelin")
        self.assertEqual(self.wheels.get_creation_year(), 2023)
        self.assertEqual(self.wheels.get_state(), 9)
        self.assertEqual(self.wheels.get_season(), Season.summer)

        wheels_str = "{'Vendor': 'Michelin', 'Creation year': 2023, 'State': 9, " + \
                     "'Season': 'summer'}"
        
        self.assertEqual(str(self.wheels), wheels_str)

if __name__ == '__main__':
    unittest.main()