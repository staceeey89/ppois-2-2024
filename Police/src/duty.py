import datetime

from utils.ccolors import ccolors


class Duty:
    def __init__(self, timenow: datetime.datetime):
        self.patrol = []
        self.detective = []
        self.public_security_team = []
        self.timenow: datetime.datetime = timenow
        self.score = 0

    def __str__(self):
        blue = ''
        for i in self.patrol:
            blue += f"{ccolors.BLUE}{i}{ccolors.DEFAULT}\n"

        green = ''
        for i in self.public_security_team:
            green += f"{ccolors.GREEN}{i}{ccolors.DEFAULT}\n"

        brown = ''
        for i in self.detective:
            brown += f"{ccolors.BROWN}{i}{ccolors.DEFAULT}\n"

        return (f"{ccolors.WARNING}Ваша смена сегодня:\n"
                f"{ccolors.BLUE}Патруль{ccolors.DEFAULT}, недоступный для вызовов, офицеры, которые {ccolors.GREEN}"
                f" отвечают на вызовы{ccolors.DEFAULT} и {ccolors.BROWN}детективы{ccolors.DEFAULT}:\n"
                f"{blue}"
                f"{green}"
                f"{brown}")
