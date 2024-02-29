import unittest
from barbershop import Barbershop


class TestBarbershop(unittest.TestCase):
    def setUp(self):
        self.barbershop = Barbershop(500)

    def test_add_registration(self):
        self.barbershop.add_registration("John", "2", "9", "1", "20", "1")
        self.assertEqual(self.barbershop.registrations_count, 0)
        self.barbershop.purchase()
        self.assertEqual(self.barbershop.barbers_not_empty(), True)
        self.barbershop.add_registration("John", "2", "9", "1", "2", "1")
        self.assertEqual(self.barbershop.registrations_count, 1)
        with self.assertRaises(ValueError):
            self.barbershop.add_registration("John", "-1", "-1", "b", "a", "0")

    def test_delete_registration(self):
        self.barbershop1 = Barbershop(0)
        self.assertEqual(self.barbershop1.budget, 150)
        self.barbershop1.add_registration("John", "2", "9", "1", "2", "2")
        self.barbershop1.delete_registration("1")
        self.assertEqual(self.barbershop1.registrations_count, 0)
        self.assertIn("Неверный индекс", self.barbershop1.delete_registration("A"))

    def test_find_available_barber(self):
        self.assertIsNone(self.barbershop.find_available_barber())

    def test_perform_all_registered_services(self):
        self.barbershop.purchase()
        self.barbershop.add_registration("John", "5", "9", "2", "20", "1")
        self.barbershop.add_registration("John", "3", "9", "2", "2", "2")
        self.barbershop.add_registration("John", "2", "9", "1", "20", "1")
        self.barbershop.add_registration("John", "3", "9", "1", "2", "1")
        self.barbershop.add_registration("John", "2", "9", "3", "20", "1")
        self.barbershop.perform_all_registered_services()
        self.assertEqual(self.barbershop.registrations_count, 0)
        self.barbershop.add_registration("John", "2", "9", "1", "3", "1")
        self.barbershop.add_registration("Piter", "2", "9", "1", "3", "1")
        self.barbershop.perform_all_registered_services()
        self.assertEqual(self.barbershop.registrations_count, 0)

    def test_print(self):
        self.assertIn("Список всех записей:", self.barbershop.print_all_registrations())

    def test_barbers_not_empty(self):
        self.assertFalse(self.barbershop.barbers_not_empty())

    def test_purchase(self):
        initial_budget = self.barbershop.budget
        result = self.barbershop.purchase()
        self.assertLess(self.barbershop.budget, initial_budget)

    def test_find_barber(self):
        count = self.barbershop.find_available_barber()
        self.assertEqual(count, None)
        self.barbershop.purchase()
        self.assertFalse(self.barbershop.barbers_not_empty() is None)

    def test_barber_count(self):
        self.assertEqual(self.barbershop.barbers_count, 0)
        self.barbershop.add_barber()
        self.assertEqual(self.barbershop.barbers_count, 1)


if __name__ == '__main__':
    unittest.main()
