import datetime
from dataclasses import dataclass


@dataclass
class Player:
    id: int
    full_name: str
    birth_date: datetime.date
    football_team: str
    home_city: str
    team_size: int
    position: str

    # def __init__(self):
    #     self.id = None
    #     self.full_name = None
    #     self.birth_date: datetime.date = None
    #     self.football_team = None
    #     self.home_city = None
    #     self.team_size = None
    #     self.position = None
