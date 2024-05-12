from unittest.mock import MagicMock
import unittest
from finances.credit_card import CreditCard
from finances.bank import Bank
from finances.finance_exceptions import FinanceException


class TestBank(unittest.TestCase):

    def setUp(self):
        self.bank = Bank("Test Bank")

    def test_add_card(self):
        # Test adding a card to the bank
        card = MagicMock(spec=CreditCard)
        self.bank.add_card(card)
        self.assertIn(card, self.bank.get_cards())

    def test_remove_card(self):
        # Test removing a card from the bank
        card = MagicMock(spec=CreditCard)
        self.bank.add_card(card)
        self.bank.remove_card(card)
        self.assertNotIn(card, self.bank.get_cards())

    def test_transfer(self):
        # Test transferring between cards
        sender_card = MagicMock(spec=CreditCard)
        receiver_card = MagicMock(spec=CreditCard)
        sender_card.withdraw.return_value = None
        receiver_card.deposit.return_value = None
        pin = 1234
        amount = 100
        self.bank.add_card(sender_card)
        self.bank.add_card(receiver_card)
        self.bank.transfer(sender_card, receiver_card, pin, amount)
        sender_card.withdraw.assert_called_once_with(amount, pin)
        receiver_card.deposit.assert_called_once_with(amount)

    def test_transfer_non_serviced_cards(self):
        # Test transferring money between cards that are not serviced by the bank
        sender_card = MagicMock(spec=CreditCard)
        receiver_card = MagicMock(spec=CreditCard)
        pin = 1234
        amount = 100
        with self.assertRaises(FinanceException):
            self.bank.transfer(sender_card, receiver_card, pin, amount)


if __name__ == '__main__':
    unittest.main()
