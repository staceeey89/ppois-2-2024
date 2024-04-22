from AbstractCustomer import AbstractCustomer

class Payment:
    
    def __init__(self, money: int) -> None:
        self.__money = money
    
    def getMoney(self) -> str:
        return f"Balance: {self._money}руб."
    
    def pay(self, order, customer: AbstractCustomer) -> bool:
        cost = 0
        for i in order._list_order:
            if self.__money >= i.getPrice():
                self.__money -= i.getPrice()
                cost += i.getPrice()
            else:
                return False 
        customer.madeOrder()
        return True
