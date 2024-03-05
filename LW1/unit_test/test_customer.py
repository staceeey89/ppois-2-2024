import os
import unittest
from unittest import TestCase
from Customer import Customer
from Order import Order


class CustomerTest(TestCase):

    
    def setUp(self):
        self.test_customer = Customer('John Doe')
        self.order = Order('Order', 'Java', 1000, 100)

    def test_add_order(self):
        self.test_customer.add_order_to_customer(self.order)
        assert len(self.test_customer.get_orders()) == 1

    def test_name_order(self):
        self.test_customer.delete_order(self.order)
        assert self.test_customer.get_num_of_orders() == 0

    def test_marked_order(self):
        self.test_customer.mark_order_as_completed('Order')
        self.test_customer.view_orders()
        assert self.test_customer.get_num_of_orders() == 0

    def tearDown(self):
        if os.path.exists(Customer.SAVE_FILE):
            os.remove(Customer.SAVE_FILE)

    def test_save_and_load_state(self):
        self.test_customer.save_state()
        self.assertTrue(os.path.exists(Customer.SAVE_FILE))
        loaded_customer = Customer.load_state()
        self.assertIsNotNone(loaded_customer)
        self.assertEqual(loaded_customer.get_name(), 'John Doe')

    def test_load_state_file_not_found(self):
        loaded_customer = Customer.load_state()
        self.assertIsNone(loaded_customer)


if __name__ == "__main__":
    unittest.main()

