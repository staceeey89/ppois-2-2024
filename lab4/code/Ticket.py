class Ticket:
    def __init__(self, price: float):
        if price < 0:
            print("Invalid input. Default value 0")
            self.price: float = 0
        else:
            self.price: float = price
