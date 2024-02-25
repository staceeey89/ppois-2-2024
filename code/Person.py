from Ticket import Ticket
from Turnstile import Turnstile


class Person:
    def __init__(self, name: str, money: float):
        self.name: str = name
        self.ticket: Ticket = None
        self.money: float = money
        self.platform = None

    def buy_ticket(self, ticket: Ticket) -> None:
        if ticket.price <= 0:
            print("Ticket price should be a positive value.")
        elif self.money >= ticket.price:
            self.money -= ticket.price
            self.ticket = ticket
            print(f"{self.name} has bought a ticket.")
        else:
            print(f"{self.name} does not have enough money to buy the ticket.")

    def enter_platform(self, platform, turnstile: Turnstile) -> None:
        if self.ticket:
            turnstile.unlock()
            self.platform = platform
            platform.increase_people_count(self)
            print(f"{self.name} has entered the platform.")
        else:
            print(f"{self.name} does not have a ticket.")
