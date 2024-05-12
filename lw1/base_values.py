from Transaction import Transaction
from Investment import Investment

possible_transactions = [Transaction(company_or_bank_account_number='Grocery'),
                         Transaction(company_or_bank_account_number='Dress store'),
                         Transaction(company_or_bank_account_number='Car shop'),
                         Transaction(company_or_bank_account_number='Education'),
                         Transaction(company_or_bank_account_number='Theater'),
                         Transaction(company_or_bank_account_number='Gaming store'),
                         Transaction(company_or_bank_account_number='5Element'),
                         Transaction(company_or_bank_account_number='Public Transport')]

possible_investments = [Investment('Ostis', risk=0.5, profit_ratio=2),
                        Investment('Education', risk=0.2, profit_ratio=1.1),
                        Investment('JKH', risk=0.8, profit_ratio=5),
                        Investment('Gaming company', risk=0.3, profit_ratio=1.05),
                        Investment('Google', risk=0.1, profit_ratio=1),
                        Investment('Student startup', risk=0.95, profit_ratio=7),
                        Investment('Bank stocks', risk=0.4, profit_ratio=1.5)]
