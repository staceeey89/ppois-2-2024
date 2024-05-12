from abc import ABC, abstractmethod


class DBInterface(ABC):
    @abstractmethod
    def add_player(self, player):
        raise NotImplementedError("Add player method must be implemented")

    @abstractmethod
    def search_players(self, criteria, offset=None, limit=None):
        raise NotImplementedError("Search players method must be implemented")

    @abstractmethod
    def get_players_count(self, criteria=None):
        raise NotImplementedError("Get players count method must be implemented")

    @abstractmethod
    def delete_players(self, criteria):
        raise NotImplementedError("Delete player method must be implemented")
