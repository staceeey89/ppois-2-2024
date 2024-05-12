import unittest

from Budget import Budget
from Transaction import Transaction
from Investment import Investment
from Report import Report
from FinanclialManagementSystem import FinancialManagementSystem
from InvestmentPortfolio import InvestmentPortfolio
from BankAccount import BankAccount


class TestBudget(unittest.TestCase):
    def test_budget(self):
        self.budget: Budget = Budget(10.0)
        self.assertEqual(self.budget.get_money_amount(), 10.0)
        self.budget.set_money_amount(20.0)
        self.assertEqual(self.budget.get_money_amount(), 20.0)


class TestTransaction(unittest.TestCase):
    def test_transaction_init(self):
        self.transaction: Transaction = Transaction(10.0, 'company', True)
        self.assertEqual(self.transaction.get_company_or_bank_account_number(), 'company')
        self.assertEqual(self.transaction.get_correct_operation(), True)
        self.assertEqual(self.transaction.get_money_amount_spent(), 10.0)

    def test_transaction_setters(self):
        self.transaction: Transaction = Transaction(10.0, 'company', True)
        self.transaction.set_money_amount_spend(20.0)
        self.transaction.set_correct_operation(False)
        self.assertEqual(self.transaction.get_money_amount_spent(), 20.0)
        self.assertEqual(self.transaction.get_correct_operation(), False)

    def test_investment_init(self):
        self.investment: Investment = Investment('company', 10.0, 0.5, 2.0)
        self.assertEqual(self.investment.get_scope_of_investment(), 'company')
        self.assertEqual(self.investment.get_price(), 10.0)
        self.assertEqual(self.investment.get_risk(), 0.5)
        self.assertEqual(self.investment.get_profit_ratio(), 2.0)


class TestInvestment(unittest.TestCase):
    def test_investment_changing_methods(self):
        self.investment: Investment = Investment('company', 10.0, 0.5, 2.0)
        previous_risk = self.investment.get_risk()
        previous_profit_ratio = self.investment.get_profit_ratio()
        self.investment.risk_changing(True)
        self.investment.profit_ratio_changing(True)
        self.assertNotEqual(previous_risk, self.investment.get_risk())
        self.assertNotEqual(previous_profit_ratio, self.investment.get_profit_ratio())

    def test_investment_setter(self):
        self.investment: Investment = Investment()
        self.investment.set_price(10.0)
        self.assertEqual(self.investment.get_price(), 10.0)


class TestReport(unittest.TestCase):
    def test_report_init(self):
        self.report: Report = Report(text='123')
        self.assertEqual(self.report.get_text(), '123')

    def test_report_analysis(self):
        self.report: Report = Report(date='123')
        self.report.form_analysis_text([Transaction(10.0, 'company', True),
                                        Transaction(5.0, 'qwerty', False)],
                                       [Investment('house', 5.0, 0.5, 2.0)],
                                       'Maksim')
        expected_text: str = """Bank account owner is Maksim. He has done 2 operations:
company: 10.0
Operation on qwerty was not completed
And has 1 investments:
house: 5.0; risk: 0.5; profit ratio: 2.0
Date: 123. Financial Management System owner: Karpuk M."""
        self.assertEqual(self.report.get_text(), expected_text)

    def test_financial_report(self):
        self.report = Report(date='123')
        self.report.form_financial_report_text(10.0, 1,
                                               1, 'Maksim')
        expected_text: str = """Bank account owner is Maksim. He has done 1 transactions and 1 investments. His balance is 10.0 
Date: 123. Financial Management System owner: Karpuk M."""
        self.assertEqual(self.report.get_text(), expected_text)


