import unittest
from Investor import Investor
from ITCompany import ITCompany
from Project import Project


class TestInvestor(unittest.TestCase):
    def setUp(self):
        self.investor = Investor('John Doe')
        self.company = ITCompany('Test Company', 100000, 'Minsk')
        self.project = Project('Project X', 10000)

    def test_invest_in_company(self):
        initial_invested_amount = self.investor.get_invested_amount()
        amount = 5000
        self.investor.invest_in_company(self.company, amount)
        self.assertEqual(self.investor.get_invested_amount(), initial_invested_amount + amount)

    def test_invest_negative_amount(self):
        initial_invested_amount = self.investor.get_invested_amount()
        negative_amount = -5000
        self.investor.invest_in_company(self.company, negative_amount)
        self.assertEqual(self.investor.get_invested_amount(), initial_invested_amount)


if __name__ == "__main__":
    unittest.main()