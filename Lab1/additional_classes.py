# additional_classes.py
import re
from datetime import datetime


class AdditionalClasses:
    def __init__(self, title: str, date: str):
        self.title = title
        self.is_valid_date(date)
        self.date = date

    def conduct_class(self):
        print(f"Дополнительное занятие '{self.title}' проводится {self.date}")

    @staticmethod
    def is_valid_date(date: str):
        pattern = r'^(0[1-9]|[12][0-9]|3[01])\.(0[1-9]|1[012])\.(19|20)\d{2}$'

        if re.match(pattern, date):
            try:
                datetime.strptime(date, '%d.%m.%Y')
                return True
            except ValueError:
                return False
        else:
            return False
