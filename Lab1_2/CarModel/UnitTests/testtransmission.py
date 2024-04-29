import unittest
import sys
from io import StringIO
from typegearsseason import TransmissionType, Gears
from carxceptions import SwitchAutomaticTransmissionError
from transmission import Transmission

class TestTransmission(unittest.TestCase):

    def setUp(self):
        self.transmission = Transmission(TransmissionType.mechanical, "Jatco", 2024)

    def test_initialization(self):

        self.assertEqual(self.transmission.get_creation_year(), 2024)
        self.assertEqual(self.transmission.get_vendor(), "Jatco")
        self.assertEqual(self.transmission.get_type(), TransmissionType.mechanical)
        self.assertEqual(self.transmission.get_gear(), Gears.N)

    def test_set_gear(self):

        self.transmission.set_gear(Gears.G1)
        self.assertEqual(self.transmission.get_gear(), Gears.G1)

    def test_str(self):

        expected_str = "{'Vendor': 'Jatco', 'Creation year': 2024, 'State': 10," + \
                       " 'Type': 'mechanical', 'Current gear': <Gears.G1: 2>}"
        
        self.transmission.set_gear(Gears.G1)
        self.assertEqual(str(self.transmission), expected_str)

    def test_invalid_set_gear(self):

        output = StringIO()
        sys.stdout = output

        self.transmission.set_gear("InvalidGear")

        sys.stdout = sys.__stdout__
        error = "ERROR! This gear is not exist\n"
        self.assertEqual(error, output.getvalue())

    def test_automatic_transmission_gear_switch(self):

        automatic_transmission = Transmission(TransmissionType.automatic, "AVendor", 2024)
        output = StringIO()
        sys.stdout = output
        
        automatic_transmission.set_gear(Gears.G1)

        sys.stdout = sys.__stdout__
        error = "You dont need switch gear, because your transmission is automatic\n"
        self.assertEqual(error, output.getvalue())

if __name__ == '__main__':
    unittest.main()