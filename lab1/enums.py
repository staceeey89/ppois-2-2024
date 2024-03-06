from enum import Enum


class BookStatus(Enum):
    renting = "renting"
    finished = "finished"


class RoomStatus(Enum):
    empty = "empty"
    occupied = "occupied"


class RoomType(Enum):
    economy = ("economy", 1)
    standard = ("standard", 2)
    luxury = ("luxury", 3)


class ServiceType(Enum):
    spa = "spa"
    massage = "massage"
    restaurant = "restaurant"


class WorkerStatus(Enum):
    resting = "resting"
    working = "working"


class Dishes(Enum):
    fish = "fish"
    meat = "meat"
    vegetables = "vegetables"

    def __repr__(self):
        return self.value
