from Food import Food

class Order:
    
    def __init__(self) -> None:
        self._list_order = []
            
    def removeItem(self, item: Food) -> None:
        if item in self._list_order:
            self._list_order.remove(item)
        else:
            return "No such dish in order"
        
    def addToOrder(self, dish: Food, ingredients: list) -> None:
        items_to_remove = []
        ingr_need = dish.getIngr()
        all_ingredients_available = True
        for ingr in ingr_need:
            if ingr not in ingredients:
                all_ingredients_available = False
                break
        if not all_ingredients_available:
            print("Не хватает ингредиентов для приготовления такого блюда", dish.getName())
            items_to_remove.append(dish)
        else:
            self._list_order.append(dish)
            print("Заказ добавлен", dish.getName())
        for item in items_to_remove:
            self.removeItem(item)
            
    def getTheOrder(self) -> list:
        return self._list_order
                
                
        
