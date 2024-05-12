from model.currency import Currency
from model.stock_exchange import StockExchange
from model.asset import Asset
from model.share import Share
from model.bond import Bond
from exception.broker_exception import BrokerException


class Broker:
    def __init__(self, name: str, license_number: str, exchanges: set[StockExchange], commission: float):
        self.__name = name
        self.__license_number = license_number
        self.__exchanges = exchanges
        self.__commission = commission

    @property
    def name(self):
        return self.__name

    @property
    def license_number(self):
        return self.__license_number

    @property
    def exchanges(self):
        return set(self.__exchanges)

    @property
    def commission(self) -> float:
        return self.__commission

    @name.setter
    def name(self, value: str) -> None:
        self.__name = value

    @license_number.setter
    def license_number(self, value: str) -> None:
        self.__license_number = value

    @exchanges.setter
    def exchanges(self, value: str) -> None:
        self.__exchanges = value

    @commission.setter
    def commission(self, value: float) -> None:
        self.__commission = value

    def info(self) -> str:
        out = self.__name + ' ' + str(self.__license_number) + ' ' + str(self.commission * 100) + '%'
        for exchange in self.__exchanges:
            out += ' ' + exchange.name
        assets = self.get_all_assets()
        for asset in assets:
            out += '\n' + asset.info()
        return out

    def add_exchange(self, exchange: StockExchange) -> None:
        if exchange in self.__exchanges:
            raise BrokerException("This exchange is already exists")
        self.__exchanges.add(exchange)

    def get_all_assets(self) -> set[Asset]:
        assets = set()
        for exchange in self.__exchanges:
            assets.update(exchange.assets)
        return assets

    def get_all_currencies(self) -> set[Currency]:
        currencies = set()
        for exchange in self.__exchanges:
            currencies.update(set(filter(lambda currency: isinstance(currency, Currency), exchange.assets)))
        return currencies

    def get_all_shares(self) -> set[Share]:
        shares = set()
        for exchange in self.__exchanges:
            shares.update(set(filter(lambda share: isinstance(share, Share), exchange.assets)))
        return shares

    def get_all_bonds(self) -> set[Bond]:
        bonds = set()
        for exchange in self.__exchanges:
            bonds.update(set(filter(lambda bond: isinstance(bond, Bond), exchange.assets)))
        return bonds