class TestFinancialManagementSystem(unittest.TestCase):
    def test_financial_management_system_init(self):
        self.system1: FinancialManagementSystem = FinancialManagementSystem()
        self.assertEqual(self.system1.get_possible_investments(), [])
        self.assertEqual(self.system1.get_possible_transactions(), [])

        self.system2: FinancialManagementSystem = FinancialManagementSystem([Investment(scope_of_investment='test')],
                                                 [Transaction(company_or_bank_account_number='test')])
        self.assertEqual(Transaction(company_or_bank_account_number='test').get_company_or_bank_account_number(),
                         self.system2.get_possible_transactions()[0].get_company_or_bank_account_number())
        self.assertEqual(Investment('test'), self.system2.get_possible_investments()[0])

    def test_financial_management_system_investment_changing(self):
        self.system: FinancialManagementSystem = FinancialManagementSystem(possible_investments=
                                                [Investment('company', 5.0, 0.5, 2.0)])
        previous_risk: float = self.system.get_possible_investments()[0].get_risk()
        previous_profit_ratio: float = self.system.get_possible_investments()[0].get_profit_ratio()
        self.system.investment_changing(Investment('company', 5.0, 0.5, 2.0))
        self.assertNotEqual(previous_risk, self.system.get_possible_investments()[0].get_risk())
        self.assertNotEqual(previous_profit_ratio, self.system.get_possible_investments()[0].get_profit_ratio())


class TestInvestmentPortfolio(unittest.TestCase):
    def test_investment_portfolio_init(self):
        self.investment_portfolio1: InvestmentPortfolio = InvestmentPortfolio()
        self.assertEqual(self.investment_portfolio1.get_investments(), [])

        self.investment_portfolio2: InvestmentPortfolio = InvestmentPortfolio([Investment('test')])
        self.assertEqual(self.investment_portfolio2.get_investments()[0], Investment('test'))

    def test_investment_portfolio_asset_allocation(self):
        self.investment_portfolio: InvestmentPortfolio = InvestmentPortfolio([Investment('test', 5.0, 0.5, 2.0)])
        previous_risk: float = self.investment_portfolio.get_investments()[0].get_risk()
        previous_profit_ratio: float = self.investment_portfolio.get_investments()[0].get_profit_ratio()
        self.investment_portfolio.assert_allocation(Investment('test'))
        self.assertGreaterEqual(previous_risk, self.investment_portfolio.get_investments()[0].get_risk())
        self.assertLessEqual(previous_profit_ratio,
                             self.investment_portfolio.get_investments()[0].get_profit_ratio())

    def test_investment_portfolio_diversification(self):
        self.investment_portfolio: InvestmentPortfolio = InvestmentPortfolio([Investment('test', 5.0, 0.5, 2.0)])
        previous_risk: float = self.investment_portfolio.get_investments()[0].get_risk()
        previous_profit_ratio: float = self.investment_portfolio.get_investments()[0].get_profit_ratio()
        self.investment_portfolio.diversification(Investment('test'))
        self.assertGreaterEqual(previous_risk, self.investment_portfolio.get_investments()[0].get_risk())
        self.assertGreaterEqual(previous_profit_ratio,
                                self.investment_portfolio.get_investments()[0].get_profit_ratio())

    def test_investment_portfolio_risk_tolerance(self):
        self.investment_portfolio: InvestmentPortfolio = InvestmentPortfolio([Investment('test', 5.0, 0.5, 2.0)])
        previous_risk: float = self.investment_portfolio.get_investments()[0].get_risk()
        previous_profit_ratio: float = self.investment_portfolio.get_investments()[0].get_profit_ratio()
        self.investment_portfolio.risk_tolerance(Investment('test'))
        self.assertGreaterEqual(previous_risk, self.investment_portfolio.get_investments()[0].get_risk())
        self.assertLessEqual(previous_profit_ratio,
                             self.investment_portfolio.get_investments()[0].get_profit_ratio())

    def test_investment_portfolio_balance(self):
        self.investment_portfolio: InvestmentPortfolio = InvestmentPortfolio([Investment('test', 5.0, 0.5, 2.0)])
        previous_risk: float = self.investment_portfolio.get_investments()[0].get_risk()
        self.investment_portfolio.balance(Investment('test'))
        self.assertGreaterEqual(previous_risk, self.investment_portfolio.get_investments()[0].get_risk())

    def test_investment_portfolio_end_and_remove_investment(self):
        self.investment_portfolio: InvestmentPortfolio = InvestmentPortfolio([Investment('test', 5.0, 0.5, 2.0),
                                                         Investment('test1', 10.0, 0.2, 3.0)])
        self.investment_portfolio.remove_investment(Investment('test1'))
        self.assertEqual(len(self.investment_portfolio.get_investments()), 1)

        self.assertEqual(self.investment_portfolio.end_investment(Investment('test')), 10.0)
        self.assertEqual(len(self.investment_portfolio.get_investments()), 0)


