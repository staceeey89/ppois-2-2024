class Food:
    
    def __init__(self, name: str, price: int, description: str, ingredients: list) -> None:
        self.__name = name
        self.__price = price
        self.__description = description
        self.__ingr = ingredients
        
    def getName(self) -> str:
        return self.__name
    
    def setName(self, name: str) -> None:
        self.__name = name
        
    def getPrice(self) -> int:
        return self.__price
    
    def setPrice(self, price: int) -> None:
        self.__price = price
        
    def setDescription(self, description: str) -> None:
        self.__description = description
        
    def getDescription(self) -> str:
        return self.__description
    
    def getIngr(self) -> list:
        return self.__ingr
        