import unittest
from Customer import Customer

class TestCustomer(unittest.TestCase):
    
    def test_initialization(self):
        customer = Customer()
        self.assertFalse(customer.Ordered())
        
    def test_made_order(self):
        customer = Customer()
        customer.madeOrder()
        self.assertTrue(customer.Ordered())
        
if __name__ == '__main__':
    unittest.main()
