import datetime
from typing import List

from config.constants import WEEKEND
from src.event import Crime
from src.officer import Officer
from utils.ccolors import ccolors
from utils.utils import time_calculation


class Investigation:
    def __init__(self, crime: Crime, assigned_officers: list):
        self.until = None
        self.crime = crime
        self.officers: List[Officer] = assigned_officers
        self.until: datetime.datetime

    def investigate(self, timenow: datetime.datetime):
        delta = 20 * time_calculation(self.crime.difficulty, self.officers)
        timenow = timenow + datetime.timedelta(hours=delta)
        self.until = timenow

        for i in self.officers:
            i.unavailable_until = timenow

    @property
    def law(self):
        return str(self.crime.law)

    @property
    def report(self):
        for i in self.officers:
            i.unavailable_until += datetime.timedelta(days=WEEKEND)
        return (f"{ccolors.HEADER}Дело:{ccolors.DEFAULT}\n"
                f"{self.__str__()}\n"
                f"{ccolors.HEADER}...было рассмотрено. Предъявлены обвинения по следующей статье:\n"
                f"{self.law}\n{ccolors.DEFAULT}")

    def __str__(self):
        return(f"{str(self.crime)}"
               f"")
