from core.db_interface import DBInterface
from core.my_sql_handler import MySQLHandler
from core.player import Player
from core.xml_handler import XMLHandler


class PlayersList:
    def __init__(self):
        self.players = []
        self.db_handler: DBInterface = MySQLHandler()

    def switch_db_to_xml(self, file_path):
        self.db_handler = XMLHandler(file_path)

    def switch_db_to_sql(self):
        self.db_handler = MySQLHandler()

    def get_players_count(self, criteria=None):
        players_count = self.db_handler.get_players_count(criteria=criteria)
        return players_count

    def fetch_players_from_db(self, limit=None, offset=0, search_criteria=None):
        if search_criteria is None:
            search_criteria = {}
        players = self.db_handler.search_players(criteria=search_criteria, limit=limit, offset=offset)

        if players:
            self.players = players
            return players
        else:
            self.players = None

    def delete_player(self, search_criteria):
        deleted_players_count = self.db_handler.delete_players(search_criteria)
        return deleted_players_count

    def add_player(self, full_name, birth_date, football_team, home_city, squad, position):
        player = Player(full_name, birth_date, football_team, home_city, squad, position)
        self.db_handler.add_player(player)
