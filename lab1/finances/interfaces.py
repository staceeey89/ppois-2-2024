from typing import Optional


class PaymentMean:
    def pay(self, amount: int, pin: Optional[int]) -> None:
        pass

    def deposit(self, amount: int) -> None:
        pass

    def withdraw(self, amount: int, pin: Optional[int]) -> None:
        pass
