import abc
from typing import Callable


class Publisher(abc.ABC):
    events = ()

    def __init__(self):
        self._handlers: dict[str, list[Callable[[dict], None]]] = {}
        for event in self.events:
            self._handlers[event] = []

    def subscribe(self, event: str, handler: Callable):
        if event not in self._handlers:
            raise ValueError(f"No event {event} in {type(self)}")
        if handler not in self._handlers[event]:
            self._handlers[event].append(handler)

    def unsubscribe(self, event: str, handler: Callable):
        if event not in self._handlers:
            raise ValueError(f"No event {event} in {type(self)}")
        if handler in self._handlers[event]:
            self._handlers[event].remove(handler)

    def _notify(self, event: str, **kwargs):
        if event not in self._handlers:
            raise ValueError(f"No event {event} in {type(self)}")
        for handler in self._handlers[event]:
            handler(**kwargs)
