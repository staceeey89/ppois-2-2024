from model.sportsman import Sportsman
from model.enums import Team, TypeOfSport, Category, FootballPosition, VolleyballPosition, BasketballPosition
from model.sportsman_dao import SportsmanRepositoryList, SportsmanRepositorySQL, SportsmanRepositoryXML
from model.exceptions import RepositoryException, ViewException


class Controller:
    def __init__(self, list_repository: SportsmanRepositoryList, db_repository: SportsmanRepositorySQL,
                 xml_repository: SportsmanRepositoryXML):
        self.__list_repository = list_repository
        self.__db_repository = db_repository
        self.__list_repository.set_list(self.__db_repository.get_all_sportsmen())
        self.__xml_repository = xml_repository
        self.__records_for_search = []

    def find_sportsman_by_name_or_sport(self, sportsman_name: str, type_of_sport: str) -> list[Sportsman]:
        self.__records_for_search = []
        if sportsman_name and type_of_sport:
            self.__records_for_search = self.__list_repository.get_sportsman_by_name_or_type_of_sport(sportsman_name,
                                                                                                      TypeOfSport(
                                                                                                          type_of_sport))
        elif sportsman_name:
            self.__records_for_search = self.__list_repository.get_sportsmen_by_name(sportsman_name)
        elif type_of_sport:
            self.__records_for_search = self.__list_repository.get_sportsmen_by_type_of_sport(TypeOfSport(type_of_sport))
        return self.__records_for_search

    def find_sportsman_by_titles(self, lower_bound: str, upper_bound: str) -> list[Sportsman]:
        self.__records_for_search = []
        if lower_bound.isdigit() and upper_bound.isdigit() and int(lower_bound) < int(upper_bound) and int(
                lower_bound) >= 0:
            self.__records_for_search = self.__list_repository.get_sportsman_by_number_of_titles(int(lower_bound), int(upper_bound))
            return self.__records_for_search
        else:
            raise ViewException("The lower bound and upper bound must be integers and upper bound must be greater " +
                                "than lower")

    def find_sportsman_by_name_or_category(self, name: str, category: str):
        self.__records_for_search = []
        if name and category:
            self.__records_for_search = self.__list_repository.get_sportsman_by_name_or_category(name, Category(category))
        elif name:
            self.__records_for_search = self.__list_repository.get_sportsmen_by_name(name)
        elif category:
            self.__records_for_search = self.__list_repository.get_sportsmen_by_category(Category(category))
        return self.__records_for_search

    def get_all_records_for_search(self):
        return self.__records_for_search

    def get_records_for_search_with_offset_and_limit(self, limit: int, offset: int) -> list[Sportsman]:
        result_records = []
        all_records = self.__records_for_search
        if limit * offset < len(all_records):
            for i in range(limit * offset, min(limit * (offset + 1), len(all_records))):
                result_records.append(all_records[i])
        return result_records

    def get_records_with_offset_and_limit(self, limit: int, offset: int) -> list[Sportsman]:
        result_records = []
        all_records = self.__list_repository.get_all_sportsmen()
        if limit * offset < len(all_records):
            for i in range(limit * offset, min(limit * (offset + 1), len(all_records))):
                result_records.append(all_records[i])
        return result_records

    def save_to_list(self, sportsman_name: str, team: str, position: str, titles: str, type_of_sport: str,
                     category: str):
        if not titles.isdigit() or int(titles) < 0:
            raise ViewException("Titles must be a positive integer or 0")

        if type_of_sport == TypeOfSport.FOOTBALL.value:
            sportsman_position = FootballPosition(position)
        elif type_of_sport == TypeOfSport.BASKETBALL.value:
            sportsman_position = BasketballPosition(position)
        else:
            sportsman_position = VolleyballPosition(position)
        sportsman_entity = Sportsman(sportsman_name, Team(team), sportsman_position, int(titles),
                                     TypeOfSport(type_of_sport),
                                     Category(category))
        self.__list_repository.add_sportsman(sportsman_entity)

    def save_to_database(self, sportsman_name: str, team: str, position: str, titles: str, type_of_sport: str,
                         category: str):
        if not titles.isdigit() or int(titles) < 0:
            raise ViewException("Titles must be a positive integer or 0")

        if type_of_sport == TypeOfSport.FOOTBALL.value:
            sportsman_position = FootballPosition(position)
        elif type_of_sport == TypeOfSport.BASKETBALL.value:
            sportsman_position = BasketballPosition(position)
        else:
            sportsman_position = VolleyballPosition(position)
        sportsman_entity = Sportsman(sportsman_name, Team(team), sportsman_position, int(titles),
                                     TypeOfSport(type_of_sport),
                                     Category(category))
        try:
            self.__db_repository.add_sportsman(sportsman_entity)
        except RepositoryException:
            raise ViewException("Problems occurred while connecting to database")

    def save_to_xml(self, sportsman_name: str, team: str, position: str, titles: str, type_of_sport: str, category: str,
                    filename: str):
        if not titles.isdigit() or int(titles) < 0:
            raise ViewException("Titles must be a positive integer or 0")

        if type_of_sport == TypeOfSport.FOOTBALL.value:
            sportsman_position = FootballPosition(position)
        elif type_of_sport == TypeOfSport.BASKETBALL.value:
            sportsman_position = BasketballPosition(position)
        else:
            sportsman_position = VolleyballPosition(position)
        sportsman_entity = Sportsman(sportsman_name, Team(team), sportsman_position, int(titles),
                                     TypeOfSport(type_of_sport),
                                     Category(category))
        sportsman_list: list[Sportsman] = [sportsman_entity]
        try:
            self.__xml_repository.write_to_xml(sportsman_list, filename)
        except RepositoryException:
            raise ViewException("Problems occurred while writing to file")

    def delete_records_by_name_or_sport(self, name: str, sport: str):
        if name and sport:
            i = self.__list_repository.delete_sportsmen_by_name(name)
            j = self.__list_repository.delete_sportsmen_by_type_of_sport(TypeOfSport(sport))
            return i + j
        elif name:
            return self.__list_repository.delete_sportsmen_by_name(name)
        elif sport:
            return self.__list_repository.delete_sportsmen_by_type_of_sport(TypeOfSport(sport))

    def delete_records_by_titles(self, lower_bound: str, upper_bound: str):
        if lower_bound.isdigit() and upper_bound.isdigit() and int(lower_bound) < int(upper_bound) and int(
                lower_bound) >= 0:
            return self.__list_repository.delete_sportsmen_by_number_of_titles(int(lower_bound), int(upper_bound))

    def delete_records_by_name_or_category(self, name: str, category: str):
        if name and category:
            i = self.__list_repository.delete_sportsmen_by_name(name)
            j = self.__list_repository.delete_sportsmen_by_category(Category(category))
            return i + j
        elif name:
            return self.__list_repository.delete_sportsmen_by_name(name)
        elif category:
            return self.__list_repository.delete_sportsmen_by_category(Category(category))

    def set_list_from_database(self):
        self.__list_repository.set_list(self.__db_repository.get_all_sportsmen())

    def set_list_from_xml(self, filename):
        self.__list_repository.set_list(self.__xml_repository.get_all_from_xml(filename))

    def get_all_records(self):
        return self.__list_repository.get_all_sportsmen()
