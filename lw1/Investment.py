import random


class Investment:
    def __init__(self, scope_of_investment: str = 'NoName Company', price: float = 0.0, risk: float = 0.0,
                 profit_ratio: float = 0.0):
        if price < 0 or profit_ratio < 0:
            raise ValueError
        self.__scope_of_investment: str = scope_of_investment
        self.__price: float = price
        self.__risk: float = risk
        self.__profit_ratio: float = profit_ratio

    def risk_changing(self, increasing: bool = True) -> None:
        self.__risk += pow(-1, int(not increasing)) * (random.random() / 10)
        self.__risk = max(0., self.__risk)

    def profit_ratio_changing(self, increasing: bool = True) -> None:
        self.__profit_ratio += pow(-1, int(not increasing)) * (random.random() / 10)
        self.__risk = max(0., self.__risk)

    def get_scope_of_investment(self) -> str:
        return self.__scope_of_investment

    def get_price(self) -> float:
        return self.__price

    def get_risk(self) -> float:
        return self.__risk

    def get_profit_ratio(self) -> float:
        return self.__profit_ratio

    def set_price(self, money_amount: float) -> None:
        if money_amount < 0:
            raise ValueError
        self.__price = money_amount

    def __eq__(self, other) -> bool:
        return self.__scope_of_investment == other.get_scope_of_investment()
