from Transaction import Transaction
from InvestmentPortfolio import InvestmentPortfolio
from Investment import Investment
from Budget import Budget
from Report import Report


class BankAccount:
    def __init__(self, unique_number: str = '0000', owner_name: str = 'Tyler', budget: Budget = Budget(),
                 transactions_history: list = None, investment_portfolio: InvestmentPortfolio = InvestmentPortfolio()):
        if transactions_history is None:
            transactions_history: list = []
        if len(unique_number) != 4:
            raise ValueError
        self.__unique_number: str = unique_number
        self.__owner_name: str = owner_name
        self.__budget: Budget = budget
        self.__transactions_history: list = transactions_history
        self.__investment_portfolio: InvestmentPortfolio = investment_portfolio

    def deposit(self, money_amount: float = 0.1) -> None:
        if money_amount <= 0:
            raise ValueError
        current_balance: float = self.__budget.get_money_amount()
        current_balance += money_amount
        self.__budget.set_money_amount(current_balance)
        self.__transactions_history.append(Transaction(money_amount, self.__unique_number, True))

    def withdrawal(self, money_amount: float = 0.1) -> None:
        if money_amount <= 0:
            raise ValueError
        current_balance: float = self.__budget.get_money_amount()
        if current_balance < money_amount:
            self.__transactions_history.append(Transaction(money_amount, self.__unique_number + '-withdrawal', False))
            return
        current_balance -= money_amount
        self.__transactions_history.append(Transaction(money_amount, self.__unique_number + '-withdrawal', True))
        self.__budget.set_money_amount(current_balance)

    def make_transaction(self, transaction: Transaction = Transaction(), money_amount: float = 0.0) -> None:
        if money_amount <= 0:
            raise ValueError
        new_transaction: Transaction = (
            Transaction(company_or_bank_account_number=transaction.get_company_or_bank_account_number()))
        new_transaction.set_money_amount_spend(money_amount)
        if money_amount > self.__budget.get_money_amount():
            new_transaction.set_correct_operation(False)
        else:
            current_balance: float = self.__budget.get_money_amount()
            current_balance -= money_amount
            self.__budget.set_money_amount(current_balance)
            new_transaction.set_correct_operation(True)
        self.__transactions_history.append(new_transaction)

    def make_investment(self, investment: Investment = Investment(), money_amount: float = 0.0) -> None:
        current_balance: float = self.__budget.get_money_amount()
        investment.set_price(money_amount)
        current_balance -= money_amount
        self.__budget.set_money_amount(current_balance)
        self.__investment_portfolio.add_new_investment(investment)

    def portfolio_management(self, investment: Investment = Investment(), operation_code: str = '1') -> None:
        if investment not in self.__investment_portfolio.get_investments():
            raise ValueError
        match operation_code:
            case '1':
                self.__investment_portfolio.asset_allocation(investment)
            case '2':
                self.__investment_portfolio.diversification(investment)
            case '3':
                self.__investment_portfolio.risk_tolerance(investment)
            case '4':
                self.__investment_portfolio.balance(investment)
            case '5':
                profit = self.__investment_portfolio.end_investment(investment)
                current_balance = self.__budget.get_money_amount()
                current_balance += profit
                self.__budget.set_money_amount(current_balance)
            case _:
                return

    def form_new_budget(self, withdrawing_money: bool = False) -> None:
        self.__transactions_history.clear()
        investment_profit: float = 0.0
        investments: list = self.__investment_portfolio.get_investments().copy()
        for i in investments:
            investment_profit += self.__investment_portfolio.end_investment(i)
        current_balance: float = self.__budget.get_money_amount() + investment_profit
        if withdrawing_money:
            current_balance = 0.0
        self.__budget.set_money_amount(current_balance)

    def get_analysis(self) -> Report:
        analysis_report: Report = Report(date='15.08.2005')
        analysis_report.form_analysis_text(self.__transactions_history, self.__investment_portfolio.get_investments(),
                                           self.__owner_name)
        return analysis_report

    def get_financial_report(self) -> Report:
        financial_report: Report = Report(date='27.08.1979')
        financial_report.form_financial_report_text(self.__budget.get_money_amount(), len(self.__transactions_history),
                                                    len(self.__investment_portfolio.get_investments()),
                                                    self.__owner_name)
        return financial_report

    def investment_removing(self, investment: Investment = Investment()) -> None:
        self.__investment_portfolio.remove_investment(investment)

    def get_unique_number(self) -> str:
        return self.__unique_number

    def get_owner_name(self) -> str:
        return self.__owner_name

    def get_transactions_history(self) -> list:
        return self.__transactions_history

    def get_investment_portfolio(self) -> InvestmentPortfolio:
        return self.__investment_portfolio

    def get_balance(self) -> float:
        return self.__budget.get_money_amount()
