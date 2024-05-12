import unittest
from Tables import Tables
from unittest.mock import MagicMock
from Reservation import Reservetion
from AbstractCustomer import AbstractCustomer

class Test_TestReservation(unittest.TestCase):
    
    def setUp(self):
        self.tables_data = {1: "Available", 2: "Occupied", 3: "Reserved"}
        self.reservation = Reservetion(self.tables_data)
        self.customer = MagicMock(spec=AbstractCustomer)
        
    def test_take_available_table(self):
        self.assertTrue(self.reservation.takeTable(1, self.reservation, self.customer))
        
    def test_take_occupied_table(self):
        self.assertFalse(self.reservation.takeTable(2, self.reservation, self.customer))
        
    def test_take_reserved_table(self):
        self.assertFalse(self.reservation.takeTable(3, self.reservation, self.customer))
        
    def test_take_nonexistent_table(self):
        self.assertFalse(self.reservation.takeTable(4, self.reservation, self.customer))
        
if __name__ == '__main__':
    unittest.main()
