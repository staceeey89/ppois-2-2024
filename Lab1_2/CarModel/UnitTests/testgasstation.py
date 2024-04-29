import unittest
from gasstation import GasStation
from car import Car
from engine import Engine
from wheels import Wheels
from transmission import Transmission
from brakes import Brakes
from typegearsseason import TransmissionType, Season

class TestGasStation(unittest.TestCase):

    def setUp(self):

        self.engine = Engine(90, "MAN Diesel", 2018, 50, True)
        self.wheels = Wheels(Season.summer, "Michelin", 2020)
        self.transmission = Transmission(TransmissionType.mechanical, "Eaton")
        self.brakes = Brakes("ATE", 2018)

        self.car1 = Car(self.engine, self.wheels, self.transmission, self.brakes, "Audi R8" , 2006)
        self.car2 = Car(self.engine, self.wheels, self.transmission, self.brakes, "BMW M4" , 2014)

    def test_add_car(self):
    
        GasStation.add(self.car1)
        self.assertIn(self.car1, GasStation.get_queue())

    def test_del_car(self):

        GasStation.add(self.car1)
        GasStation.rem(self.car1)
        self.assertNotIn(self.car1, GasStation.get_queue())

    def test_set_queue(self):

        queue = {self.car1, self.car2}
        GasStation.set_queue(queue)
        self.assertEqual(GasStation.get_queue(), queue)

    def test_fueling(self):

        queue = {self.car1, self.car2}
        GasStation.set_queue(queue)
        fueled_cars = GasStation.gen_refueling_cars()
        
        fuel_level1 = next(fueled_cars).light_indicators["Fuel"]
        fuel_level2 = next(fueled_cars).light_indicators["Fuel"]
        self.assertEqual(fuel_level1, 90)
        self.assertEqual(fuel_level2, 90)