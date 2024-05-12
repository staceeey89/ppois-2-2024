from typing import List
from Railway import Railway
from Station import Station
from Person import Person


class Train:
    def __init__(self, number: int):
        self.number: int = number
        self.locomotive = self.Locomotive()
        self.wagons: List[Wagon] = []
        self.railway: Railway = None
        self.current_station_index: int = 0

    def add_wagon(self, wagon) -> None:
        if wagon.wagon_connected:
            print(f"Wagon {wagon.number} has already been connected")
        elif wagon.number in [w.number for w in self.wagons]:
            print(f"Wagon with number {wagon.number} is already attached to the train.")
        else:
            self.wagons.append(wagon)
            wagon.train = self
            wagon.wagon_connected = True
            print(f"Wagon {wagon.number} was connected")

    def remove_wagon(self, wagon) -> None:
        if wagon in self.wagons:
            self.wagons.remove(wagon)
            wagon.wagon_connected = False
            print(f"Wagon {wagon.number} was disconnected")
        else:
            print("This wagon is not connected")

    def choise_railway(self, railway: Railway) -> None:
        if not railway.stations:
            print("There are no stations on this railway")
        elif self.railway is not None:
            print("The railway has already been chosen")
        else:
            self.railway = railway
            railway.stations[0].trains.append(self)
            self.current_station_index = 0
            print(f"Railway {railway.number} is selected, the train is at station {railway.stations[0].name}")

    def move_forward(self) -> None:
        if self.locomotive.engine_running == False:
            print("The engine is not running.")
            return
        if self.railway is None:
            print("No railway selected for the train.")
            return

        current_station = self.railway.stations[self.current_station_index]
        self.current_station_index += 1
        if self.current_station_index >= len(self.railway.stations):
            print("Train reached the end of the railway.")
            print("The train departs to the first station.")
            self.current_station_index -= 1
            current_station.trains.remove(self)
            self.current_station_index = 0
            next_station = self.railway.stations[0]
            next_station.trains.append(self)
            return

        current_station.trains.remove(self)
        next_station = self.railway.stations[self.current_station_index]
        next_station.trains.append(self)
        print(f"Train moved from {current_station.name} to {next_station.name}")

    def board_person(self, person: Person, number_of_wagon: int) -> bool:
        if person.ticket is None:
            print(f"{person.name} does not have a ticket. Cannot board the train.")
            return False

        if not self.railway:
            print("No railway selected for the train. Cannot board the train.")
            return False

        current_station = self.railway.stations[self.current_station_index]
        if person.station != current_station:
            print(f"{person.name} is not at the current station. Cannot board the train.")
            return False

        for wagon in self.wagons:
            if wagon.number == number_of_wagon:
                wagon.persons.append(person)
                person.train = self
                person.station = None
                person.ticket = None
                self.railway.stations[self.current_station_index].persons.remove(person)
                print(f"{person.name} boarded the train.")
                return True
        print("There is no such wagon")

    def board_all_persons(self, number_of_wagon: int) -> None:
        persons = self.railway.stations[self.current_station_index].persons[:]
        for person in persons:
            self.board_person(person, number_of_wagon)

    def leave_person(self, person: Person) -> bool:
        if person.train != self:
            print(f"{person.name} is not on this train. Cannot alight from the train.")
            return False

        for wagon in self.wagons:
            if person in wagon.persons:
                person.train = None
                current_station = self.railway.stations[self.current_station_index]
                current_station.persons.append(person)
                person.station = current_station
                wagon.persons.remove(person)
                print(f"{person.name} leaved from the train at {current_station.name}.")
                return True

    def leave_all_persons(self) -> None:
        persons = []
        for wagon in self.wagons:
            persons.extend(wagon.persons)
        for person in persons:
            self.leave_person(person)

    @staticmethod
    def transportation_services() -> None:
        print("Maintenance is being carried out...")

    class Locomotive:
        def __init__(self):
            self.engine_running = False

        def start_engine(self) -> None:
            self.engine_running = True
            print("Engine started")

        def stop_engine(self) -> None:
            self.engine_running = False
            print("Engine stopped")


class Wagon:
    def __init__(self, number: int):
        self.number: int = number
        self.train = None
        self.wagon_connected: bool = False
        self.persons: List[Person] = []

    def provide_security(self) -> None:
        print(f"Security is provided at wagon {self.number}...")
