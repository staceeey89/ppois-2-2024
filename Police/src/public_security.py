import datetime

from src.event import Call
from utils.utils import time_calculation


class PublicSecurity:
    def __init__(self, call: Call, assigned_officers: list):
        self.call = call
        self.officers = assigned_officers

    def public_security_operation(self, timenow: datetime.datetime):
        delta = 50 * time_calculation(self.call.difficulty, self.officers)
        timenow = timenow + datetime.timedelta(minutes=delta)

        for i in self.officers:
            i.unavailable_until = timenow

    def __str__(self):
        result = ''
        for i in self.officers:
            result += str(i)
        return result
