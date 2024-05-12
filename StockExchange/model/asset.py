from abc import ABC, abstractmethod


class Asset(ABC):
    def __init__(self, symbol, name):
        self.__symbol = symbol
        self.__name = name

    def __eq__(self, other):
        if not isinstance(other, Asset):
            return False
        return self.symbol == other.symbol

    def __hash__(self):
        return self.symbol.__hash__()

    @property
    def symbol(self):
        return self.__symbol

    @property
    def name(self):
        return self.__name

    @symbol.setter
    def symbol(self, value) -> None:
        self.__symbol = value

    @name.setter
    def name(self, value: str) -> None:
        self.__name = value

    @abstractmethod
    def info(self) -> str:
        pass
