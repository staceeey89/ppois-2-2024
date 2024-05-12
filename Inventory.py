from Menu import Menu

class Inventory(Menu):
    
    def __init__(self, ingridients=None) -> None:
        super().__init__()
        if ingridients:
            for i in ingridients:
                self.addItem(i)
