import unittest
from car import Car
from engine import Engine
from wheels import Wheels
from transmission import Transmission
from typegearsseason import TransmissionType, Season
from brakes import Brakes


class TestCar(unittest.TestCase):

    def setUp(self):
        
        self.engine = Engine(90, "MAN Diesel", 2018)
        self.wheels = Wheels(Season.summer, "Michelin", 2020)
        self.transmission = Transmission(TransmissionType.automatic, "Eaton")
        self.brakes = Brakes("ATE", 2018)

        self.car = Car(self.engine, self.wheels, self.transmission, 
                       self.brakes, "Audi R8" , 2006)

    def test_initial_state(self):

        self.assertEqual(self.car.get_name(), "Audi R8")
        self.assertEqual(self.car.get_creation_year(), 2006)
        self.assertEqual(self.car.get_engine(), self.engine)
        self.assertEqual(self.car.get_wheels(), self.wheels)
        self.assertEqual(self.car.get_transmission(), self.transmission)
        self.assertEqual(self.car.get_brakes(), self.brakes)

        self.assertDictEqual(self.car.light_indicators, 
                             {"Fuel": 0, "max Fuel": 90,
                              "Oil": False,
                              "Engine": True, "Wheels": True,
                              "Transmission": True, 
                              "Gear": None,
                              "Brakes": True, "Turn on": False, 
                              "Mileage": 180000})

if __name__ == '__main__':
    unittest.main()