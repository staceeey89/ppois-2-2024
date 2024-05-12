import unittest
from unittest.mock import patch
from unittest.mock import MagicMock
from Tables import Tables
from AbstractCustomer import AbstractCustomer

class TestTables(unittest.TestCase):
    
    def setUp(self):
        tablesDict = {1: "Free", 2: "Occupied", 3: "Reserved"}
        self.tables = Tables(tablesDict)
        self.customer = MagicMock(spec=AbstractCustomer)
        
    def test_get_info(self):
        with patch('builtins.print') as mocked_print:
            self.tables.getInfo()
            mocked_print.assert_has_calls([
                unittest.mock.call('1 - Free'),
                unittest.mock.call('2 - Occupied'),
                unittest.mock.call('3 - Reserved')
            ])
            
    def test_take_table_available(self):
        self.assertTrue(self.tables.takeTable(1, self.customer))
        
    def test_take_table_reserved(self):
        self.assertFalse(self.tables.takeTable(3, self.customer))
        
    def test_take_table_occupied(self):
        self.assertFalse(self.tables.takeTable(2, self.customer))
        
    def test_take_table_invalid_number(self):
        self.assertFalse(self.tables.takeTable(4, self.customer))
        
if __name__ == '__main__':
    unittest.main()
