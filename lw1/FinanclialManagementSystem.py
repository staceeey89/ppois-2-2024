import random

from Investment import Investment


class FinancialManagementSystem:
    def __init__(self, possible_investments: list = None, possible_transactions: list = None):
        if possible_investments is None:
            possible_investments: list = []
        if possible_transactions is None:
            possible_transactions: list = []
        self.__possible_investments: list = possible_investments
        self.__possible_transactions: list = possible_transactions

    def investment_changing(self, investment: Investment = Investment()) -> None:
        if investment not in self.__possible_investments:
            raise ValueError
        position: int = self.__possible_investments.index(investment)
        self.__possible_investments[position].risk_changing(bool(random.randint(0, 1)))
        self.__possible_investments[position].profit_ratio_changing(bool(random.randint(0, 1)))

    def get_possible_transactions(self) -> list:
        return self.__possible_transactions

    def get_possible_investments(self) -> list:
        return self.__possible_investments
