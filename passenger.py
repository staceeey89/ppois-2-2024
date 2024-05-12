from ticket import Ticket
from turnstile import Turnstile
from station import Station
from abstractions import AbstractTrain, AbstractPassenger, AbstractPlatform


class Passenger(AbstractPassenger):
    def __init__(self, name: str, cash: int):
        self.__name: str = name
        self.__cash: int = cash
        self.__ticket: Ticket = None
        self.__platform: AbstractPlatform = None
        self.__station: Station = None
        self.__crossed_a_turnstile: bool = False

    @property
    def crossed_turnstile(self):
        return self.__crossed_a_turnstile
    @property
    def platform(self):
        return self.__platform

    @property
    def cash(self):
        return self.__cash

    @cash.setter
    def cash(self, cash: int):
        self.__cash = cash

    def buy_a_ticket(self, ticket: Ticket):
        self.__cash -= ticket.cost
        self.__ticket = ticket

    def cross_a_turnstile(self, turnstile: Turnstile):
        self.__crossed_a_turnstile = turnstile.check(self.ticket)

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name: str):
        self.__name = name

    @property
    def ticket(self):
        return self.__ticket

    def choose_a_platform(self, platform: AbstractPlatform):
        try:
            if self.__crossed_a_turnstile:
                self.__platform = platform
            else:
                raise RuntimeError(f"Пассажир {self.name}, пройди турникет!")
        except RuntimeError as e:
            print(e)

    @property
    def station(self):
        return self.__station

    @station.setter
    def station(self,station: Station):
        self.__station = station

    def board(self, train: AbstractTrain):
        try:
            if self.__platform is not None and self.__platform.train == train:
                train.add_passenger(self)
                self.__station = None
                self.__platform.remove_passenger(self)

            elif self.__platform is None:
                raise ValueError("Выберите платформу!")
            elif self.__platform.train is None:
                raise ValueError(f"Поезда нет на платформе!")
        except ValueError as e:
            print(e)

    def disembark(self, train: AbstractTrain):
        train.remove_passenger(self)
        self.__platform = train.platform
        self.__station = self.__platform.station
        train.platform.add_passenger(self)
