import unittest
from Person import Person


class TestPerson(unittest.TestCase):
    def test_constructor(self):
        person = Person("Иван", "Компания А")
        self.assertEqual(person.get_name(), "Иван")
        self.assertEqual(person.get_affiliation(), "Компания А")

    def test_set_name(self):
        person = Person("Иван", "Компания А")
        person.set_name("Петр")
        self.assertEqual(person.get_name(), "Петр")

        person.set_name(123)
        assert person.get_name != person.set_name

    def test_set_affiliation(self):
        person = Person("Иван", "Компания А")
        person.set_affiliation("Компания Б")
        self.assertEqual(person.get_affiliation(), "Компания Б")

        person.set_affiliation(123)
        assert person.get_affiliation != person.set_affiliation

if __name__ == '__main__':
    unittest.main()
