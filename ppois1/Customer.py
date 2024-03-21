import enum

from Person import Person
from Category import Category
from Product import Product


class Customer(Person):
    def __init__(self, name: str, age: int, cunning: bool, budget: int, need: str) -> None:
        Person.__init__(self, name, age, cunning)
        self.__budget = budget
        self._need: str
        for section in Category:
            if section.value == need:
                self._need = section.value
                break

    def buy(self, product: Product) -> bool:
        bought = False
        if self.__budget > product.get_price():
            self.__budget -= product.get_price()
            bought = True
            print(f"Your budget: {self.__budget}")
        return bought

    def get_need(self) -> Category:
        return self._need

    def get_cunning(self) -> bool:
        return self._cunning

    def get_budget(self):
        return self.__budget

    def visit_tavern(self):
        if self._age < 18:
            return "Don't you think you're too young for that?"
        else:
            return "Congrats! You're drunk now!"

# customer = Customer("Jhon", 24, True, 300, 'food')

