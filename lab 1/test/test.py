import unittest
from Person import Person
from Railway import Railway
from Schedule import ScheduleItem
from Schedule import Schedule
from Station import Station
from Ticket import Ticket
from Train import Train
from Train import Wagon
from datetime import datetime


class TestPerson(unittest.TestCase):
    def test_buy_ticket(self):
        ticket = Ticket(75)
        person = Person("John", 100)
        person.buy_ticket(ticket)

        self.assertEqual(person.ticket, ticket)
        self.assertTrue(ticket.purchased)
        self.assertEqual(person.balance, 25)

    def test_buy_ticket_insufficient_balance(self):
        ticket = Ticket(75)
        person = Person("John", 50)
        person.buy_ticket(ticket)

        self.assertIsNone(person.ticket)
        self.assertFalse(ticket.purchased)
        self.assertEqual(person.balance, 50)

    def test_buy_ticket_already_has_ticket(self):
        ticket1 = Ticket(75)
        ticket2 = Ticket(100)
        person = Person("John", 200)
        person.buy_ticket(ticket1)
        person.buy_ticket(ticket2)

        self.assertEqual(person.ticket, ticket1)
        self.assertFalse(ticket2.purchased)
        self.assertEqual(person.balance, 125)

    def test_select_station(self):
        person = Person("John", 100)
        station = Station("Station A")
        person.select_station(station)

        self.assertEqual(person.station, station)
        self.assertIn(person, station.persons)


class RailwayTest(unittest.TestCase):
    def test_add_station(self):
        station1 = Station("Station A")
        station2 = Station("Station B")
        railway = Railway(1)

        railway.add_station(station1)
        self.assertIn(station1, railway.stations)

        railway.add_station(station2)
        self.assertIn(station2, railway.stations)

        railway.add_station(station1)
        self.assertNotEqual(railway.stations.count(station1), 2)

    def test_remove_station(self):
        station1 = Station("Station A")
        station2 = Station("Station B")
        railway = Railway(1)

        railway.add_station(station1)
        railway.add_station(station2)

        railway.remove_station(station1)
        self.assertNotIn(station1, railway.stations)

        railway.remove_station(station2)
        self.assertNotIn(station2, railway.stations)

    def test_remove_station_not_in_railway(self):
        station = Station("Station A")
        railway = Railway(1)

        with self.assertRaises(ValueError):
            railway.remove_station(station)


class ScheduleTest(unittest.TestCase):
    def setUp(self):
        self.train1 = Train(1)
        self.train2 = Train(2)
        self.station1 = Station("Station A")
        self.station2 = Station("Station B")
        self.arrival_time1 = datetime(2024, 3, 25, 10, 0)
        self.arrival_time2 = datetime(2024, 3, 25, 12, 0)

    def test_add_item(self):
        schedule = Schedule()
        item1 = ScheduleItem(self.train1, self.station1, self.arrival_time1)
        item2 = ScheduleItem(self.train2, self.station2, self.arrival_time2)

        schedule.add_item(item1)
        self.assertIn(item1, schedule.items)

        schedule.add_item(item2)
        self.assertIn(item2, schedule.items)

    def test_remove_item(self):
        schedule = Schedule()
        item1 = ScheduleItem(self.train1, self.station1, self.arrival_time1)
        item2 = ScheduleItem(self.train2, self.station2, self.arrival_time2)

        schedule.add_item(item1)
        schedule.add_item(item2)

        schedule.remove_item(item1)
        self.assertNotIn(item1, schedule.items)

        schedule.remove_item(item2)
        self.assertNotIn(item2, schedule.items)


