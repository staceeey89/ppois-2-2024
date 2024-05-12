from model.stock import Stock
from datetime import date


class Bond(Stock):
    def __init__(self, symbol: str, name: str, price: float, maturity_date: date):
        super().__init__(symbol, name, price)
        self.__maturity_date = maturity_date

    def __eq__(self, other):
        return super().__eq__(other)

    def __hash__(self):
        return super().__hash__()

    @property
    def maturity_date(self):
        return self.__maturity_date

    @maturity_date.setter
    def maturity_date(self, value: date) -> None:
        self.__maturity_date = value

    def info(self) -> str:
        return 'Bond ' + self.symbol + ' ' + self.name + ' ' + str(self.price) + ' ' + str(self.maturity_date)
