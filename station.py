from typing import List
from ticket import Ticket
from platf import Platform
from turnstile import Turnstile
from passenger import Passenger


class Station:
    def __init__(self, number: int):
        self.__number: int = number
        self.__passengers: List[Passenger] = []
        self.__ticket: Ticket = None
        self.__turnstile: Turnstile = None
        self.__platforms: List[Platform] = []

    def add_platform(self, platform: Platform):
        try:
            if len(self.__platforms) < 2:
                self.__platforms.append(platform)
            else:
                raise ValueError("Платформы уже две")
        except ValueError as e:
            print(e)

    def remove_platform(self, platform: Platform):
        self.__platforms.remove(platform)

    @property
    def turnstile(self):
        return self.__turnstile

    @turnstile.setter
    def turnstile(self, turnstile: Turnstile):
        self.__turnstile = turnstile

    @property
    def ticket(self):
        return self.__ticket

    @ticket.setter
    def ticket(self, ticket: Ticket):
        self.__ticket = ticket

    def sell_a_ticket(self, passenger: Passenger):
        try:
            if passenger.cash >= self.__ticket.cost:
                passenger.buy_a_ticket(self.ticket)
            else:
                raise ValueError(f"Passenger {passenger.name} doesn't have enough money")
        except ValueError as e:
            print(e)
            raise ValueError("Purchase has not been made!")


    def get_platforms(self):
        return self.__platforms

    @property
    def number(self):
        return self.__number
