from model.trader import Trader
from model.asset import Asset
from model.currency import Currency
from model.stock import Stock
from exception.buy_exception import BuySellException


def buy_asset(trader: Trader, asset: Asset, amount: int) -> None:
    if isinstance(asset, Currency):
        new_balance = trader.balance - asset.exchange_rate * amount * (1 + trader.broker.commission)
        if new_balance < 0:
            raise BuySellException("Insufficient funds")
        trader.balance = new_balance

    elif isinstance(asset, Stock):
        new_balance = trader.balance - asset.price * amount * (1 + trader.broker.commission)
        if new_balance < 0:
            raise BuySellException("Insufficient funds")
        trader.balance = new_balance
    else:
        raise BuySellException("Not correct instance")

    try:
        trader.portfolio[asset] = trader.portfolio[asset] + amount
    except KeyError:
        trader.portfolio[asset] = amount


def sell_asset(trader: Trader, asset: Asset, amount: int) -> None:
    try:
        actual_amount = trader.portfolio[asset]
        if actual_amount < amount:
            raise BuySellException("Can not sell this amount")
        trader.portfolio[asset] = actual_amount - amount
    except KeyError:
        raise BuySellException("No this asset in portfolio")

    if isinstance(asset, Currency):
        trader.balance = trader.balance + asset.exchange_rate * amount * (1 - trader.broker.commission)
    elif isinstance(asset, Stock):
        trader.balance = trader.balance + asset.price * amount * (1 - trader.broker.commission)
