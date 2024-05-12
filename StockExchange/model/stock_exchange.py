from exception.stock_exchange_exception import StockExchangeException
from model.asset import Asset


class StockExchange:
    def __init__(self, name: str, assets: set[Asset]):
        self.__name = name
        self.__assets = assets.copy()

    @property
    def name(self):
        return self.__name

    @property
    def assets(self):
        return self.__assets

    @name.setter
    def name(self, value) -> None:
        self.__name = value

    @assets.setter
    def assets(self, value: set[Asset]) -> None:
        self.__assets = value

    # TODO index

    def add_asset(self, asset: Asset) -> None:
        if asset in self.__assets:
            raise StockExchangeException("Asset " + asset.info() + " is already exists")
        self.__assets.add(asset)