class TestBankAccount(unittest.TestCase):
    def test_bank_account_init(self):
        self.bank_account: BankAccount = BankAccount('1234', 'Maksim', Budget(10.0),
                                        [Transaction(10.0, 'test', True)],
                                        InvestmentPortfolio([Investment('test')]))
        self.assertEqual(self.bank_account.get_balance(), 10.0)
        self.assertEqual(self.bank_account.get_unique_number(), '1234')
        self.assertEqual(self.bank_account.get_owner_name(), 'Maksim')
        self.assertEqual(self.bank_account.get_transactions_history()[0].get_company_or_bank_account_number(),
                         Transaction(company_or_bank_account_number='test').get_company_or_bank_account_number())
        self.assertEqual(self.bank_account.get_investment_portfolio().get_investments()[0], Investment('test'))

    def test_bank_account_deposit(self):
        self.bank_account: BankAccount = BankAccount(budget=Budget(10.0))
        self.bank_account.deposit(20.0)
        self.assertEqual(self.bank_account.get_balance(), 30.0)

    def test_bank_account_withdrawal(self):
        self.bank_account: BankAccount = BankAccount(budget=Budget(10.0))
        self.bank_account.withdrawal(5.0)
        self.assertEqual(self.bank_account.get_balance(), 5.0)

    def test_bank_account_make_transaction(self):
        self.bank_account: BankAccount = BankAccount(budget=Budget(10.0))
        self.bank_account.make_transaction(Transaction(company_or_bank_account_number='test'), 5.0)
        transaction: Transaction = self.bank_account.get_transactions_history()[0]
        self.assertEqual(self.bank_account.get_balance(), 5.0)
        self.assertEqual(transaction.get_company_or_bank_account_number(), 'test')
        self.assertEqual(transaction.get_money_amount_spent(), 5.0)
        self.assertEqual(transaction.get_correct_operation(), True)

    def test_bank_account_make_investment(self):
        self.bank_account: BankAccount = BankAccount(budget=Budget(10.0))
        self.bank_account.make_investment(Investment('test'), 5.0)
        investment: Investment = self.bank_account.get_investment_portfolio().get_investments()[0]
        self.assertEqual(self.bank_account.get_balance(), 5.0)
        self.assertEqual(investment, Investment('test'))

    def test_bank_account_portfolio_management(self):
        self.bank_account: BankAccount = BankAccount(
            investment_portfolio=InvestmentPortfolio([Investment('test', 5.0, 0.5, 2.0)]))
        previous_risk: float = self.bank_account.get_investment_portfolio().get_investments()[0].get_risk()
        previous_profit_ratio: float = (
            self.bank_account.get_investment_portfolio().get_investments()[0].get_profit_ratio())
        self.bank_account.portfolio_management(Investment('test'), '1')
        self.assertGreaterEqual(previous_risk,
                                self.bank_account.get_investment_portfolio().get_investments()[0].get_risk())
        self.assertLessEqual(previous_profit_ratio,
                             self.bank_account.get_investment_portfolio().get_investments()[0].get_profit_ratio())

    def test_bank_account_form_new_budget(self):
        self.bank_account1: BankAccount = BankAccount(transactions_history=[Transaction(5, 'test')], budget=Budget(10.0))
        self.bank_account1.form_new_budget(False)
        self.assertEqual(len(self.bank_account1.get_transactions_history()), 0)
        self.assertEqual(self.bank_account1.get_balance(), 10.0)

        self.bank_account2: BankAccount = BankAccount(budget=Budget(10.0))
        self.bank_account2.form_new_budget(True)
        self.assertEqual(self.bank_account2.get_balance(), 0)
