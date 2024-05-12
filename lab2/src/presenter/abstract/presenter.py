from abc import ABC, abstractmethod

from src.model.DAO.repository import Repository
from src.view.abstract.window import Window


class Presenter(ABC):
    def __init__(self, window: Window):
        self._window = window
        self._repo: Repository | None = None
        self._do_subscriptions()

    @abstractmethod
    def _do_subscriptions(self) -> None: pass
