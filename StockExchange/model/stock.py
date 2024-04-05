from model.asset import Asset
from abc import abstractmethod


class Stock(Asset):
    def __init__(self, symbol: str, name: str, price: float):
        super().__init__(symbol, name)
        self.__price = price

    def __eq__(self, other):
        return super().__eq__(other)

    def __hash__(self):
        return super().__hash__()

    @property
    def price(self):
        return self.__price

    @price.setter
    def price(self, price: float) -> None:
        self.__price = price

    @abstractmethod
    def info(self) -> str:
        pass
