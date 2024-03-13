import unittest
from passenger import Passenger


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.passenger = Passenger("ZHOPA", 50)

    def test_something(self):
        self.assertEqual(self.passenger.name, "ZHOPA")  # add assertion here
        self.assertEqual(self.passenger.cash, 50)  # add


if __name__ == '__main__':
    unittest.main()
