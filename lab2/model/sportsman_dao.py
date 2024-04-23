import psycopg2

from util.connection_manager import ConnectionManager
from abc import ABCMeta, abstractmethod
from entity.sportsman import Sportsman
from enums.category import Category
from enums.type_of_sport import TypeOfSport


class SportsmanRepositoryInterface(ABCMeta):

    @abstractmethod
    def add_sportsmen(self, sportsman: Sportsman):
        """add sportsman to the repository"""

    @abstractmethod
    def delete_sportsmen_by_name(self, sportsmen_name: str) -> int:
        """delete sportsmen by name"""

    @abstractmethod
    def delete_sportsmen_by_number_of_titles(self, number_of_titles: int) -> int:
        """delete sportsmen by number of titles"""

    @abstractmethod
    def delete_sportsmen_by_type_of_sport(self, type_of_sport: TypeOfSport) -> int:
        """delete sportsmen by type of sport"""

    @abstractmethod
    def delete_sportsmen_by_category(self, sportsmen_category: Category) -> int:
        """delete sportsmen by category"""

    @abstractmethod
    def get_sportsmen_by_type_of_sport(self, type_of_sport: TypeOfSport) -> list[Sportsman]:
        """return sportsmen by type of sport"""

    @abstractmethod
    def get_sportsmen_by_name(self, sportsmen_name: str) -> list[Sportsman]:
        """return sportsmen by name"""

    @abstractmethod
    def get_sportsmen_by_number_of_titles(self, number_of_titles: int) -> list[Sportsman]:
        """return sportsmen by number of titles"""

    @abstractmethod
    def get_sportsmen_by_category(self, sportsmen_category: Category) -> list[Sportsman]:
        """return all sportsmen by category"""


class SportsmanRepositorySQL(SportsmanRepositoryInterface):
    ADD_SPORTSMAN_SQL = """INSERT INTO sportsman(name, team, position, category, titles, type_of_sport, category)
    VALUES (?, ?, ?, ?, ?, ?, ?);"""

    def add_sportsmen(self, sportsman: Sportsman):
        with ConnectionManager.open() as connection, \
                connection.cursor() as cursor:
            try:
                cursor.execute(SportsmanRepositorySQL.ADD_SPORTSMAN_SQL, (sportsman.name,
                                                                          sportsman.team.value,
                                                                          sportsman.position.value,
                                                                          sportsman.category.value,
                                                                          sportsman.titles,
                                                                          sportsman.type_of_sport.value,
                                                                          sportsman.category.value))
                connection.commit()

            except psycopg2.Error as e:
                connection.rollback()

    def delete_sportsmen_by_name(self, sportsmen_name: str) -> int:
        pass

    def delete_sportsmen_by_number_of_titles(self, number_of_titles: int) -> int:
        pass

    def delete_sportsmen_by_type_of_sport(self, type_of_sport: TypeOfSport) -> int:
        pass

    def delete_sportsmen_by_category(self, sportsmen_category: Category) -> int:
        pass

    def get_sportsmen_by_type_of_sport(self, type_of_sport: TypeOfSport) -> list[Sportsman]:
        pass

    def get_sportsmen_by_name(self, sportsmen_name: str) -> list[Sportsman]:
        pass

    def get_sportsmen_by_number_of_titles(self, number_of_titles: int) -> list[Sportsman]:
        pass

    def get_sportsmen_by_category(self, sportsmen_category: Category) -> list[Sportsman]:
        pass
