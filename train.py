from typing import List
from abstractions import AbstractTrain, AbstractPlatform, AbstractPassenger


class Train(AbstractTrain):
    def __init__(self):
        self.__passengers: List[AbstractPassenger] = []
        self.__platform: AbstractPlatform = None

    @property
    def platform(self):
        return self.__platform

    @platform.setter
    def platform(self, platform: AbstractPlatform):
        self.__platform = platform

    def add_passenger(self, passenger: AbstractPassenger):
        self.__passengers.append(passenger)

    def remove_passenger(self, passenger: AbstractPassenger):
        self.__passengers.remove(passenger)

    def switch_station(self, next_platform: AbstractPlatform):
        try:
            if next_platform.train is None:
                self.__platform = next_platform
                next_platform.train = self
            else:
                raise ValueError(f"На следующей платформе ({next_platform.number}) есть поезд ")
        except ValueError as e:
            print(e)

    def get_passengers(self):
        return self.__passengers
