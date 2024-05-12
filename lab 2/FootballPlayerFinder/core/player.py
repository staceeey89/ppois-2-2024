from datetime import datetime


class Player:
    def __init__(self, full_name, birth_date, football_team, home_city, squad, position):
        self.full_name = full_name
        self.football_team = football_team
        self.home_city = home_city
        self.squad = squad
        self.position = position
        self.birth_date = birth_date

    def get_player_data(self):
        return (
            self.full_name,
            self.birth_date,
            self.football_team,
            self.home_city,
            self.squad,
            self.position
        )
