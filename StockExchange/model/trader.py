from model.broker import Broker
from model.asset import Asset


class Trader:
    def __init__(self, name: str, broker: Broker, portfolio: dict[Asset, int], balance: float):
        self.__name = name
        self.__broker = broker
        self.__portfolio = portfolio
        self.__balance = balance

    @property
    def name(self):
        return self.__name

    @property
    def broker(self):
        return self.__broker

    @property
    def portfolio(self):
        return self.__portfolio

    @property
    def balance(self):
        return self.__balance

    @name.setter
    def name(self, name: str) -> None:
        self.__name = name

    @broker.setter
    def broker(self, broker: Broker) -> None:
        self.__broker = broker

    @portfolio.setter
    def portfolio(self, portfolio: dict[Asset, int]) -> None:
        self.__portfolio = portfolio

    @balance.setter
    def balance(self, balance: float) -> None:
        self.__balance = balance
