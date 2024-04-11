import unittest
from unittest.mock import patch, MagicMock
from io import StringIO
import Tank as T

class TestTank(unittest.TestCase):
    def setUp(self):
        self.crew = [T.CrewMember("John", True), T.CrewMember("Jane", True)]
        self.equipment = [T.Equipment("Machine Gun", True), T.Equipment("Rocket Launcher", True)]
        self.fuel = T.Fuel("Diesel", 100)
        self.tank = T.Tank("T-34 No.1", self.crew, self.equipment, self.fuel, 1)

    def test_prepare_for_battle(self):
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.tank.prepare_for_battle()
            self.assertEqual(fake_out.getvalue().strip(), "Tank T-34 No.1 is preparing for battle.")

    def test_move_and_maneuver(self):
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.tank.move_and_maneuver()
            self.assertEqual(fake_out.getvalue().strip(), "Tank T-34 No.1 is moving and maneuvering.")

    def test_fire_and_shoot(self):
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.tank.fire_and_shoot()
            self.assertEqual(fake_out.getvalue().strip(), "Tank T-34 No.1 is firing and shooting.")

    def test_repair_and_maintenance(self):
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.tank.repair_and_maintenance()
            self.assertEqual(fake_out.getvalue().strip(), "Tank T-34 No.1 is being repaired and maintained.")

    def test_destroy(self):
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.tank.destroy()
            self.assertEqual(fake_out.getvalue().strip(), "Tank T-34 No.1 has been destroyed.")
            self.assertTrue(self.tank.is_destroyed)



class TestTankFunctions(unittest.TestCase):
    def setUp(self):
        self.tanks = {}

    def test_create_tank(self):
        with patch('sys.stdout', new=StringIO()) as fake_out:
            number = T.create_tank(self.tanks)
            self.assertEqual(fake_out.getvalue().strip(), f"Created tank T-34 No.{number}")
            self.assertIn(number, self.tanks)



    def test_destroy_nonexistent_tank(self):
        with patch('sys.stdout', new=StringIO()) as fake_out:
            T.destroy_tank(self.tanks, 999)
            self.assertEqual(fake_out.getvalue().strip(), "Tank No.999 does not exist.")

    def test_select_tank(self):
        number = T.create_tank(self.tanks)
        with patch('builtins.input', return_value=str(number)):
            selected_number = T.select_tank(self.tanks)
            self.assertEqual(selected_number, number)

    def test_select_destroyed_tank(self):
        number = T.create_tank(self.tanks)
        T.destroy_tank(self.tanks, number)
        with patch('builtins.input', return_value=str(number)):
            selected_number = T.select_tank(self.tanks)
            self.assertIsNone(selected_number)

    def test_change_tank_attribute(self):
        number = T.create_tank(self.tanks)
        with patch('builtins.input', return_value='New Tank Name'):
            T.change_tank_attribute(self.tanks, number)
            self.assertEqual(self.tanks[number].name, 'New Tank Name')

    def test_list_tanks(self):
        number = T.create_tank(self.tanks)
        with patch('sys.stdout', new=StringIO()) as fake_out:
            T.list_tanks(self.tanks)
            self.assertIn(f"Tank No.{number}: T-34 No.{number} (Available)", fake_out.getvalue())

    def test_perform_action(self):
        number = T.create_tank(self.tanks)
        with patch('sys.stdout', new=StringIO()) as fake_out:
            T.perform_action(self.tanks, number, 'prepare_for_battle')
            self.assertEqual(fake_out.getvalue().strip(), f"Tank T-34 No.{number} is preparing for battle.")

if __name__ == '__main__':
    unittest.main()