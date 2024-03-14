import unittest
from passenger import Passenger
from station import Station
from platf import Platform
from ticket import Ticket
from turnstile import Turnstile
from train import Train
from depot import Depot


class TestPassenger(unittest.TestCase):
    def setUp(self):
        self.passenger = Passenger("ZHOPA", 50)
        self.station1 = Station(1)
        self.platform1 = Platform(0)
        self.platform2 = Platform(1)
        self.ticket = Ticket()
        self.turnstile = Turnstile()
        self.station1.ticket = self.ticket
        self.station1.turnstile = self.turnstile
        self.station1.add_platform(self.platform1)
        self.station1.add_platform(self.platform2)
        self.train_test = Train()
        self.station2 = Station(2)

        self.depot = Depot()

    def test_getters_setters(self):
        self.assertEqual(self.passenger.name, "ZHOPA")  # add assertion here
        self.assertEqual(self.passenger.cash, 50)  # add
        self.assertEqual(self.station1.number, 1)
        self.assertEqual(self.platform1.number, 0)
        self.assertEqual(self.station1.ticket, self.ticket)
        self.assertEqual(self.station1.turnstile, self.turnstile)
        self.assertEqual(self.station1.get_platforms()[0].number, self.platform1.number)
        self.station2.add_platform(self.platform2)
        self.assertEqual(self.station2.get_platforms()[0], self.platform2)
        self.station2.remove_platform(self.platform2)
        self.assertEqual(len(self.station2.get_platforms()), 0)
        self.assertEqual(self.ticket.cost, 0)
        self.ticket.cost = 30
        self.assertEqual(self.ticket.cost, 30)
        self.train_test.platform = self.platform1
        self.assertEqual(self.train_test.platform, self.platform1)

    def test_passenger_takes_train(self):
        self.passenger2 = Passenger("Name", 50)
        self.ticket2 = Ticket()
        self.ticket2.cost = 20
        self.station2.ticket = self.ticket2
        self.station2.add_platform(self.platform2)
        self.station2.add_platform(self.platform1)
        self.station2.sell_a_ticket(self.passenger2)
        self.assertEqual(self.passenger2.cash, 30)
        self.assertEqual(self.passenger2.ticket, self.ticket2)
        self.passenger2.cross_a_turnstile(self.turnstile)
        self.passenger2.choose_a_platform(self.station2.get_platforms()[0])
        self.train_test.platform = self.station2.get_platforms()[0]
        self.station2.get_platforms()[0].train = self.train_test
        self.assertEqual(self.station2.get_platforms()[0].train, self.train_test)
        self.passenger2.board(self.train_test)
        self.assertEqual(self.train_test.get_passengers()[0], self.passenger2)
        self.passenger2.disembark(self.train_test)
        self.assertEqual(len(self.train_test.get_passengers()), 0)

    def test_depot(self):
        self.depot.pull_into(self.train_test)
        self.assertEqual(self.depot.get_trains_list()[0], self.train_test)
        self.assertEqual(self.depot.pull_out_train(), self.train_test)
        self.assertEqual(len(self.depot.get_trains_list()), 0)

if __name__ == '__main__':
    unittest.main()
