import abc

from src.DAO.repository import Repository
from src.controller.input import Input


class Command(abc.ABC):
    name: str = "command"

    def __init__(self, input_: Input, repository: Repository):
        self._repository = repository
        self._args = input_.args

    @property
    def args(self):
        return self._args.copy()

    @property
    def repository(self):
        return self._repository

    @abc.abstractmethod
    def execute(self): pass

    @abc.abstractmethod
    def can_execute(self) -> bool: pass
