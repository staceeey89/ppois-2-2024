from .credit_card import CreditCard
from .transaction import Transaction
from .finance_exceptions import FinanceException
from datetime import datetime


class Bank:
    def __init__(self, name):
        self.name: str = name
        self.__cards: list[CreditCard] = []
        self.__transaction_history: list[Transaction] = []

    def add_card(self, card: CreditCard) -> None:
        self.__cards.append(card)

    def remove_card(self, card: CreditCard) -> None:
        self.__cards.remove(card)

    def get_cards(self) -> list[CreditCard]:
        return self.__cards

    def transfer(self, sender_card: CreditCard, receiver_card: CreditCard, pin: int, amount: int) -> None:
        if sender_card not in self.__cards or receiver_card not in self.__cards:
            raise FinanceException("Both of specified cards are not serviced by addressed bank")

        transaction = Transaction(sender_card, receiver_card, amount, datetime.now())
        try:
            sender_card.withdraw(amount, pin)
            receiver_card.deposit(amount)
            self.__transaction_history.append(transaction)
        except FinanceException as e:
            raise e
