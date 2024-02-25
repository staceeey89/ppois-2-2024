import unittest
from Ticket import Ticket
from Person import Person
from Turnstile import Turnstile
from Station import Station
from Train import Train
from Schedule import Schedule


class TestPerson(unittest.TestCase):
    def setUp(self):
        self.ticket = Ticket(10)
        self.person_with_ticket = Person("Alice", 20)
        self.person_without_ticket = Person("Bob", 5)
        self.platform = Station(Station.StationName.STATION_A.value).platform
        self.turnstile = Turnstile()

    def test_buy_ticket_with_enough_money(self):
        self.assertIsNone(self.person_with_ticket.ticket)
        self.assertEqual(self.person_with_ticket.money, 20)
        self.person_with_ticket.buy_ticket(self.ticket)
        self.assertEqual(self.person_with_ticket.ticket, self.ticket)
        self.assertEqual(self.person_with_ticket.money, 10)

    def test_buy_ticket_with_not_enough_money(self):
        self.assertIsNone(self.person_without_ticket.ticket)
        self.assertEqual(self.person_without_ticket.money, 5)
        self.person_without_ticket.buy_ticket(self.ticket)
        self.assertIsNone(self.person_without_ticket.ticket)
        self.assertEqual(self.person_without_ticket.money, 5)

    def test_enter_platform_with_ticket(self):
        self.assertIsNone(self.person_with_ticket.platform)
        self.person_with_ticket.buy_ticket(self.ticket)
        self.person_with_ticket.enter_platform(self.platform, self.turnstile)
        self.assertEqual(self.person_with_ticket.platform, self.platform)

    def test_enter_platform_without_ticket(self):
        self.assertIsNone(self.person_without_ticket.platform)
        self.person_without_ticket.enter_platform(self.platform, self.turnstile)
        self.assertIsNone(self.person_without_ticket.platform)


class TestSchedule(unittest.TestCase):
    def setUp(self):
        self.station_a = Station("Station A")
        self.station_b = Station("Station B")
        self.station_c = Station("Station C")
        self.station_service = Station("Service Station")
        self.schedule = Schedule()

    def test_add_station(self):
        self.assertEqual(len(self.schedule.stations), 0)
        self.schedule.add_station(self.station_a)
        self.assertEqual(len(self.schedule.stations), 1)
        self.assertIn(self.station_a, self.schedule.stations)

    def test_remove_station(self):
        self.schedule.add_station(self.station_a)
        self.schedule.add_station(self.station_b)
        self.assertEqual(len(self.schedule.stations), 2)
        self.schedule.remove_station(self.station_a)
        self.assertEqual(len(self.schedule.stations), 1)
        self.assertNotIn(self.station_a, self.schedule.stations)

    def test_add_train(self):
        self.assertEqual(len(self.schedule.trains), 0)
        train = Train("001", self.station_service)
        self.schedule.add_train(train)
        self.assertEqual(len(self.schedule.trains), 1)
        self.assertIn(train, self.schedule.trains)

    def test_remove_train(self):
        train1 = Train("001", self.station_service)
        train2 = Train("002", self.station_service)
        self.schedule.add_train(train1)
        self.schedule.add_train(train2)
        self.assertEqual(len(self.schedule.trains), 2)
        self.schedule.remove_train(train1)
        self.assertEqual(len(self.schedule.trains), 1)
        self.assertNotIn(train1, self.schedule.trains)


class TestTrain(unittest.TestCase):
    def setUp(self):
        self.station = Station("Test Station")
        self.train = Train("001", self.station)
        self.person1 = Person("Alice", 50.0)
        self.person2 = Person("Bob", 30.0)
        self.person3 = Person("Charlie", 40.0)

    def test_load_passenger(self):
        self.assertEqual(len(self.train.persons), 0)
        self.station.platform.increase_people_count(self.person1)
        self.station.platform.increase_people_count(self.person2)
        passengers = [self.person1, self.person2]
        self.train.load_passenger(passengers)
        self.assertEqual(len(self.train.persons), 2)
        self.assertNotIn(self.person1, self.station.platform.persons)
        self.assertNotIn(self.person2, self.station.platform.persons)

    def test_unload_passenger(self):
        self.station.platform.increase_people_count(self.person1)
        self.station.platform.increase_people_count(self.person2)
        passengers = [self.person1, self.person2]
        self.train.load_passenger(passengers)
        self.assertEqual(len(self.station.platform.persons), 0)
        self.train.unload_passenger()
        self.assertEqual(len(self.train.persons), 0)
        self.assertIn(self.person1, self.station.platform.persons)
        self.assertIn(self.person2, self.station.platform.persons)


if __name__ == '__main__':
    unittest.main()
