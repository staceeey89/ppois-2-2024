import unittest
from hotel import *
from enums import BookStatus


class TestHotel(unittest.TestCase):
    def test_add_room(self):
        hotel = Hotel()
        self.assertTrue(hotel.add_room("101", RoomType.economy.value[0]))
        self.assertFalse(hotel.add_room("101", RoomType.economy.value[0]))
        self.assertFalse(hotel.add_room("102", "NoSuchType"))

    def test_get_available_rooms(self):
        reception = Reception()
        room1 = HotelRoom("101", RoomType.economy, RoomStatus.empty)
        room2 = HotelRoom("201", RoomType.standard, RoomStatus.occupied)
        test_rooms: list[HotelRoom] = [room1]
        reception.add_room(room1)
        reception.add_room(room2)
        self.assertEqual(test_rooms, reception.find_available_rooms())
        test_rooms.append(room2)
        self.assertNotEqual(test_rooms, reception.find_available_rooms())

    def test_get_all_rooms(self):
        reception = Reception()
        room1 = HotelRoom("101", RoomType.economy, RoomStatus.empty)
        room2 = HotelRoom("201", RoomType.standard, RoomStatus.occupied)
        test_rooms: list[HotelRoom] = [room1, room2]
        reception.add_room(room1)
        reception.add_room(room2)
        self.assertNotEqual(test_rooms, reception.find_available_rooms())
        self.assertEqual(test_rooms, reception.rooms)

    def test_add_worker(self):
        hotel = Hotel()
        self.assertTrue(hotel.add_worker("Ivan Ivanov", 32, "IvanIvanov32id"))
        self.assertFalse(hotel.add_worker("Ivan Ivanov", 32, "IvanIvanov32id"))

    def test_fire_off_worker(self):
        hotel = Hotel()
        hotel.add_worker("Ivan Ivanov", 32, "IvanIvanov32id")
        self.assertTrue(hotel.fire_off_worker("IvanIvanov32id"))
        self.assertFalse(hotel.fire_off_worker("IvanIvanov32id"))

    def test_book_room(self):
        hotel = Hotel()
        hotel.add_room("101", RoomType.economy.value[0])
        hotel.add_room("102", RoomType.economy.value[0])
        self.assertTrue(hotel.book_room("Petr Petrov", 25,
                                        "PetrPetrov25id", "101", 3))
        self.assertTrue(hotel.book_room("Petr Petrov", 25,
                                        "PetrPetrov25id", "102", 3))
        self.assertFalse(hotel.book_room("Petr Petrov", 25,
                                         "PetrPetrov25id", "101", 3))
        self.assertFalse(hotel.book_room("Ivan Ivanov", 32,
                                         "IvanIvanov32id", "101", 3))

    def test_pay_off(self):
        hotel = Hotel()
        hotel.add_room("101", RoomType.economy.value[0])
        hotel.book_room("Petr Petrov", 25, "PetrPetrov25id", "101", 3)
        self.assertTrue(hotel.pay_off("PetrPetrov25id"))
        self.assertFalse(hotel.pay_off("PetrPetrov25id"))
        self.assertFalse(hotel.pay_off("NoSuchPassportId"))

    def test_ask_for_service(self):
        hotel = Hotel()
        hotel.add_room("101", RoomType.economy.value[0])
        hotel.add_worker("Ivan Ivanov", 32, "IvanIvanov32id")
        hotel.book_room("Petr Petrov", 25, "PetrPetrov25id", "101", 3)
        self.assertFalse(hotel.ask_for_service("NoSuchPassportId",
                                               "PetrPetrov25id", ServiceType.massage.value))
        self.assertFalse(hotel.ask_for_service("IvanIvanov32id",
                                               "NoSuchId", ServiceType.massage.value))
        self.assertTrue(hotel.ask_for_service("IvanIvanov32id",
                                              "PetrPetrov25id", ServiceType.massage.value))

    def test_ask_for_restaurant_service(self):
        hotel = Hotel()
        hotel.add_room("101", RoomType.economy.value[0])
        hotel.add_worker("Ivan Ivanov", 32, "IvanIvanov32id")
        hotel.book_room("Petr Petrov", 25, "PetrPetrov25id", "101", 3)
        dishes: list[Dishes] = [Dishes.fish, Dishes.meat]
        self.assertTrue(hotel.ask_for_restaurant_service("IvanIvanov32id",
                                                         "PetrPetrov25id", dishes))
        self.assertFalse(hotel.ask_for_restaurant_service("IvanIvanov32id",
                                                          "PetrPetrov25id", dishes))
        self.assertFalse(hotel.ask_for_restaurant_service("NoSuchId",
                                                          "PetrPetrov25id", dishes))
        self.assertFalse(hotel.ask_for_restaurant_service("IvanIvanov32id",
                                                          "NoSuchId", dishes))

    def test_finish_service(self):
        hotel = Hotel()
        hotel.add_room("101", RoomType.economy.value[0])
        hotel.add_worker("Ivan Ivanov", 32, "IvanIvanov32id")
        hotel.book_room("Petr Petrov", 25, "PetrPetrov25id", "101", 3)
        hotel.ask_for_service("IvanIvanov32id",
                              "PetrPetrov25id", ServiceType.massage.value)
        self.assertTrue(hotel.finish_service("IvanIvanov32id"))
        self.assertFalse(hotel.finish_service("NoSuchWorkerPassportId"))

    def test_get_all_visitors(self):
        reception = Reception()
        visitor = Visitor("Petr Petrov", 25, "PetrPetrov25id")
        self.assertTrue(reception.registrate_visitor(visitor))
        visitors: list[Visitor] = [visitor]
        self.assertFalse(reception.registrate_visitor(visitor))
        self.assertEqual(visitors, reception.visitors)

    def test_get_all_bookings(self):
        reception = Reception()
        visitor = Visitor("Petr Petrov", 25, "PetrPetrov25id")
        visitors: list[Visitor] = [visitor]
        reception.registrate_visitor(visitor)
        room1 = HotelRoom("101", RoomType.economy, RoomStatus.empty)
        room2 = HotelRoom("201", RoomType.standard, RoomStatus.empty)
        reception.add_room(room1)
        reception.add_room(room2)
        start_date: datetime = datetime.now().replace(hour=12, minute=0, second=0, microsecond=0)
        finish_date: datetime = (datetime.now() + timedelta(days=3)).replace(hour=12, minute=0, second=0, microsecond=0)
        reception.book("PetrPetrov25id", "101", start_date, finish_date)
        reception.book("PetrPetrov25id", "201", start_date, finish_date)
        booking1 = Booking(visitor, room1, start_date, finish_date, BookStatus.renting)
        booking2 = Booking(visitor, room2, start_date, finish_date, BookStatus.renting)
        bookings: list[Booking] = [booking1, booking2]
        self.assertEqual(visitors, reception.visitors)
        self.assertEqual(bookings, reception.bookings)
