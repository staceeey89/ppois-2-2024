from datetime import datetime
from accessify import private
from enums import RoomStatus, ServiceType, BookStatus, WorkerStatus, Dishes
from entities import HotelRoom, Visitor, Service, RestaurantService, Booking, Worker
from exceptions import VisitorNotFoundException, BookingException


class Reception:
    def __init__(self):
        self.__visitors: list[Visitor] = []
        self.__bookings: list[Booking] = []
        self.__services: list[Service] = []
        self.__rooms: list[HotelRoom] = []

    def book(self, visitor_passport_id, room_number: str, start_date: datetime, finish_date: datetime) -> Booking:
        visitor = self.find_visitor(visitor_passport_id)
        if not visitor:
            raise VisitorNotFoundException(visitor_passport_id)
        room = self.find_room(room_number)
        if not room:
            self.__visitors.remove(visitor)
            raise BookingException("No such room")
        if room not in self.find_available_rooms():
            self.__visitors.remove(visitor)
            raise BookingException("Room is not available now")
        room.status = RoomStatus.occupied
        booking = Booking(visitor, room, start_date, finish_date, BookStatus.renting)
        self.__bookings.append(booking)
        return booking

    def finish_booking(self, visitor_passport_id: str) -> Booking:
        visitor = self.find_visitor(visitor_passport_id)
        if not visitor:
            raise VisitorNotFoundException(visitor_passport_id)
        booking = self.find_booking_by_visitor_passport_id(visitor_passport_id)
        if not booking:
            raise BookingException("Booking not found")
        booking.room.status = RoomStatus.empty
        booking.status = BookStatus.finished
        self.__visitors.remove(visitor)
        self.__bookings.remove(booking)
        return booking

    def ask_for_service(self, visitor_passport_id: str, service_type: ServiceType, worker: Worker):
        visitor = self.find_visitor(visitor_passport_id)
        if not visitor:
            raise VisitorNotFoundException(visitor_passport_id)
        self.__services.append(Service(visitor, service_type, worker))
        worker.status = WorkerStatus.working

    def ask_for_restaurant_service(self, visitor_passport_id: str, worker: Worker, dishes: list[Dishes]):
        visitor = self.find_visitor(visitor_passport_id)
        if not visitor:
            raise VisitorNotFoundException(visitor_passport_id)
        self.__services.append(RestaurantService(visitor, ServiceType.restaurant, worker, dishes))
        worker.status = WorkerStatus.working

    def finish_service(self, worker_passport_id) -> Service | None:
        for service in self.__services:
            if service.worker.passport_id == worker_passport_id:
                self.__services.remove(service)
                return service
        return None

    def find_available_rooms(self) -> list[HotelRoom]:
        rooms: list[HotelRoom] = []
        for room in self.__rooms:
            if room.status == RoomStatus.empty:
                rooms.append(room)
        return rooms

    def registrate_visitor(self, visitor: Visitor) -> bool:
        if visitor not in self.__visitors:
            self.__visitors.append(visitor)
            return True
        return False

    def add_room(self, room: HotelRoom) -> bool:
        if room not in self.__rooms:
            self.__rooms.append(room)
            return True
        return False

    def find_visitor(self, visitor_passport_id: str) -> Visitor | None:
        for visitor in self.__visitors:
            if visitor.passport_id == visitor_passport_id:
                return visitor
        return None

    @property
    def rooms(self) -> list[HotelRoom]:
        return self.__rooms

    @property
    def services(self) -> list[Service]:
        return self.__services

    @property
    def bookings(self) -> list[Booking]:
        return self.__bookings

    @property
    def visitors(self) -> list[Visitor]:
        return self.__visitors

    @private
    def find_room(self, room_number: str) -> HotelRoom | None:
        for room in self.__rooms:
            if room.number == room_number:
                return room
        return None

    @private
    def find_booking_by_visitor_passport_id(self, visitor_passport_id: str) -> Booking | None:
        for booking in self.__bookings:
            if booking.visitor.passport_id == visitor_passport_id:
                return booking
        return None
