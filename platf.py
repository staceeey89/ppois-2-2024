from typing import List
from station import Station
from abstractions import AbstractTrain, AbstractPassenger, AbstractPlatform


class Platform(AbstractPlatform):
    def __init__(self, number: int):
        self.__number: int = number
        self.__passengers: List[AbstractPassenger] = []
        self.__train: AbstractTrain = None
        self.__station: Station = None

    def add_passenger(self, passenger: AbstractPassenger):
        self.__passengers.append(passenger)

    def remove_passenger(self, passenger: AbstractPassenger):
        self.__passengers.remove(passenger)

    @property
    def train(self):
        return self.__train

    @property
    def number(self):
        return self.__number

    @train.setter
    def train(self, train: AbstractTrain):
        self.__train = train

    def get_passengers(self):
        return self.__passengers

    @property
    def station(self):
        return self.__station

    @station.setter
    def station(self, station: Station):
        self.__station = station
