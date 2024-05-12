from typing import List
from Station import Station


class Railway:
    def __init__(self, number: int):
        self.number: int = number
        self.stations: List[Station] = []

    def add_station(self, station: Station) -> None:
        if station in self.stations:
            print(f"{station.name} is already in this railway track")
        else:
            self.stations.append(station)

    def remove_station(self, station: Station) -> None:
        self.stations.remove(station)
        print(f"Station {station.name} has been deleted")
