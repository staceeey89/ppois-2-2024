from datetime import datetime
from Train import Train
from Station import Station


class ScheduleItem:
    def __init__(self, train: Train, station: Station, arrival_time: datetime):
        self.train = train
        self.station = station
        self.arrival_time = arrival_time


class Schedule:
    def __init__(self):
        self.items = []

    def add_item(self, item: ScheduleItem) -> None:
        self.items.append(item)
        print("Schedule item added.")

    def remove_item(self, item: ScheduleItem) -> None:
        self.items.remove(item)
        print("Schedule item removed.")

    def show_schedule(self) -> None:
        if not self.items:
            print("No schedule items found.")
            return

        print("Schedule:")
        for i, item in enumerate(self.items, start=1):
            print(f"{i}. Train: {item.train.number}, Station: {item.station.name}, Arrival Time: {item.arrival_time}")
