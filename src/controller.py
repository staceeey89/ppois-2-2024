import re


def check_date_format(date_string):
    pattern = r'^(19|20)\d\d[-](0[1-9]|1[012])[-](0[1-9]|[12][0-9]|3[01])$'
    if re.match(pattern, date_string):
        return True
    else:
        return False


def check_types(trn_name: str, trn_date: str, trn_sport: str, win_name: str, trn_prize: str):
    errors: str = ''
    trn_name = trn_name.split()
    trn_sport = trn_sport.split()
    win_name = win_name.split()
    if not all([el.isalnum() for el in trn_name]):
        errors += f'Incorrect Tournament Name: {trn_name}\n'
    if not check_date_format(trn_date):
        errors += f'Incorrect Date Format: {trn_date}\n'
    if not all([el.isalpha for el in trn_sport]):
        errors += f'Incorrect Tournament Sport: {trn_sport}\n'
    if not all([el.isalpha() for el in win_name]):
        errors += f'Incorrect Winner Name: {win_name}\n'
    if not trn_prize.isdigit():
        errors += f'Incorrect Tournament Prize: {trn_prize}\n'

    return errors
