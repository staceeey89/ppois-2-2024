from typing import List
from Person import Person


class Station:
    def __init__(self, name: str):
        self.name: str = name
        self.persons: List[Person] = []
        self.trains = []

    def provide_security(self) -> None:
        print(f"Security is provided at station {self.name}...")

    def get_persons(self) -> List[str]:
        return [person.name for person in self.persons]

    def get_trains(self) -> List[str]:
        return [train.number for train in self.trains]

