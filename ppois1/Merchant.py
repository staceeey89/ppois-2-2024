from Person import Person
from Product import Product
from Tradestand import TradeStand
from Place import Place


class Merchant(Person):
    __income: int = 0

    def __init__(self, name: str, age: int, place: Place, cunning: bool = True):
        Person.__init__(self, name, age, cunning)
        self.__place = place

    def expose_new_product(self, product: Product, quantity: int):
        new_trade_stand = TradeStand(product, quantity)
        self.__place.get_stands().append(new_trade_stand)

    def order_products(self):
        for stand in self.__place.get_stands():
            if stand.get_quantity() >= 5:
                pass
            else:
                stand.set_ordered(True)
                stand.product_loading(10)

    def make_discount(self, product: Product) -> Product:
        print("Merchant: Alright, I'll make a discount 20%, just get off me already")
        product.set_price(int(product.get_price()-0.2*product.get_price()))
        print(f"Now the price is {product.get_price()} solids")
        return product

    def sell(self, product: Product):
        self.__income += product.get_price()
        for item in self.__place.get_stands():
            if item.get_product().get_name() == product.get_name():
                item.sell()
                self.order_products()

    def get_place(self) -> Place:
        return self.__place

    def get_income(self):
        return self.__income
