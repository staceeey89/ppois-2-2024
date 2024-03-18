import unittest
from ConferenceHall import ConferenceHall


class TestConferenceHall(unittest.TestCase):
    def setUp(self):
        self.conference_hall = ConferenceHall("Зал для тестов", 100)

    def test_set_name(self):
        self.conference_hall.set_name("Новый зал")
        self.assertEqual(self.conference_hall.get_name(), "Новый зал")


    def test_set_capacity(self):
        self.conference_hall.set_capacity(200)
        self.assertEqual(self.conference_hall.get_capacity(), 200)

        self.conference_hall.set_capacity(-100)
        assert self.conference_hall.get_capacity() != self.conference_hall.set_capacity


    def test_add_booking(self):
        self.conference_hall.add_booking("Бронирование 1")
        self.assertIn("Бронирование 1", self.conference_hall.get_bookings())

    def test_cancel_booking(self):
        self.conference_hall.add_booking("Отмена бронирования")

        self.conference_hall.cancel_booking("Отмена бронирования")
        self.assertNotIn("Отмена бронирования", self.conference_hall.get_bookings())

        self.conference_hall.cancel_booking("Несуществующее бронирование")

if __name__ == '__main__':
    unittest.main()