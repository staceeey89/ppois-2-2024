from abc import ABC, abstractmethod
from typing import Any

from car import Car


class AddDel(ABC):

    @abstractmethod
    def add(element: Any): pass

    @abstractmethod
    def rem(element: Any): pass
