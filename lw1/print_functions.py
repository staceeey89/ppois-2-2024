def bank_account_not_enough_money_for_investment():
    print('You have not enough money to make an investment. Would you like to make this investment with all'
          'money you have?y/n')


def bank_account_your_balance_is_0():
    print('Your balance is 0, so you can\'t make an investment')


def bank_account_risk_of_investment(risk=0.0):
    print(f'The risk of this investment is {risk}, would you like to make an investment? y/n')


def console_choose_operation():
    print('Choose operation:')


def console_make_transaction():
    print('1 - Make transaction')


def console_make_investment():
    print('2 - Make new investment')


def console_make_deposit():
    print('3 - Make deposit')


def console_make_withdrawal():
    print('4 - Make withdrawal')


def console_get_analysis():
    print('5 - Get bank account analysis')


def console_get_financial_report():
    print('6 - Get financial report')


def console_form_new_budget():
    print('7 - Form new budget')


def console_portfolio_management():
    print('8 - Portfolio management')


def console_exit():
    print('9 - Exit')


def console_choose_transaction():
    print('Choose transaction:')


def console_operation_inf(number=0, scope_or_company_or_bank_account_number=''):
    print(f'{number + 1} - {scope_or_company_or_bank_account_number}')


def console_enter_sum():
    print('Enter the sum:')


def console_transaction_complete(correct=True):
    print('Your transaction was ' + ('' if correct else 'not ') + 'completed')


def console_choose_investment():
    print('Choose investment:')


def console_report_text(text):
    print(text)


def console_transfer_money():
    print('Would you like to transfer your money to new budget? y/n')


def invalid_input():
    print('Invalid input')


def console_asset_allocation():
    print('1 - Asset allocation')


def console_diversification():
    print('2 - Diversification')


def console_risk_tolerance():
    print('3 - Risk tolerance')


def console_balance():
    print('4 - Balance')


def console_end_investment():
    print('5 - End investment and receive profit')


def console_wrong_operation_key():
    print('Wrong operation key')


def console_before_investment_operation(scope_of_investment='', previous_risk=0.0, previous_profit_ratio=0.0):
    print(f'Your {scope_of_investment} investment had {previous_risk} risk '
          f'and {previous_profit_ratio} profit_ratio')


def console_after_investment_operation(risk=0.0, profit_ratio=0.0):
    print(f'Now your investment has {risk} risk and {profit_ratio} profit ratio')


def console_balance_difference(previous_balance, current_balance):
    print(f'You completed operation. Your balance was {previous_balance} and now is {current_balance}')


def console_no_investments():
    print('You don\'t have any investments to work with')


def console_removing_investment(scope_of_investment=''):
    print(f'Your\'s {scope_of_investment} investment risk is higher than 1, so the investment is over, you got no money')
