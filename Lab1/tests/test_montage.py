import unittest
from Montage import Montage


class MontageTestCase(unittest.TestCase):

    def test_load_number(self):
        montage = Montage()
        montage.increase_load_number()
        self.assertEqual(montage.get_load_number(), 1)
