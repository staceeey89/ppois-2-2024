from ticket import Ticket
from turnstile import Turnstile
from abstractions import AbstractTrain, AbstractPassenger, AbstractPlatform


class Passenger(AbstractPassenger):
    def __init__(self, name: str, cash: int):
        self.__name: str = name
        self.__cash: int = cash
        self.__ticket: Ticket = None
        self.__platform: AbstractPlatform = None
        self.__crossed_a_turnstile: bool = False

    @property
    def cash(self):
        return self.__cash

    def buy_a_ticket(self, ticket: Ticket):
        self.__cash -= ticket.cost
        self.__ticket = ticket

    def cross_a_turnstile(self, turnstile: Turnstile):
        self.__crossed_a_turnstile = turnstile.check(self.ticket)

    @property
    def name(self):
        return self.__name

    @property
    def ticket(self):
        return self.__ticket

    def choose_a_platform(self, platform: AbstractPlatform):
        try:
            if self.__crossed_a_turnstile:
                self.__platform = platform
            else:
                Exception(f"Passenger {self.name}, cross a turnstile!")
        except Exception as text:
            print(text)

    def board(self, train: AbstractTrain):
        try:
            if self.__platform is not None and self.__platform.train == train:
                train.add_passenger(self)
            elif self.__platform is None:
                Exception("Choose a platform!")
            elif self.__platform.train is None:
                Exception(f"Train is {self.__platform.train}")
        except Exception as text:
            print(text)

    def disembark(self, train: AbstractTrain):
        train.remove_passenger(self)
        self.__platform = train.platform
        train.platform.add_passenger(self)
