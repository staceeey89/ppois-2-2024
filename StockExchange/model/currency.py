from model.asset import Asset


class Currency(Asset):
    def __init__(self, symbol: str, name: str, code: int, exchange_rate: float):
        super().__init__(symbol, name)
        self.__code = code
        self.__exchange_rate = exchange_rate

    def __eq__(self, other):
        return super().__eq__(other)

    def __hash__(self):
        return super().__hash__()

    @property
    def code(self):
        return self.__code

    @property
    def exchange_rate(self):
        return self.__exchange_rate

    @code.setter
    def code(self, new_code: int) -> None:
        self.__code = new_code

    @exchange_rate.setter
    def exchange_rate(self, new_rate: float):
        self.__exchange_rate = new_rate

    def info(self) -> str:
        return ('Currency ' + self.symbol + ' ' + self.name + ' ' + str(self.code) + ' '
                + str(self.exchange_rate))
