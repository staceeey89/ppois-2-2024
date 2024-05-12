class Budget:
    def __init__(self, money_amount: float = 0.0):
        if money_amount < 0:
            raise ValueError
        self.__money_amount: float = money_amount

    def get_money_amount(self) -> float:
        return self.__money_amount

    def set_money_amount(self, new_amount: float) -> None:
        if new_amount < 0:
            raise ValueError
        self.__money_amount = new_amount

