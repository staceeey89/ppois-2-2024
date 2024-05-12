import datetime
from dataclasses import dataclass


@dataclass(eq=True, frozen=True)
class PlayerDto:
    id: int
    full_name: str
    birth_date: datetime.date
    football_team: str
    home_city: str
    team_size: int
    position: str
