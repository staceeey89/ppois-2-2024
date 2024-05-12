from Food import Food

class Menu:
    
    def __init__(self) -> None:
        self.__list_food = []
        
    def getItems(self) -> list:
        return self.__list_food
        
    def addItem(self, item: Food) -> None:
        self.__list_food.append(item)
        
    def removeItem(self, item: Food) -> None:
        if item in self.__list_food:
            self.__list_food.remove(item)
        else:
            return ("No such dish in menu")
