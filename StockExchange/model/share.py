from model.stock import Stock


class Share(Stock):
    def __init__(self, symbol: str, name: str, price: float):
        super().__init__(symbol, name, price)

    def __eq__(self, other):
        return super().__eq__(other)

    def __hash__(self):
        return super().__hash__()

    def info(self) -> str:
        return 'Share ' + self.symbol + ' ' + self.name + ' ' + str(self.price)
