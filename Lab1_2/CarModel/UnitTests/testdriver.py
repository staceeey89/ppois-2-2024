import unittest
import sys
from io import StringIO
from unittest.mock import MagicMock
from engine import Engine
from wheels import Wheels
from transmission import Transmission
from brakes import Brakes
from driver import Driver
from typegearsseason import TransmissionType, Season, Gears
from car import Car


class TestDriver(unittest.TestCase):

    def setUp(self):
        
        self.engine = Engine(90, "MAN Diesel", 2018, 50, True)
        self.wheels = Wheels(Season.summer, "Michelin", 2020)
        self.transmission = Transmission(TransmissionType.mechanical, "Eaton")
        self.brakes = Brakes("ATE", 2018)

        self.car1 = Car(self.engine, self.wheels, self.transmission, self.brakes, "Audi R8" , 2006)
        
        self.car2 = MagicMock(spec=Car)
        
        self.driver = Driver("Pjotr", "Smirnof")
        self.young_driver = Driver("Nikolay", "Smirnof", 16)

    def test_invalid_set_age(self):

        output = StringIO()
        sys.stdout = output

        self.driver.set_age(-45)

        sys.stdout = sys.__stdout__
        error = "Nothing changed, because this age is invalid\n"
        self.assertEqual(error, output.getvalue())

    def test_eq(self):

        driver_copy = self.driver

        self.assertFalse(self.driver == self.young_driver)
        self.assertTrue(self.driver == driver_copy)

    def test_add_car(self):
    
        self.driver.add(self.car1)
        self.assertIn(self.car1, self.driver.get_vehicle_fleet())

    def test_del_car(self):

        self.driver.add(self.car1)
        self.driver.rem(self.car1)
        self.assertNotIn(self.car1, self.driver.get_vehicle_fleet())

    def test_choose_car(self):
        
        output = StringIO()
        sys.stdout = output

        self.driver.add(self.car2)
        self.driver.choose(self.car2)
        self.assertEqual(self.driver.get_current_car(), self.car2)

        self.young_driver.add(self.car1)
        self.young_driver.choose(self.car1)

        sys.stdout = sys.__stdout__
        error = "You are too young for this\n\n"

        self.assertEqual(error, output.getvalue())

    def test_get_car_state(self):

        self.driver.add(self.car1)
        self.driver.choose(self.car1)

        car_state = {"Fuel": 50, 
                "max Fuel": 90,
                "Oil": True,
                "Engine": True, 
                "Wheels": True,
                "Transmission": True, 
                "Gear": Gears.N,
                "Brakes": True, 
                "Turn on": False, 
                "Mileage": 180_000}

        self.assertEqual(self.driver.get_car_state(), car_state)
        
    def test_start_engine(self):

        output = StringIO()
        sys.stdout = output
        
        self.driver.add(self.car1)
        self.driver.choose(self.car1)
        self.driver.start_engine()
        self.assertTrue(self.driver.get_current_car().light_indicators["Turn on"])

        self.driver.start_engine()
        sys.stdout = sys.__stdout__
        error = "Your engine is already turning on\n\n"
        self.assertEqual(error, output.getvalue())

    def test_stop_engine(self):

        output = StringIO()
        sys.stdout = output
        
        self.driver.add(self.car1)
        self.driver.choose(self.car1)
        self.driver.stop_engine()
        sys.stdout = sys.__stdout__
        error = "Your engine is already turning off\n\n"
        self.assertEqual(error, output.getvalue())

        self.driver.start_engine()
        self.driver.stop_engine()
        self.assertFalse(self.driver.get_current_car().light_indicators["Turn on"])

    def test_drive_forward(self):

        output = StringIO()
        sys.stdout = output

        self.driver.add(self.car1)
        self.driver.choose(self.car1)
        initial_mileage = self.driver.get_current_car().light_indicators["Mileage"]
        self.driver.start_engine()

        self.driver.drive_forward()
        sys.stdout = sys.__stdout__
        error = "ERROR! Can't drive, because current gear is invalid\n\n"
        self.assertEqual(error, output.getvalue())

        self.driver.change_gear(Gears.G1)
        self.driver.drive_forward()
        final_mileage = self.driver.get_current_car().light_indicators["Mileage"]
        self.assertEqual(final_mileage, initial_mileage + 1)

    def test_drive_back(self):

        output = StringIO()
        sys.stdout = output

        self.driver.add(self.car1)
        self.driver.choose(self.car1)
        initial_mileage = self.driver.get_current_car().light_indicators["Mileage"]
        self.driver.start_engine()

        self.driver.drive_back()
        sys.stdout = sys.__stdout__
        error = "ERROR! Can't drive, because current gear is invalid\n\n"
        self.assertEqual(error, output.getvalue())

        self.driver.change_gear(Gears.R)
        self.driver.drive_back()
        final_mileage = self.driver.get_current_car().light_indicators["Mileage"]
        self.assertEqual(final_mileage, initial_mileage + 1)


    def test_drive_right(self):

        output = StringIO()
        sys.stdout = output

        self.driver.add(self.car1)
        self.driver.choose(self.car1)
        initial_mileage = self.driver.get_current_car().light_indicators["Mileage"]
        self.driver.start_engine()

        self.driver.drive_right()
        sys.stdout = sys.__stdout__
        error = "ERROR! Can't drive, because current gear is invalid\n\n"
        self.assertEqual(error, output.getvalue())

        self.driver.change_gear(Gears.G1)
        self.driver.drive_right()
        final_mileage = self.driver.get_current_car().light_indicators["Mileage"]
        self.assertEqual(final_mileage, initial_mileage + 1)

    def test_current_car_unavailable(self):
        
        output = StringIO()
        sys.stdout = output

        self.driver.start_engine()
        self.driver.change_gear(Gears.G2)
        self.driver.drive_forward()
        self.driver.drive_right()
        self.driver.change_gear(Gears.R)
        self.driver.drive_back()
        self.driver.stop_engine()
        sys.stdout = sys.__stdout__
        error = "ERROR! You are not choosing current car for operation\n\n" * 7
        self.assertEqual(error, output.getvalue())
    
    

if __name__ == '__main__':
    unittest.main()

    

