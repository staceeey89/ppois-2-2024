from typing import List

from src.model import Model
from extras.tournament import Tournament


class EmptyListStorage(Model):
    def __init__(self) -> None:
        super().__init__()
        self._tournaments: List[Tournament] = []

    def __len__(self) -> int:
        return len(self._tournaments)

    def insert(self, tournament: Tournament) -> None:
        self._tournaments.append(tournament)

    def get_all_tournaments(self, offset=0, limit=None) -> List[Tournament]:
        return self._tournaments[offset: offset + limit]

    def get_all_sports(self) -> List[str]:
        result = sorted({trn.trn_sport for trn in self._tournaments})
        return result

    def search_by_trn_name(self, trn_name: str, offset=0, limit=None) -> List[Tournament]:
        result = [trn for trn in self._tournaments if trn_name.lower() == trn.trn_name.lower()]
        return result[offset:offset + limit]

    def delete_by_trn_name(self, trn_name: str) -> int:
        to_delete = [trn for trn in self._tournaments if trn_name.lower() == trn.trn_name.lower()]
        for trn in to_delete:
            self._tournaments.remove(trn)
        return len(to_delete)

    def search_by_trn_sport(self, trn_sport: str, offset=0, limit=None) -> List[Tournament]:
        result = [trn for trn in self._tournaments if trn_sport.lower() == trn.trn_sport.lower()]
        return result[offset:offset + limit]

    def delete_by_trn_sport(self, trn_sport: str) -> int:
        to_delete = [trn for trn in self._tournaments if trn_sport.lower() == trn.trn_sport.lower()]
        for trn in to_delete:
            self._tournaments.remove(trn)
        return len(to_delete)

    def search_by_trn_prize(self, bottom: int, top: int, offset=0, limit=None) -> List[Tournament]:
        result = [trn for trn in self._tournaments if bottom <= trn.trn_prize <= top]
        return result[offset:offset + limit]

    def delete_by_trn_prize(self, bottom: int, top: int) -> int:
        to_delete = [trn for trn in self._tournaments if bottom <= trn.trn_prize <= top]
        for trn in to_delete:
            self._tournaments.remove(trn)
        return len(to_delete)
