from typing import List

from extras.tournament import Tournament


class Model:
    def __init__(self) -> None:
        pass

    def insert(self, tournament: Tournament) -> None:
        pass

    def get_all_tournaments(self) -> List[Tournament]:
        pass

    def get_all_sports(self) -> List[str]:
        pass

    def search_by_trn_name(self, trn_name: str) -> List[Tournament]:
        pass

    def delete_by_trn_name(self, trn_name: str) -> int:
        pass

    def search_by_trn_sport(self, trn_sport: str) -> List[Tournament]:
        pass

    def delete_by_trn_sport(self, trn_sport: str) -> int:
        pass

    def search_by_trn_prize(self, bottom: int, top: int) -> List[Tournament]:
        pass

    def delete_by_trn_prize(self, bottom: int, top: int) -> int:
        pass

    def save(self) -> None:
        pass
