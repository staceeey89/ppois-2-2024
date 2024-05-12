import unittest
from Merchant import Merchant
from Product import Product
from Tradestand import TradeStand
from Place import Place


class TestMerchant(unittest.TestCase):
    def setUp(self):
        self.product1 = Product("Master and Margarita", 30)
        self.product2 = Product("Idiot", 35)
        self.trade_stand1 = TradeStand(self.product1, 3)
        self.trade_stand2 = TradeStand(self.product2, 2)
        self.place = Place([self.trade_stand1, self.trade_stand2], 'books')
        self.my_merchant = Merchant("Vittoria", 32, self.place)

    def test_expose_new_product(self):
        new_product = Product("War and Peace", 40)
        self.my_merchant.expose_new_product(new_product, 2)
        self.assertEqual(self.my_merchant.get_place().get_stands()[2].get_product().get_name(),
                         "War and Peace")

    def test_order_products(self):
        self.my_merchant.order_products()
        self.assertEqual(self.my_merchant.get_place().get_stands()[1].get_quantity(),
                         12)

    def test_make_discount(self):
        product = self.my_merchant.get_place().get_stands()[0].get_product()
        old_price = product.get_price()
        new_product = self.my_merchant.make_discount(product)
        self.assertEqual(old_price - 0.2*old_price,  new_product.get_price())
        assert new_product is product


if __name__ == '__main__':
    unittest.main()
