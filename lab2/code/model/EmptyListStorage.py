from typing import List

from model.entity.Player import Player


class EmptyListStorage:
    def __init__(self, *args):
        super().__init__()
        self._players: List[Player] = []

    def insert(self, player: Player):
        self._players.append(player)

    def get_all_players(self) -> List[Player]:
        return self._players

    def search_by_name(self, name: str, offset=0, limit=None) -> List[Player]:
        result = [player for player in self._players if name.lower() in player.full_name.lower()]
        return result[offset:offset + limit] if limit else result

    def delete_by_name(self, name: str) -> int:
        players_to_remove = [player for player in self._players if name.lower() in player.full_name.lower()]
        for player in players_to_remove:
            self._players.remove(player)
        return len(players_to_remove)

    def search_by_birth_date(self, birth_date: str, offset=0, limit=None) -> List[Player]:
        result = [player for player in self._players if birth_date == player.birth_date]
        return result[offset:offset + limit] if limit else result

    def delete_by_birth_date(self, birth_date: str) -> int:
        players_to_remove = [player for player in self._players if birth_date == player.birth_date]
        for player in players_to_remove:
            self._players.remove(player)
        return len(players_to_remove)

    def search_by_position(self, position: str, offset=0, limit=None) -> List[Player]:
        result = [player for player in self._players if position.lower() == player.position.lower()]
        return result[offset:offset + limit] if limit else result

    def delete_by_position(self, position: str) -> int:
        players_to_remove = [player for player in self._players if position.lower() == player.position.lower()]
        for player in players_to_remove:
            self._players.remove(player)
        return len(players_to_remove)

    def search_by_team_size(self, team_size: int, offset=0, limit=None) -> List[Player]:
        result = [player for player in self._players if team_size == player.team_size]
        return result[offset:offset + limit] if limit else result

    def delete_by_team_size(self, team_size: int) -> int:
        players_to_remove = [player for player in self._players if team_size == player.team_size]
        for player in players_to_remove:
            self._players.remove(player)
        return len(players_to_remove)

    def search_by_football_team(self, football_team: str, offset=0, limit=None) -> List[Player]:
        result = [player for player in self._players if football_team.lower() == player.football_team.lower()]
        return result[offset:offset + limit] if limit else result

    def delete_by_football_team(self, football_team: str) -> int:
        players_to_remove = [player for player in self._players if
                             football_team.lower() == player.football_team.lower()]
        for player in players_to_remove:
            self._players.remove(player)
        return len(players_to_remove)

    def search_by_home_city(self, home_city: str, offset=0, limit=None) -> List[Player]:
        result = [player for player in self._players if home_city.lower() == player.home_city.lower()]
        return result[offset:offset + limit] if limit else result

    def delete_by_home_city(self, home_city: str) -> int:
        players_to_remove = [player for player in self._players if home_city.lower() == player.home_city.lower()]
        for player in players_to_remove:
            self._players.remove(player)
        return len(players_to_remove)
