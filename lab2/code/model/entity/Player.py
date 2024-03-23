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
