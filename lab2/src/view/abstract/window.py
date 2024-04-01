from abc import ABC, abstractmethod
from src.absract.publisher import Publisher
from tkinter import Tk


class Window(Tk, Publisher, ABC):
    window_title = "Title"

    def __init__(self):
        super().__init__()
        super(Tk, self).__init__()
        self._build()
        self.title(self.window_title)

    @abstractmethod
    def _build(self) -> None: pass

    def show(self) -> None: pass
