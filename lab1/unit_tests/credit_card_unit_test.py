import unittest
from finances.credit_card import CreditCard
from finances.card_owner import CardOwner
from finances.finance_exceptions import FinanceException


class TestCreditCard(unittest.TestCase):

    def setUp(self):
        owner = CardOwner(name="John Doe", address="123 Main St", email="john@example.com", phone="555-5555")
        self.credit_card = CreditCard(card_number="1234567890123456", owner=owner)
        self.pin = 1234
        self.credit_card.set_pin(self.pin)

    def test_deposit(self):
        # Test deposit method
        self.credit_card.deposit(500)
        self.assertEqual(self.credit_card.get_balance(self.pin), 500)

    def test_withdraw(self):
        # Test withdraw method
        self.credit_card.deposit(1000)
        self.credit_card.withdraw(500, self.pin)
        self.assertEqual(self.credit_card.get_balance(self.pin), 500)

    def test_pay(self):
        # Test pay method
        self.credit_card.deposit(1000)
        self.credit_card.pay(500, self.pin)
        self.assertEqual(self.credit_card.get_balance(self.pin), 500)

    def test_get_balance(self):
        # Test get_balance method
        self.credit_card.deposit(1000)
        self.assertEqual(self.credit_card.get_balance(self.pin), 1000)

    def test_is_blocked(self):
        # Test is_blocked method
        self.assertFalse(self.credit_card.is_blocked())

    def test_block(self):
        # Test block method
        self.credit_card.block()
        self.assertTrue(self.credit_card.is_blocked())

    def test_unblock(self):
        # Test unblock method
        self.credit_card.unblock()
        self.assertFalse(self.credit_card.is_blocked())

    def test_deposit_non_positive_amount(self):
        # Test deposit method with non-positive amount
        with self.assertRaises(ValueError):
            self.credit_card.deposit(-100)

    def test_withdraw_non_positive_amount(self):
        # Test withdraw method with non-positive amount
        with self.assertRaises(ValueError):
            self.credit_card.withdraw(-100, self.pin)

    def test_pay_non_positive_amount(self):
        # Test pay method with non-positive amount
        with self.assertRaises(ValueError):
            self.credit_card.pay(-100, self.pin)

    def test_withdraw_wrong_pin(self):
        # Test withdraw method with wrong pin
        with self.assertRaises(FinanceException):
            self.credit_card.deposit(1000)
            self.credit_card.withdraw(500, pin=9999)

    def test_pay_wrong_pin(self):
        # Test pay method with wrong pin
        with self.assertRaises(FinanceException):
            self.credit_card.deposit(1000)
            self.credit_card.pay(500, pin=9999)

    def test_set_limit_wrong_pin(self):
        # Test set_limit method with wrong pin
        with self.assertRaises(FinanceException):
            self.credit_card.set_limit(pin=9999, new_limit=1500)

    def test_set_limit_negative_limit(self):
        # Test set_limit method with negative limit
        with self.assertRaises(ValueError):
            self.credit_card.set_limit(self.pin, new_limit=-100)


if __name__ == '__main__':
    unittest.main()
