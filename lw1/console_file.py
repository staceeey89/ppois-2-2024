import pickle
import random

from BankAccount import BankAccount
from FinanclialManagementSystem import FinancialManagementSystem
from Report import Report

import print_functions
# import base_values

with open('data_save.pickle', 'rb') as file:
    load_data = pickle.load(file)

financial_inf_system: FinancialManagementSystem = load_data['financial_inf_system']
bank_account: BankAccount = load_data['bank_account']
operations: int = load_data['operations']

while True:
    print_functions.console_choose_operation()
    print_functions.console_make_transaction()
    print_functions.console_make_investment()
    print_functions.console_make_deposit()
    print_functions.console_make_withdrawal()
    print_functions.console_get_analysis()
    print_functions.console_get_financial_report()
    print_functions.console_form_new_budget()
    print_functions.console_portfolio_management()
    print_functions.console_exit()
    operation_key: str = input()
    match operation_key:
        case '1':
            print_functions.console_choose_transaction()
            transactions: list = financial_inf_system.get_possible_transactions()
            for i in range(len(transactions)):
                print_functions.console_operation_inf(i, transactions[i].get_company_or_bank_account_number())
            index_str: str = input()
            if not index_str.isdigit():
                raise ValueError
            index: int = int(index_str) - 1
            if index >= len(transactions):
                raise IndexError
            print_functions.console_enter_sum()
            money_amount_str: str = input()
            if not money_amount_str.isdigit():
                raise ValueError
            money_amount: float = float(money_amount_str)
            bank_account.make_transaction(transactions[index], money_amount)
            transaction_history = bank_account.get_transactions_history()
            print_functions.console_transaction_complete(
                transaction_history[len(transaction_history) - 1].get_correct_operation())
        case '2':
            print_functions.console_choose_investment()
            investments: list = financial_inf_system.get_possible_investments()
            for i in range(len(investments)):
                print_functions.console_operation_inf(i, investments[i].get_scope_of_investment())
            index_str: str = input()
            if not index_str.isdigit():
                raise ValueError
            index: int = int(index_str) - 1
            if index >= len(investments):
                raise IndexError
            print_functions.console_enter_sum()
            money_amount_str: str = input()
            if not money_amount_str.isdigit():
                raise ValueError
            money_amount: float = float(money_amount_str)
            if money_amount <= 0:
                raise ValueError
            balance: float = bank_account.get_balance()
            if money_amount > balance:
                print_functions.bank_account_not_enough_money_for_investment()
                money_choice: str = input()
                if money_choice == 'y':
                    money_amount = balance
                else:
                    continue
                if money_amount == 0:
                    print_functions.bank_account_your_balance_is_0()
                    continue
            print_functions.bank_account_risk_of_investment(investments[index].get_risk())
            bet_choice: str = input()
            if bet_choice == 'y':
                bank_account.make_investment(investments[index], money_amount)
            else:
                continue
        case '3':
            previous_balance = bank_account.get_balance()
            print_functions.console_enter_sum()
            money_amount_str: str = input()
            if not money_amount_str.isdigit():
                raise ValueError
            money_amount = int(money_amount_str)
            bank_account.deposit(money_amount)
            print_functions.console_balance_difference(previous_balance, bank_account.get_balance())
        case '4':
            previous_balance = bank_account.get_balance()
            print_functions.console_enter_sum()
            money_amount_str: str = input()
            if not money_amount_str.isdigit():
                raise ValueError
            money_amount = int(money_amount_str)
            bank_account.withdrawal(money_amount)
            print_functions.console_balance_difference(previous_balance, bank_account.get_balance())
        case '5':
            analysis: Report = bank_account.get_analysis()
            print_functions.console_report_text(analysis.get_text())
        case '6':
            financial_report: Report = bank_account.get_financial_report()
            print_functions.console_report_text(financial_report.get_text())
        case '7':
            print_functions.console_transfer_money()
            decision = input()
            if decision != 'y' and decision != 'n':
                print_functions.invalid_input()
                continue
            bank_account.form_new_budget(False if decision == 'y' else True)
        case '8':
            investments: list = bank_account.get_investment_portfolio().get_investments()
            if len(investments) == 0:
                print_functions.console_no_investments()
                continue
            print_functions.console_choose_investment()
            for i in range(len(investments)):
                print_functions.console_operation_inf(i, investments[i].get_scope_of_investment())
            index_str: str = input()
            if not index_str.isdigit():
                raise ValueError
            index: int = int(index_str) - 1
            if index >= len(investments):
                raise IndexError
            print_functions.console_choose_operation()
            print_functions.console_asset_allocation()
            print_functions.console_diversification()
            print_functions.console_risk_tolerance()
            print_functions.console_balance()
            print_functions.console_end_investment()
            investment_operation_key = input()
            if investment_operation_key not in ['1', '2', '3', '4', '5']:
                print_functions.console_wrong_operation_key()
                continue
            previous_risk, previous_profit_ratio = investments[index].get_risk(), investments[index].get_profit_ratio()
            previous_balance = bank_account.get_balance()
            bank_account.portfolio_management(investments[index], investment_operation_key)
            if investment_operation_key != '5':
                print_functions.console_before_investment_operation(investments[index].get_scope_of_investment(),
                                                                    previous_risk, previous_profit_ratio)
                print_functions.console_after_investment_operation(investments[index].get_risk(),
                                                                   investments[index].get_profit_ratio())
            else:
                print_functions.console_balance_difference(previous_balance, bank_account.get_balance())
        case '9':
            break
        case _:
            print_functions.console_wrong_operation_key()
            continue

    operations += 1
    if operations % 3 == 0:
        investments = bank_account.get_investment_portfolio().get_investments()
        if len(investments) > 0:
            index = random.randint(0, len(investments) - 1)
            investments[index].risk_changing(bool(random.randint(0, 1)))
            investments[index].profit_ratio_changing(bool(random.randint(0, 1)))
            if investments[index].get_risk() >= 1.:
                print_functions.console_removing_investment(investments[index].get_scope_of_investment())
                bank_account.investment_removing(investments[index])
    data_to_save = {
        'financial_inf_system': financial_inf_system,
        'bank_account': bank_account,
        'operations': operations
    }

    with open('data_save.pickle', 'wb') as file:
        pickle.dump(data_to_save, file)

data_to_save = {
    'financial_inf_system': financial_inf_system,
    'bank_account': bank_account,
    'operations': operations
}

with open('data_save.pickle', 'wb') as file:
    pickle.dump(data_to_save, file)
