import enum

from Tradestand import TradeStand
from Category import Category


class Place:
    def __init__(self, stands: list[TradeStand], need: str):
        self.__stands = stands
        for section in Category:
            if section.value == need:
                self.__need = section.value
                break

    def get_stands(self) -> list[TradeStand]:
        return self.__stands

    def print_stands(self):
        for item in self.__stands:
            print(f"{item.get_product().get_name()}: {item.get_product().get_price()} solids")

    def get_need(self) -> enum.Enum:
        return self.__need
