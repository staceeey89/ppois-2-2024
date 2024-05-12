class Report:
    def __init__(self, text='Classic report without information', date='01.01.01'):
        self.__text: str = text
        self.__date: str = date

    def form_analysis_text(self, transaction_history: list = None, investments: list = None, owner_name: str = '')\
            -> None:
        if transaction_history is None:
            transaction_history: list = []
        if investments is None:
            investments: list = []
        self.__text = f'Bank account owner is {owner_name}. He has done {len(transaction_history)} operations:'
        for i in transaction_history:
            if i.get_correct_operation():
                self.__text += f'\n{i.get_company_or_bank_account_number()}: {i.get_money_amount_spent()}'
            else:
                self.__text += f'\nOperation on {i.get_company_or_bank_account_number()} was not completed'
        self.__text += f'\nAnd has {len(investments)} investments:'
        for i in investments:
            self.__text += (f'\n{i.get_scope_of_investment()}: {i.get_price()}; '
                            f'risk: {i.get_risk()}; profit ratio: {i.get_profit_ratio()}')
        self.__text += f'\nDate: {self.__date}. Financial Management System owner: Karpuk M.'

    def form_financial_report_text(self, balance: float = 0, transactions_amount: int = 0, investments_amount: int = 0,
                                   owner_name: str = 'Tyler') -> None:
        self.__text = (f'Bank account owner is {owner_name}. He has done {transactions_amount} transactions and '
                       f'{investments_amount} investments. His balance is {balance}')
        self.__text += f'\nDate: {self.__date}. Financial Management System owner: Karpuk M.'

    def get_text(self) -> str:
        return self.__text
