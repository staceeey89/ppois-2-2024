class Product:
    def __init__(self, name: str, price: int) -> None:
        self.__name = name
        self.__price = price

    def get_name(self) -> str:
        return self.__name

    def get_price(self) -> int:
        return self.__price

    def set_price(self, new_price: int):
        self.__price = new_price

