from accessify import private
from exceptions import BookingException, VisitorNotFoundException
from reception import Reception
from entities import HotelRoom, Visitor, Booking, Service, Worker
from enums import RoomStatus, RoomType, WorkerStatus, ServiceType, Dishes
from datetime import datetime, timedelta


class Hotel:

    __PAYMENT_PER_DAY = 100

    def __init__(self):
        self.__reception = Reception()
        self.__workers: list[Worker] = []

    def add_worker(self, name: str, age: int, passport_id: str) -> bool:
        for worker in self.__workers:
            if worker.passport_id == passport_id:
                return False
        worker = Worker(name, age, passport_id, WorkerStatus.resting)
        self.__workers.append(worker)
        return True

    def fire_off_worker(self, worker_passport_id: str) -> bool:
        for worker in self.__workers:
            if worker_passport_id == worker.passport_id and worker.status is WorkerStatus.resting:
                self.__workers.remove(worker)
                return True
        print(f"Worker with passport id: {worker_passport_id} is busy or doesn't exist ")
        return False

    def show_unemployed_workers(self):
        for worker in self.__workers:
            if worker.status == WorkerStatus.resting:
                print(worker)

    def show_all_workers(self):
        for worker in self.__workers:
            print(worker)

    def add_room(self, room_number: str, type_of_room: str) -> bool:
        try:
            type_of_room = RoomType[type_of_room]
            room = HotelRoom(room_number, type_of_room, RoomStatus.empty)
            return self.__reception.add_room(room)
        except KeyError:
            print("No such type of room")
            return False

    def show_available_rooms(self):
        rooms: list[HotelRoom] = self.__reception.find_available_rooms()
        print("Available rooms: ")
        for room in rooms:
            print(room, "\n")

    def show_all_rooms(self):
        for room in self.__reception.rooms:
            print(room, "\n")

    def book_room(self, name: str, age: int, passport_id: str, room_number: str, number_of_days: int) -> bool:
        visitor: Visitor = self.registrate_visitor(name, age, passport_id)
        start_date = datetime.now().replace(hour=12, minute=0, second=0, microsecond=0)
        finish_date = start_date + timedelta(days=number_of_days)
        finish_date = finish_date.replace(hour=12, minute=0, second=0, microsecond=0)
        try:
            book: Booking = self.__reception.book(visitor.passport_id, room_number, start_date, finish_date)
            print(book)
            return True
        except BookingException as e:
            print(e)
            return False
        except VisitorNotFoundException as e:
            print(e)
            return False

    def pay_off(self, visitor_passport_id: str) -> bool:
        try:
            booking: Booking = self.__reception.finish_booking(visitor_passport_id)
            days: int = (booking.finish_date - booking.start_date).days
            print(f"""Payment for {days} days is {days * Hotel.__PAYMENT_PER_DAY * booking.room.type.value[1]}""")
            return True
        except BookingException as e:
            print(e)
            return False
        except VisitorNotFoundException as e:
            print(e)
            return False

    def show_uncompleted_services(self):
        services: list[Service] = self.__reception.services
        for service in services:
            print(service)

    def ask_for_service(self, worker_passport_id: str, visitor_passport_id: str, service_type: str) -> bool:
        if service_type == 'restaurant':
            print("You should ask for a restaurant service")
            return False
        try:
            for worker in self.__workers:
                if worker.passport_id == worker_passport_id and worker.status is WorkerStatus.resting:
                    type_of_service: ServiceType = ServiceType[service_type]
                    self.__reception.ask_for_service(visitor_passport_id, type_of_service, worker)
                    return True
            print(f"Worker with passport id '{worker_passport_id}' is busy or doesn't exist")
            return False
        except KeyError:
            print("Invalid type of service")
        except VisitorNotFoundException as e:
            print(e)
            return False

    def ask_for_restaurant_service(self, worker_passport_id: str,
                                   visitor_passport_id: str, dishes: list[Dishes]) -> bool:
        try:
            for worker in self.__workers:
                if worker.passport_id == worker_passport_id and worker.status is WorkerStatus.resting:
                    self.__reception.ask_for_restaurant_service(visitor_passport_id, worker, dishes)
                    return True
            print(f"Worker with passport id '{worker_passport_id}' is busy or doesn't exist")
            return False
        except VisitorNotFoundException as e:
            print(e)
            return False

    def finish_service(self, worker_passport_id: str) -> bool:
        service = self.__reception.finish_service(worker_passport_id)
        if service:
            service.worker.status = WorkerStatus.resting
            print("Finished service: ", service, sep="\n")
            return True
        else:
            print("No service found")
            return False

    def show_all_visitors(self):
        for visitor in self.__reception.visitors:
            print(visitor, "\n")

    def show_all_bookings(self):
        for booking in self.__reception.bookings:
            print(booking, "\n")

    @private
    def registrate_visitor(self, name: str, age: int, passport_id: str) -> Visitor:
        visitor = Visitor(name, age, passport_id)
        if not self.__reception.registrate_visitor(visitor):
            self.__reception.find_visitor(visitor.passport_id)
        return visitor
