from Investment import Investment


class InvestmentPortfolio:
    def __init__(self, investments: list = None):
        if investments is None:
            investments = []
        self.__investments: list = investments

    def asset_allocation(self, investment: Investment = Investment()) -> None:
        if investment not in self.__investments:
            raise ValueError
        position: int = self.__investments.index(investment)
        self.__investments[position].risk_changing(False)
        self.__investments[position].profit_ratio_changing(True)

    def diversification(self, investment: Investment = Investment()) -> None:
        if investment not in self.__investments:
            raise ValueError
        position: int = self.__investments.index(investment)
        self.__investments[position].risk_changing(False)
        self.__investments[position].profit_ratio_changing(False)

    def risk_tolerance(self, investment: Investment = Investment()) -> None:
        if investment not in self.__investments:
            raise ValueError
        position: int = self.__investments.index(investment)
        self.__investments[position].risk_changing(False)
        self.__investments[position].profit_ratio_changing(True)

    def balance(self, investment: Investment = Investment()) -> None:
        if investment not in self.__investments:
            raise ValueError
        position: int = self.__investments.index(investment)
        self.__investments[position].risk_changing(False)

    def end_investment(self, investment: Investment = Investment()) -> float:
        if investment not in self.__investments:
            raise ValueError
        position: int = self.__investments.index(investment)
        profit: float = self.__investments[position].get_price() * self.__investments[position].get_profit_ratio()
        self.__investments.remove(investment)
        return profit

    def remove_investment(self, investment: Investment = Investment) -> None:
        if investment not in self.__investments:
            raise ValueError
        self.__investments.remove(investment)

    def add_new_investment(self, investment: Investment = Investment()) -> None:
        if investment in self.__investments:
            raise ValueError
        self.__investments.append(investment)

    def get_investments(self) -> list:
        return self.__investments
