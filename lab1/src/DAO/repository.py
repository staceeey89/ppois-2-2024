import  abc

from src.model.state import State


class Repository(abc.ABC):
    @abc.abstractmethod
    def get_states(self) -> list[State]: pass

    @abc.abstractmethod
    def get_state(self, name: str) -> State: pass

    @abc.abstractmethod
    def add_state(self, state: State): pass

    @abc.abstractmethod
    def remove_state(self, state: State): pass
    