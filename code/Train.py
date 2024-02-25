from typing import List
from Station import Station
from Person import Person


class Train:
    def __init__(self, number: str, station: Station):
        self.number: str = number
        self.station: Station = station
        self.persons: List[Person] = []

    def load_passenger(self, persons: List[Person]) -> None:
        self.persons.extend(persons)
        for person in self.persons:
            self.station.platform.decrease_people_count(person)

    def unload_passenger(self) -> None:
        persons_to_remove = [person for person in self.persons]
        for person in persons_to_remove:
            self.persons.remove(person)
            self.station.platform.increase_people_count(person)

    @staticmethod
    def transportation_services() -> None:
        print("Maintenance is being carried out...")
