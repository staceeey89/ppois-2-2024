from AbstractCustomer import AbstractCustomer

class Customer(AbstractCustomer):
    
    def __init__(self) -> None:
        self.__madeOrder = False
        self.__tookTable = False
        
    def madeOrder(self) -> None:
        self.__madeOrder = True
        
    def Ordered(self) -> bool:
        return self.__madeOrder
    
    def tookTable(self) -> None:
        self.__tookTable = True
        
    def didTookTable(self) -> bool:
        return self.__tookTable

    
    