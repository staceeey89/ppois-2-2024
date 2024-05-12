from exception.input_exception import InputException
from model import broker
from model.asset import Asset
from model.broker import Broker
from model.trader import Trader
from service.buy_sell_service import *


def print_main_menu() -> None:
    print('Write trader name or "exit" to exit')


def print_trader_menu(trader: Trader) -> None:
    print(trader.name + ' - ' + str(trader.balance) + ' ' + trader.broker.name + '\n' +

          '1 - view portfolio\n'
          '2 - change broker\n'
          '3 - view broker info\n'
          '4 - buy assets\n'
          '5 - sell assets\n'
          '6 - view brokers\n'
          '7 - exit')


def print_trader_portfolio(trader: Trader) -> None:
    for asset in trader.portfolio:
        print(asset.info() + ' --- ' + str(trader.portfolio[asset]))


def change_broker(trader: Trader, brokers: list[Broker], choice: str) -> None:
    for broker in brokers:
        if broker.name == choice:
            trader.broker = broker
            return
    raise InputException('No such broker')


def buy(trader: Trader, assets: set[Asset], symbol: str, amount: int) -> None:
    for asset in assets:
        if asset.symbol == symbol:
            buy_asset(trader, asset, amount)
            return
    raise BuySellException("No such asset")


def sell(trader: Trader, symbol: str, amount: int) -> None:
    for asset in trader.portfolio:
        if asset.symbol == symbol:
            sell_asset(trader, asset, amount)
            return
    raise BuySellException("No such asset")


def print_brokers(brokers: list[Broker]) -> None:
    for b in brokers:
        print(b.info())
        print('------------------------')
