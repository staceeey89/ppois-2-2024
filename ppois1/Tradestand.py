from Product import Product


class TradeStand:

    __ordered = False

    def __init__(self, product: Product, quantity: int) -> None:
        self.__product = product
        self.__quantity = quantity

    def get_ordered(self) -> bool:
        return self.__ordered

    def set_ordered(self, ordered: bool):
        self.__ordered = ordered

    def sell(self):
        self.__quantity -= 1

    def get_quantity(self) -> int:
        return self.__quantity

    def get_product(self) -> Product:
        return self.__product

    def product_loading(self, addition: int) -> None:
        self.__quantity += addition
        self.__ordered = False
