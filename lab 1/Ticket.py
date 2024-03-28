class Ticket:
    def __init__(self, price: int):
        if price <= 0:
            print("The ticket price must be more than 0. The price is set at 50")
            self.price: int = 50
        else:
            self.price: int = price
        self.purchased: bool = False

    def get_price(self) -> int:
        return self.price

    def get_purchased(self) -> bool:
        return self.purchased
