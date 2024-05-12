from abc import ABC, abstractmethod


class Instrument(ABC):
    @abstractmethod
    def use(self):
        pass
