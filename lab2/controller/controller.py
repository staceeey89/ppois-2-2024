from model.sportsman import Sportsman
from model.exceptions import RepositoryException
from model.enums import Team, TypeOfSport, Category, FootballPosition, VolleyballPosition, BasketballPosition
from model.sportsman_dao import SportsmanRepositoryList, SportsmanRepositorySQL, SportsmanRepositoryXML


class Contoller:
    def __init__(self, list_repository: SportsmanRepositoryList, db_repository: SportsmanRepositorySQL,
                 xml_repository: SportsmanRepositoryXML):
        self.list_repository = list_repository
        self.db_repository = db_repository
        self.xml_repository = xml_repository