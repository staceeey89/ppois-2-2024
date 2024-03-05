import abc

from src.controller.input import Input


class Inputer(abc.ABC):
    @abc.abstractmethod
    def get_input(self) -> Input: pass