class TrainTest(unittest.TestCase):
    def setUp(self):
        self.train = Train(1)
        self.wagon1 = Wagon(1)
        self.wagon2 = Wagon(2)
        self.wagon3 = Wagon(1)
        self.railway = Railway(1)
        self.station1 = Station("Station A")
        self.station2 = Station("Station B")
        self.railway.add_station(self.station1)
        self.railway.add_station(self.station2)
        self.person = Person("John", 500)
        self.person.select_station(self.station1)
        self.person2 = Person("Bob", 500)
        self.person2.select_station(self.station2)
        self.person3 = Person("Emi", 100)
        self.person3.select_station(self.station1)

    def test_add_wagon(self):
        self.train.add_wagon(self.wagon1)
        self.assertIn(self.wagon1, self.train.wagons)

    def test_add_wagon_already_connected(self):
        self.wagon1.wagon_connected = True
        self.train.add_wagon(self.wagon1)
        self.assertNotEqual(self.train.wagons.count(self.wagon1), 2)

    def test_add_wagons_with_same_number(self):
        self.train.add_wagon(self.wagon1)
        self.train.add_wagon(self.wagon3)
        self.assertNotIn(self.wagon3, self.train.wagons)

    def test_remove_wagon(self):
        self.train.add_wagon(self.wagon1)
        self.train.remove_wagon(self.wagon1)
        self.train.remove_wagon(self.wagon1)
        self.assertNotIn(self.wagon1, self.train.wagons)

    def test_choise_railway(self):
        self.train.choise_railway(self.railway)
        self.assertEqual(self.train.railway, self.railway)
        self.assertEqual(self.train.current_station_index, 0)
        self.assertIn(self.train, self.station1.trains)

    def test_choise_railway_no_stations(self):
        railway = Railway(2)
        self.train.choise_railway(railway)
        self.assertIsNone(self.train.railway)

    def test_move_forward_engine_not_running(self):
        self.train.move_forward()
        self.assertEqual(self.train.current_station_index, 0)

    def test_move_forward_no_railway_selected(self):
        self.train.locomotive.start_engine()
        self.train.move_forward()
        self.assertEqual(self.train.current_station_index, 0)

    def test_move_forward_reached_end_of_railway(self):
        self.train.locomotive.start_engine()
        self.train.choise_railway(self.railway)
        self.train.move_forward()
        self.train.move_forward()
        self.assertIn(self.train, self.station1.trains)
        self.assertEqual(self.train.current_station_index, 0)

    def test_board_person_no_ticket(self):
        self.train.choise_railway(self.railway)
        self.train.add_wagon(self.wagon1)
        self.train.add_wagon(self.wagon2)
        self.train.board_person(self.person, 1)
        self.assertNotIn(self.person, self.wagon1.persons)

    def test_board_person_no_railway_selected(self):
        self.train.add_wagon(self.wagon1)
        self.train.add_wagon(self.wagon2)
        ticket = Ticket(10)
        self.person.buy_ticket(ticket)
        self.train.board_person(self.person, 1)
        self.assertNotIn(self.person, self.wagon1.persons)

    def test_board_person_not_at_current_station(self):
        self.train.choise_railway(self.railway)
        self.train.add_wagon(self.wagon1)
        self.train.add_wagon(self.wagon2)
        ticket = Ticket(10)
        self.person2.buy_ticket(ticket)
        self.train.board_person(self.person2, 1)
        self.assertNotIn(self.person2, self.wagon1.persons)

    def test_board_person_success(self):
        self.train.choise_railway(self.railway)
        self.train.add_wagon(self.wagon1)
        self.train.add_wagon(self.wagon2)
        ticket = Ticket(10)
        self.person.buy_ticket(ticket)
        self.train.board_person(self.person, 1)
        self.assertIn(self.person, self.wagon1.persons)
        self.assertNotIn(self.person, self.station1.persons)

    def test_board_all_persons(self):
        self.train.choise_railway(self.railway)
        self.train.add_wagon(self.wagon1)
        self.train.add_wagon(self.wagon2)
        ticket1 = Ticket(10)
        ticket2 = Ticket(10)
        self.person.buy_ticket(ticket1)
        self.person3.buy_ticket(ticket2)
        self.train.board_all_persons(1)
        self.assertIn(self.person, self.wagon1.persons)
        self.assertIn(self.person3, self.wagon1.persons)
        self.assertNotIn(self.person, self.station1.persons)
        self.assertNotIn(self.person3, self.station1.persons)

    def test_leave_person_success(self):
        self.train.choise_railway(self.railway)
        self.train.add_wagon(self.wagon1)
        self.train.add_wagon(self.wagon2)
        ticket = Ticket(10)
        self.person.buy_ticket(ticket)
        self.train.board_person(self.person, 1)
        self.assertIn(self.person, self.wagon1.persons)

        self.train.leave_person(self.person)
        self.assertNotIn(self.person, self.wagon1.persons)
        self.assertIn(self.person, self.station1.persons)

    def test_leave_all_persons(self):
        self.train.choise_railway(self.railway)
        self.train.add_wagon(self.wagon1)
        self.train.add_wagon(self.wagon2)
        ticket1 = Ticket(10)
        ticket2 = Ticket(10)
        self.person.buy_ticket(ticket1)
        self.person3.buy_ticket(ticket2)
        self.train.board_all_persons(1)
        self.assertIn(self.person, self.wagon1.persons)
        self.assertIn(self.person3, self.wagon1.persons)

        self.train.leave_all_persons()
        self.assertNotIn(self.person, self.wagon1.persons)
        self.assertNotIn(self.person3, self.wagon1.persons)
        self.assertIn(self.person, self.station1.persons)
        self.assertIn(self.person3, self.station1.persons)


if __name__ == '__main__':
    unittest.main()
