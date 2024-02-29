from .interfaces import PaymentMean
from .finance_exceptions import FinanceException
from .card_owner import CardOwner
import random


class CreditCard(PaymentMean):
    def __init__(self,
                 card_number,
                 owner: CardOwner,
                 pin: int = random.randint(1000, 10000),
                 is_blocked: bool = False):
        self.card_number: str = card_number
        self.owner: CardOwner = owner
        self.__payment_limit: int = 0
        self.__pin: int = 0
        self.set_pin(pin)
        self.__balance: int = 0
        self.__is_blocked: bool = is_blocked
        self.__wrong_pin_inputs: int = 0

    def __check_pin(self, pin: int) -> None:
        if self.__is_blocked:
            raise FinanceException("The card is blocked")
        if pin == self.__pin:
            self.__wrong_pin_inputs = 0
            return
        else:
            self.__wrong_pin_inputs += 1
            if self.__wrong_pin_inputs >= 3:
                self.block()
            raise FinanceException("Wrong pin")

    def __check_balance(self, amount: int) -> None:
        if amount > self.__balance:
            raise FinanceException("Too low balance")

    def deposit(self, amount: int) -> None:
        if self.__is_blocked:
            raise FinanceException("The card is blocked")
        if amount <= 0:
            raise ValueError("Cannot deposit non-positive amount")
        self.__balance += amount

    def withdraw(self, amount: int, pin: int) -> None:
        self.__check_pin(pin)
        self.__check_balance(amount)
        if amount <= 0:
            raise ValueError("Cannot withdraw non-positive amount")
        self.__balance -= amount

    def pay(self, amount: int, pin: int) -> None:
        self.__check_pin(pin)
        self.__check_balance(amount)
        if amount <= 0:
            raise ValueError("Cannot pay non-positive amount")

        if self.__payment_limit != 0 and amount > self.__payment_limit:
            raise FinanceException("Too high sum for one payment")

        self.__balance -= amount

    def get_balance(self, pin: int) -> int:
        self.__check_pin(pin)
        return self.__balance

    def is_blocked(self) -> bool:
        return self.__is_blocked

    def block(self) -> None:
        self.__is_blocked = True

    def unblock(self) -> None:
        self.__is_blocked = False

    def set_pin(self, new_pin: int) -> None:
        if new_pin < 1000 or new_pin >= 10000:
            raise ValueError("Pin must be 4-digit number")
        self.__pin = new_pin

    def set_limit(self, pin: int, new_limit: int) -> None:
        self.__check_pin(pin)
        if new_limit < 0:
            raise ValueError("Limit can't be negative")

        self.__payment_limit = new_limit
