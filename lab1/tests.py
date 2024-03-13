import unittest
from plot import Plot
from instrument import Instrument
from plant import Plant
from irrigation_system import IrrigationSystem
from recreationArea import RecreationArea
from unittest.mock import patch
from io import StringIO


class TestPlot(unittest.TestCase):
    def test_plot(self):
        a = Plot("asd", 5)
        self.assertEqual(a.square, 5)

    def test_plants_in_plot(self):
        a = Plot("plot", 6)
        plant = Plant("ромашка")
        instruments = []
        instrument = Instrument("лопата")
        instruments.append(instrument)
        with patch('builtins.input', return_value="лопата"):
            a.planting_a_plant(plant, instruments)

        self.assertEqual(a.plants[0].is_planted, True)

        expected_output: str = "индекс:  0 название растения:  ромашка посажено:  True ухожено:  False полито:  False\n"
        with patch('sys.stdout', new=StringIO()) as fake_out:
            a.print_list_of_the_plants()
            actual_output: str = fake_out.getvalue()

        self.assertEqual(expected_output, actual_output)

    def test_watering_my_plants(self):
        a = Plot("plot", 6)
        plant = Plant("ромашка")
        instruments = []
        instrument = Instrument("лопата")
        instruments.append(instrument)
        with patch('builtins.input', return_value="лопата"):
            a.planting_a_plant(plant, instruments)

        irrigation_system = IrrigationSystem()
        expected_output: str = "включена система полива\n"
        with patch('sys.stdout', new=StringIO()) as fake_out:
            irrigation_system.turn_on()
            actual_output: str = fake_out.getvalue()

        self.assertEqual(expected_output, actual_output)

        with patch('builtins.input', return_value="2"):
            a.watering_my_plants(irrigation_system)

        self.assertEqual(a.plants[0].is_watering, True)
        self.assertEqual(a.soil.is_watered, True)

    def test_take_care_of_plants(self):
        a = Plot("plot", 6)
        plant = Plant("ромашка")
        instruments = []
        instrument = Instrument("лопата")
        instruments.append(instrument)
        with patch('builtins.input', return_value="лопата"):
            a.planting_a_plant(plant, instruments)

        expected_output: str = "надо почистить инструмент\n"
        with patch('builtins.input', return_value="лопата"):
            with patch('sys.stdout', new=StringIO()) as fake_out:
                a.take_care_of_plant(instruments)
                actual_output: str = fake_out.getvalue()

        self.assertEqual(expected_output, actual_output)


class TestInstrument(unittest.TestCase):
    def test_instrument(self):
        name = "лопата"
        instrument = Instrument(name)
        self.assertEqual(instrument.name, "лопата")

    def test_clearing_instruments(self):
        name = "лопата"
        instrument = Instrument(name)
        self.assertEqual(instrument.status, True)
        instrument.status = False
        instrument.clearing()
        self.assertEqual(instrument.status, True)


class TestRecreationArea(unittest.TestCase):
    def test_recreation_area(self):
        expected_output: str = "зона отдыха успешно создана!\n"
        with patch('sys.stdout', new=StringIO()) as fake_out:
            area = RecreationArea("ad", 2)
            actual_output: str = fake_out.getvalue()
        self.assertEqual(expected_output, actual_output)

    def test_decoration(self):
        area = RecreationArea("ad", 2)
        instruments = []
        instrument = Instrument("лопата")
        instruments.append(instrument)

        with patch('builtins.input', side_effect=["2", "уточка"]):
            area.decoration(instruments)

        self.assertEqual(area.decorations, ["уточка"])

        with patch('builtins.input', side_effect=["1", "ромашка", "лопата"]):
            area.decoration(instruments)

        self.assertEqual(area.plants[0].name, "ромашка")

    def test_print(self):
        area = RecreationArea("ad", 2)
        instruments = []
        instrument = Instrument("лопата")
        instruments.append(instrument)

        with patch('builtins.input', side_effect=["2", "уточка"]):
            area.decoration(instruments)

        expected_output: str = "уточка\n"
        with patch('sys.stdout', new=StringIO()) as fake_out:
            area.print_list_of_decorations()
            actual_output: str = fake_out.getvalue()

        self.assertEqual(expected_output, actual_output)


class TestIrrigationSystem(unittest.TestCase):
    def test_fertilizing(self):
        irrigation_system = IrrigationSystem()
        irrigation_system.start_fertilize()
        self.assertEqual(irrigation_system.dunged, True)
        irrigation_system.stop_fertilize()
        self.assertEqual(irrigation_system.dunged, False)


if __name__ == '__main__':
    unittest.main()
