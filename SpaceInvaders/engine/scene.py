from abc import ABC, abstractmethod


class Scene(ABC):
    def __init__(self, *args):
        pass

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def render(self, screen):
        pass
