import unittest
from Product import Product


class TestPerson(unittest.TestCase):
    def setUp(self):
        self.product = Product("gloves", 10)

    def test_set_price(self):
        new_price = self.product.set_price(12)
        assert 12 == self.product.get_price()


if __name__ == '__main__':
    unittest.main()
