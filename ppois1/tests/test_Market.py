import unittest
from unittest import mock
from main import create
from main import main
from Customer import Customer
from Product import Product
from Market import Market


class TestMarket(unittest.TestCase):
    # @mock.patch('Market.input', create=True)
    def setUp(self):
        self.my_customer = Customer("Benny", 15, False, 40, 'books')
        self.my_market = create(self.my_customer)

    def test_find_need(self):
        found, merchant = self.my_market.find_need_match()
        self.assertTrue(found, True)
        m_need = merchant.get_place().get_need()
        self.assertEqual(m_need, self.my_customer.get_need())

    def test_trade(self):
        with mock.patch('builtins.input', return_value="2"):
            # product = Product("Master and Margarita", 30)
            success = self.my_market.trade()
            self.assertTrue(success)

    def test_ads(self):
        text = self.my_market.ads()
        self.assertEqual(text, """Did you know about this new medieval market in town?
                     Well...
                     Now you do! You are all welcome to walk, eat, drink, 
                     get excited and just have fun with your family!""")

    def test_get_customer(self):
        real_customer = self.my_market.get_customer()
        assert real_customer is self.my_customer

    def test_get_merchants(self):
        first_merchant = self.my_market.get_merchants()[0].get_name()
        expected_name = "Franko"
        assert first_merchant is expected_name

    def test_leave(self):
        with mock.patch('builtins.input', return_value="5"):
            line = main()
            self.assertEqual(line, "We will miss you! Dont forget to tell your friends about us!")

if __name__ == '__main__':
    unittest.main()
