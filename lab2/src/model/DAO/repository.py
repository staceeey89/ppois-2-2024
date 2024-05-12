from abc import ABC, abstractmethod

from src.model.user import User


class Repository(ABC):
    @abstractmethod
    def save(self, record: User) -> None: pass
    @abstractmethod
    def get(self, uid: int) -> tuple: pass
    @abstractmethod
    def find(self, conditions: str) -> list[User]: pass
    @abstractmethod
    def list(self, *, offset, count) -> list[User]: pass
    @abstractmethod
    def erase(self, user: User) -> None: pass
    @abstractmethod
    def commit(self) -> None: pass
    @abstractmethod
    def count(self) -> int: pass

