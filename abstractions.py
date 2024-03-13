from abc import ABC, abstractmethod


class AbstractTrain(ABC):

    @abstractmethod
    def __init__(self, value):
        pass

    @abstractmethod
    def add_passenger(self, value):
        pass

    @abstractmethod
    def remove_passenger(self, value):
        pass

    @abstractmethod
    def switch_station(self, value):
        pass

    @property
    @abstractmethod
    def platform(self):
        pass

    @platform.setter
    @abstractmethod
    def platform(self, value):
        pass


class AbstractPassenger(ABC):
    @abstractmethod
    def __init__(self, value_1, value_2):
        pass

    @property
    @abstractmethod
    def cash(self):
        pass

    @abstractmethod
    def buy_a_ticket(self, value):
        pass

    @abstractmethod
    def cross_a_turnstile(self, value):
        pass

    @property
    @abstractmethod
    def name(self):
        pass

    @property
    @abstractmethod
    def ticket(self):
        pass

    @abstractmethod
    def choose_a_platform(self, value):
        pass

    @abstractmethod
    def board(self, value):
        pass

    @abstractmethod
    def disembark(self, value):
        pass


class AbstractPlatform(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def add_passenger(self, value):
        pass

    @abstractmethod
    def remove_passenger(self, value):
        pass

    @property
    @abstractmethod
    def train(self):
        pass

    @property
    @abstractmethod
    def number(self):
        pass

    @train.setter
    @abstractmethod
    def train(self, value):
        pass
