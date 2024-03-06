import datetime
from enums import RoomStatus, RoomType, ServiceType, BookStatus, WorkerStatus, Dishes


class Person:
    def __init__(self, name: str, age: int, passport_id: str):
        self.__name = name
        self.__age = age
        self.__passport_id = passport_id

    @property
    def name(self) -> str:
        return self.__name

    @property
    def age(self) -> int:
        return self.__age

    @property
    def passport_id(self) -> str:
        return self.__passport_id


class HotelRoom:
    def __init__(self, number: str, type_of_room: RoomType, status: RoomStatus):
        self.__number = number
        self.__type_of_room = type_of_room
        self.__status = status

    @property
    def number(self) -> str:
        return self.__number

    @property
    def type(self) -> RoomType:
        return self.__type_of_room

    @property
    def status(self) -> RoomStatus:
        return self.__status

    @status.setter
    def status(self, status: RoomStatus):
        self.__status = status

    def __str__(self) -> str:
        return f"""Room #{self.__number}\nType: {self.__type_of_room.value[0]}\nStatus: {self.__status.value}"""

    def __eq__(self, other) -> bool:
        return self.__number == other.number


class Visitor(Person):
    def __init__(self, name: str, age: int, passport_id: str):
        super().__init__(name, age, passport_id)

    @property
    def name(self) -> str:
        return super().name

    @property
    def age(self) -> int:
        return super().age

    @property
    def passport_id(self) -> str:
        return super().passport_id

    def __eq__(self, other) -> bool:
        return self.passport_id == other.passport_id

    def __str__(self) -> str:
        return f"Visitor: {super().name}\nAge: {super().age}\nPassport id: {super().passport_id}\n"


class Worker(Person):
    def __init__(self, name: str, age: int, passport_id: str, status: WorkerStatus):
        super().__init__(name, age, passport_id)
        self.__status = status

    @property
    def name(self) -> str:
        return super().name

    @property
    def age(self) -> int:
        return super().age

    @property
    def passport_id(self) -> str:
        return super().passport_id

    @property
    def status(self) -> WorkerStatus:
        return self.__status

    @status.setter
    def status(self, status: WorkerStatus):
        self.__status = status

    def __str__(self) -> str:
        return (f"Worker: {super().name}\nAge: {super().age}\nPassport id: {super().passport_id}\n"
                f"Status: {self.__status.value}\n")


class Booking:
    def __init__(self, visitor: Visitor, room: HotelRoom,
                 start_date: datetime, finish_date: datetime, status: BookStatus):
        self.__visitor = visitor
        self.__room = room
        self.__start_date = start_date
        self.__finish_date = finish_date
        self.__status = status

    @property
    def visitor(self) -> Visitor:
        return self.__visitor

    @property
    def room(self) -> HotelRoom:
        return self.__room

    @property
    def start_date(self) -> datetime:
        return self.__start_date

    @property
    def finish_date(self) -> datetime:
        return self.__finish_date

    @property
    def status(self) -> BookStatus:
        return self.__status

    @status.setter
    def status(self, status: BookStatus):
        self.__status = status

    def __eq__(self, other):
        return self.visitor == other.visitor and self.room == other.room and self.start_date == other.start_date and \
            self.finish_date == other.finish_date and self.status == other.status

    def __str__(self):
        return (f"Room#{self.room.number} is booked\n"
                f"From: {self.__start_date.strftime('%d/%m/%Y %H:%M')}\n"
                f"Before: {self.__finish_date.strftime('%d/%m/%Y %H:%M')}\n")


class Service:
    def __init__(self, visitor: Visitor, service_type: ServiceType, worker: Worker):
        self.__visitor = visitor
        self.__type = service_type
        self.__worker = worker

    @property
    def visitor(self) -> Visitor:
        return self.__visitor

    @property
    def type(self) -> ServiceType:
        return self.__type

    @property
    def worker(self) -> Worker:
        return self.__worker

    def __str__(self):
        return f"{self.__type.value} for {self.__visitor.name} by {self.__worker.name}"

    def __eq__(self, other) -> bool:
        return self.__visitor == other.__visitor and self.__type == other.__type and self.__worker == other.__worker


class RestaurantService(Service):
    def __init__(self, visitor: Visitor, service_type: ServiceType, worker: Worker, dishes: list[Dishes]):
        super().__init__(visitor, service_type, worker)
        self.__dishes: list[Dishes] = dishes

    def __str__(self) -> str:
        return (f"Restaurant service for {super().visitor.name}\n"
                f"Dishes: {self.__dishes}\n")
