import unittest
from Customer import Customer
from Product import Product


class TestCustomer(unittest.TestCase):
    def setUp(self):
        self.my_customer = Customer("Benny", 15, False, 40, 'books')
        self.product = Product("War and Peace", 35)

    def test_buy(self):
        old_budget = self.my_customer.get_budget()
        bought = self.my_customer.buy(self.product)
        self.assertEqual(self.my_customer.get_budget(), 5)
        self.assertEqual(self.my_customer.get_budget(), old_budget - 35)
        self.assertEqual(bought, True)

    def test_get_name(self):
        expected_name = "Georgy"
        assert self.my_customer.get_name() != expected_name

    def test_get_cunning(self):
        expected_cunning = False
        assert self.my_customer.get_cunning() == expected_cunning

    def test_visit_tavern(self):
        line = self.my_customer.visit_tavern()
        self.assertEqual(line, "Don't you think you're too young for that?")



if __name__ == '__main__':
    unittest.main()
