from enum import Enum
from typing import List
from Person import Person


class Platform:
    def __init__(self):
        self.persons: List[Person] = []

    def increase_people_count(self, person: Person) -> None:
        self.persons.append(person)

    def decrease_people_count(self, person: Person) -> None:
        self.persons.remove(person)

    def get_people_count(self) -> int:
        return len(self.persons)


class Station:
    class StationName(Enum):
        STATION_A: str = "Station A"
        STATION_B: str = "Station B"
        STATION_C: str = "Station C"
        STATION_SERVICE: str = "Service station"

    def __init__(self, station_name: str):
        self.station_name: str = station_name
        self.platform: Platform = Platform()
