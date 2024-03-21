import unittest
from Place import Place
from Product import Product
from Tradestand import TradeStand


class TestPlace(unittest.TestCase):
    def setUp(self):
        self.product1 = Product("carrot", 3)
        self.product2 = Product("tomato", 4)
        self.trade_stand1 = TradeStand(self.product1, 7)
        self.trade_stand2 = TradeStand(self.product2, 6)
        self.my_place = Place([self.trade_stand1, self.trade_stand2], 'food')

    def test_get_need(self):
        assert self.my_place.get_need() == 'food'

    def test_get_stands(self):
        assert self.my_place.get_stands()[1] is self.trade_stand2


if __name__ == '__main__':
    unittest.main()
