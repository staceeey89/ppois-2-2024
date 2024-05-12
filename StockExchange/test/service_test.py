import unittest

from model.broker import Broker
from model.share import Share
from service.buy_sell_service import *
from exception.buy_exception import BuySellException


class TestBuySellAsset(unittest.TestCase):

    def setUp(self):
        self.currency = Currency('USD', 'US Dollar', 123, 100)
        self.share = Share('AAPL', 'Apple Inc.', 150.0)
        self.trader = Trader('John Doe', Broker('name', 'ls', set(), 0), dict(), 10000.0)

    def test_buy_currency(self):
        buy_asset(self.trader, self.currency, 1)
        self.assertEqual(self.trader.balance, 9900.0)

    def test_buy_stock(self):
        buy_asset(self.trader, self.share, 10)
        self.assertEqual(self.trader.balance, 8500.0)

    def test_buy_not_enough_funds(self):
        self.trader.balance = 1000.0
        with self.assertRaises(BuySellException):
            buy_asset(self.trader, self.share, 10)

    def test_buy_not_correct_instance(self):
        with self.assertRaises(BuySellException):
            buy_asset(self.trader, self.share, 6000)

    def test_sell_asset_not_in_portfolio(self):
        with self.assertRaises(BuySellException):
            sell_asset(self.trader, self.currency, 100)

    def test_sell_asset_incorrect_amount(self):
        self.trader.portfolio[self.currency] = 100
        with self.assertRaises(BuySellException):
            sell_asset(self.trader, self.currency, 200)

    def test_sell_currency(self):
        self.trader.portfolio[self.currency] = 100
        sell_asset(self.trader, self.currency, 50)
        self.assertEqual(self.trader.balance, 15000.0)

    def test_sell_stock(self):
        self.trader.portfolio[self.share] = 10
        sell_asset(self.trader, self.share, 5)
        self.assertEqual(self.trader.balance, 10750.0)


if __name__ == '__main__':
    unittest.main()
