from datetime import date


class Tournament:
    def __init__(self,
                 identifier: int,
                 trn_name: str,
                 trn_date: date,
                 trn_sport: str,
                 win_name: str,
                 trn_prize: int,
                 win_prize=None) -> None:
        self.id = identifier
        self.trn_name = trn_name
        self.trn_date = trn_date
        self.trn_sport = trn_sport
        self.win_name = win_name
        self.trn_prize = trn_prize
        self.win_prize = win_prize if win_prize else int(0.6 * trn_prize)

    def __str__(self) -> str:
        return (f'{self.trn_name} '
                f'{self.trn_date} '
                f'{self.trn_sport} '
                f'{self.win_name} '
                f'{self.trn_prize} '
                f'{self.win_prize}')
