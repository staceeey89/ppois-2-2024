import unittest
from vacuum_cleaner import VacuumCleaner
from room import Room


class TestVacuumCleaner(unittest.TestCase):
    def setUp(self):
        self.test_vacuum = VacuumCleaner("red", "samsung")
        self.test_vacuum.engine.set_power(100, 300)
        self.test_vacuum.control_buttons.change_power(200)
        self.room = Room(3, 5)

    def test_put_on_nozzle(self):
        self.test_vacuum.put_on_nozzle("Turbo Brush")
        self.assertEqual(self.test_vacuum.nozzle.turbo_brush, True)

    def test_change_nozzle(self):
        self.test_vacuum.change_nozzle("Corner Nozzle")
        self.assertEqual(self.test_vacuum.nozzle.corner_nozzle, True)
        self.assertEqual(self.test_vacuum.nozzle.turbo_brush, False)

    def test_cleaning_dust_cont(self):
        self.test_vacuum.dust_container.isFilled = True
        self.test_vacuum.clean_dust_container()
        self.assertEqual(self.test_vacuum.dust_container.isFilled, False)

    def test_start_vacuum(self):
        self.test_vacuum.start_vacuum(100)
        self.assertEqual(self.test_vacuum.control_buttons.start_b, True)

    def test_room_cleaning(self):
        self.test_vacuum.start_vacuum(200)
        self.test_vacuum.clean_room(self.room)
        self.assertEqual(self.test_vacuum.dust_container.isFilled, True)
        self.assertEqual(self.test_vacuum.filter.health, 4)
        self.assertEqual(self.test_vacuum.engine.health, 95)
        self.test_vacuum.technical_work()
        self.assertEqual(self.test_vacuum.dust_container.isFilled, False)
        self.assertEqual(self.test_vacuum.filter.health, 5)
        self.assertEqual(self.test_vacuum.engine.health, 100)
