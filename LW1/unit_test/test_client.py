from unittest import TestCase
from Client import Client
import unittest


class ClientTest(TestCase):

    def setUp(self):
        self.client = Client("Nikolai")

    def test_get_name(self):
        expected_name = 'John Doe'
        assert self.client.getname() != expected_name


if __name__ == "__main__":
    unittest.main()