class Transaction:
    def __init__(self, money_amount_spent: float = 0.0, company_or_bank_account_number: str = '',
                 correct_operation: bool = True):
        if money_amount_spent < 0:
            raise ValueError
        self.__money_amount_spent: float = money_amount_spent
        self.__company_or_bank_account_number: str = company_or_bank_account_number
        self.__correct_operation: bool = correct_operation

    def get_money_amount_spent(self) -> float:
        return self.__money_amount_spent

    def get_company_or_bank_account_number(self) -> str:
        return self.__company_or_bank_account_number

    def get_correct_operation(self) -> bool:
        return self.__correct_operation

    def set_money_amount_spend(self, money_amount: float = 0.0) -> None:
        if money_amount < 0:
            raise ValueError
        self.__money_amount_spent = money_amount

    def set_correct_operation(self, correct: bool = True) -> None:
        self.__correct_operation = correct
