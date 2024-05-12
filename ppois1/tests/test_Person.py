import unittest
from Person import Person


class TestPerson(unittest.TestCase):
    def setUp(self):
        self.my_person = Person("Bella", 23, True)

    def test_get_age(self):
        assert 23 == self.my_person.get_age()


if __name__ == '__main__':
    unittest.main()
