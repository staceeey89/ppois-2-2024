import unittest
from Tradestand import TradeStand
from Product import Product


class TestTradeStand(unittest.TestCase):
    def setUp(self):
        self.my_product = Product("brush", 10)
        self.my_trade_stand = TradeStand(self.my_product, 5)

    def test_product_loading(self):
        self.my_trade_stand.product_loading(7)
        assert 12 == self.my_trade_stand.get_quantity()


if __name__ == '__main__':
    unittest.main()
