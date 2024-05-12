import psycopg2
import xml.dom.minidom
import xml.sax

from util.connection_manager import ConnectionManager
from abc import ABCMeta, abstractmethod
from model.sportsman import Sportsman
from model.enums import Category
from model.enums import TypeOfSport
from model.enums import Team
from model.enums import FootballPosition, VolleyballPosition, BasketballPosition
from model.exceptions import RepositoryException


class SportsmanRepositoryInterface(metaclass=ABCMeta):

    @abstractmethod
    def add_sportsman(self, sportsman: Sportsman):
        """add sportsman to the repository"""

    @abstractmethod
    def delete_sportsmen_by_name(self, sportsmen_name: str) -> int:
        """delete sportsmen by name"""

    @abstractmethod
    def delete_sportsmen_by_number_of_titles(self, lower_bound: int, upper_bound: int) -> int:
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
    def get_sportsmen_by_name(self, sportsman_name: str) -> list[Sportsman]:
        """return sportsmen by name"""

    @abstractmethod
    def get_sportsmen_by_number_of_titles(self, number_of_titles: int) -> list[Sportsman]:
        """return sportsmen by number of titles"""

    @abstractmethod
    def get_sportsmen_by_category(self, sportsmen_category: Category) -> list[Sportsman]:
        """return all sportsmen by category"""

    @abstractmethod
    def get_all_sportsmen(self):
        """return all sportsmen"""


class SportsmanRepositorySQL:
    ADD_SPORTSMAN_SQL = """INSERT INTO sportsman(name, team, position, titles, type_of_sport, category)
    VALUES ( %s, %s, %s, %s, %s, %s);"""

    DELETE_SPORTSMAN_SQL = """DELETE FROM sportsman
    WHERE %s = %s;"""

    FIND_SPORTSMEN_SQL = """SELECT name, team, position, titles, type_of_sport, category FROM sportsman
    WHERE %s = %s"""

    def add_sportsman(self, sportsman: Sportsman):
        with ConnectionManager.open() as connection, \
                connection.cursor() as cursor:
            try:
                cursor.execute(SportsmanRepositorySQL.ADD_SPORTSMAN_SQL, (sportsman.name,
                                                                          sportsman.team.value,
                                                                          sportsman.position.value,
                                                                          sportsman.titles,
                                                                          sportsman.type_of_sport.value,
                                                                          sportsman.category.value))
                connection.commit()
            except psycopg2.Error:
                connection.rollback()
                raise RepositoryException("Troubles while updating database")

    @staticmethod
    def __delete_sportsman_by_attribute(attribute_name: str, attribute_value) -> int:
        with ConnectionManager.open() as connection, \
                connection.cursor() as cursor:
            try:
                cursor.execute(
                    SportsmanRepositorySQL.DELETE_SPORTSMAN_SQL % (attribute_name, "'" + attribute_value + "'"))
                rowcount = cursor.rowcount
                connection.commit()
                return rowcount
            except psycopg2.Error:
                connection.rollback()
                raise RepositoryException("Troubles while updating database")

    @staticmethod
    def __get_sportsmen_by_attribute(attribute_name: str, attribute_value) -> list[Sportsman]:
        sportsmen_list = []
        with ConnectionManager.open() as connection, \
                connection.cursor() as cursor:
            try:
                cursor.execute(
                    SportsmanRepositorySQL.FIND_SPORTSMEN_SQL % (attribute_name, "'" + attribute_value + "'"))

                for row in cursor.fetchall():
                    name, team, position, titles, type_of_sport, category = row
                    if type_of_sport == TypeOfSport.FOOTBALL.value:
                        sportsman_position = FootballPosition(position)
                    elif type_of_sport == TypeOfSport.BASKETBALL.value:
                        sportsman_position = BasketballPosition(position)
                    else:
                        sportsman_position = VolleyballPosition(position)
                    sportsman_entity = Sportsman(name, Team(team), sportsman_position, titles,
                                                 TypeOfSport(type_of_sport),
                                                 Category(category))
                    sportsmen_list.append(sportsman_entity)

                return sportsmen_list
            except (psycopg2.Error, KeyError):
                raise RepositoryException("Troubles while reading from database")

    def delete_sportsmen_by_name(self, sportsmen_name: str) -> int:
        return self.__delete_sportsman_by_attribute("name", sportsmen_name)

    def delete_sportsmen_by_number_of_titles(self, number_of_titles: int) -> int:
        return self.__delete_sportsman_by_attribute("titles", number_of_titles)

    def delete_sportsmen_by_type_of_sport(self, type_of_sport: TypeOfSport) -> int:
        return self.__delete_sportsman_by_attribute("type_of_sport", type_of_sport.value)

    def delete_sportsmen_by_category(self, sportsmen_category: Category) -> int:
        return self.__delete_sportsman_by_attribute("category", sportsmen_category.value)

    def get_sportsmen_by_type_of_sport(self, type_of_sport: TypeOfSport) -> list[Sportsman]:
        return self.__get_sportsmen_by_attribute("type_of_sport", type_of_sport.value)

    def get_sportsmen_by_name(self, sportsman_name: str) -> list[Sportsman]:
        return self.__get_sportsmen_by_attribute("name", sportsman_name)

    def get_sportsmen_by_number_of_titles(self, number_of_titles: int) -> list[Sportsman]:
        return self.__get_sportsmen_by_attribute("titles", number_of_titles)

    def get_sportsmen_by_category(self, sportsmen_category: Category) -> list[Sportsman]:
        return self.__get_sportsmen_by_attribute("titles", sportsmen_category.value)

    def get_all_sportsmen(self) -> list[Sportsman]:
        sportsmen_list = []
        with ConnectionManager.open() as connection, \
                connection.cursor() as cursor:
            try:
                cursor.execute("""SELECT * FROM sportsman""")

                for row in cursor.fetchall():
                    sportsman_id, name, team, position, titles, type_of_sport, category = row
                    if type_of_sport == TypeOfSport.FOOTBALL.value:
                        sportsman_position = FootballPosition(position)
                    elif type_of_sport == TypeOfSport.BASKETBALL.value:
                        sportsman_position = BasketballPosition(position)
                    else:
                        sportsman_position = VolleyballPosition(position)
                    sportsman_entity = Sportsman(name, Team(team), sportsman_position, titles,
                                                 TypeOfSport(type_of_sport),
                                                 Category(category))
                    sportsmen_list.append(sportsman_entity)

                return sportsmen_list
            except (psycopg2.Error, KeyError):
                raise RepositoryException("Troubles while reading from database")


class SportsmanRepositoryList(SportsmanRepositoryInterface):

    def __init__(self):
        self.__sportsmen_list: list[Sportsman] = []

    def add_sportsman(self, sportsman: Sportsman):
        self.__sportsmen_list.append(sportsman)

    def delete_sportsmen_by_name(self, sportsmen_name: str) -> int:
        rowcount = 0
        records_copy = self.__sportsmen_list[:]
        for sportsman in records_copy:
            if sportsman.name == sportsmen_name:
                rowcount += 1
                self.__sportsmen_list.remove(sportsman)
        return rowcount

    def delete_sportsmen_by_number_of_titles(self, lower_bound: int, upper_bound: int) -> int:
        rowcount = 0
        records_copy = self.__sportsmen_list[:]
        for sportsman in records_copy:
            if lower_bound <= sportsman.titles <= upper_bound:
                rowcount += 1
                self.__sportsmen_list.remove(sportsman)
        return rowcount

    def delete_sportsmen_by_type_of_sport(self, type_of_sport: TypeOfSport) -> int:
        rowcount = 0
        records_copy = self.__sportsmen_list[:]
        for sportsman in records_copy:
            if sportsman.type_of_sport == type_of_sport:
                rowcount += 1
                self.__sportsmen_list.remove(sportsman)
        return rowcount

    def delete_sportsmen_by_category(self, sportsmen_category: Category) -> int:
        rowcount = 0
        records_copy = self.__sportsmen_list[:]
        for sportsman in records_copy:
            if sportsman.category == sportsmen_category:
                rowcount += 1
                self.__sportsmen_list.remove(sportsman)
        return rowcount

    def get_sportsmen_by_type_of_sport(self, type_of_sport: TypeOfSport) -> list[Sportsman]:
        found_sportsmen_list: list[Sportsman] = []
        for sportsman in self.__sportsmen_list:
            if sportsman.type_of_sport == type_of_sport:
                found_sportsmen_list.append(sportsman)
        return found_sportsmen_list

    def get_sportsmen_by_name(self, sportsman_name: str) -> list[Sportsman]:
        found_sportsmen_list: list[Sportsman] = []
        for sportsman in self.__sportsmen_list:
            if sportsman.name == sportsman_name:
                found_sportsmen_list.append(sportsman)
        return found_sportsmen_list

    def get_sportsmen_by_number_of_titles(self, number_of_titles: int) -> list[Sportsman]:
        found_sportsmen_list: list[Sportsman] = []
        for sportsman in self.__sportsmen_list:
            if sportsman.titles == number_of_titles:
                found_sportsmen_list.append(sportsman)
        return found_sportsmen_list

    def get_sportsmen_by_category(self, sportsmen_category: Category) -> list[Sportsman]:
        found_sportsmen_list: list[Sportsman] = []
        for sportsman in self.__sportsmen_list:
            if sportsman.category == sportsmen_category:
                found_sportsmen_list.append(sportsman)
        return found_sportsmen_list

    def get_all_sportsmen(self) -> list[Sportsman]:
        return self.__sportsmen_list

    def set_list(self, sportsmen_list: list[Sportsman]):
        self.__sportsmen_list = sportsmen_list

    def get_sportsman_by_name_or_type_of_sport(self, sportsman_name: str, type_of_sport: TypeOfSport) -> list[Sportsman]:
        found_sportsmen_list: list[Sportsman] = []
        for sportsman in self.__sportsmen_list:
            if sportsman.name == sportsman_name or sportsman.type_of_sport == type_of_sport:
                found_sportsmen_list.append(sportsman)
        return found_sportsmen_list

    def get_sportsman_by_number_of_titles(self, low_limit: int, high_limit: int):
        found_sportsmen_list: list[Sportsman] = []
        for sportsman in self.__sportsmen_list:
            if low_limit <= sportsman.titles <= high_limit:
                found_sportsmen_list.append(sportsman)
        return found_sportsmen_list

    def get_sportsman_by_name_or_category(self, sportsman_name: str, sportsman_category: Category):
        found_sportsmen_list: list[Sportsman] = []
        for sportsman in self.__sportsmen_list:
            if sportsman.name == sportsman_name or sportsman.category == sportsman_category:
                found_sportsmen_list.append(sportsman)
        return found_sportsmen_list


class SportsmanRecordHandler(xml.sax.ContentHandler):
    def __init__(self):
        self.records = []
        self.current_data = ""
        self.sportsman_name = ""
        self.team = ""
        self.position = ""
        self.titles = ""
        self.type_of_sport = ""
        self.category = ""

    def startElement(self, tag, attributes):
        self.current_data = tag

    def endElement(self, tag):
        if tag == "sportsman_record":
            self.sportsman_name = self.sportsman_name.strip()
            self.team = self.team.strip()
            self.position = self.position.strip()
            self.titles = self.titles.strip()
            self.type_of_sport = self.type_of_sport.strip()
            self.category = self.category.strip()

            if self.type_of_sport == TypeOfSport.FOOTBALL.value:
                sportsman_position = FootballPosition(self.position)
            elif self.type_of_sport == TypeOfSport.BASKETBALL.value:
                sportsman_position = BasketballPosition(self.position)
            else:
                sportsman_position = VolleyballPosition(self.position)

            self.records.append(
                Sportsman(self.sportsman_name, Team(self.team), sportsman_position, int(self.titles),
                          TypeOfSport(self.type_of_sport),
                          Category(self.category)))
            self.sportsman_name = ""
            self.team = ""
            self.position = ""
            self.titles = ""
            self.type_of_sport = ""
            self.category = ""

    def characters(self, content):
        if self.current_data == "sportsman_name":
            self.sportsman_name += content
        elif self.current_data == "team":
            self.team += content
        elif self.current_data == "position":
            self.position += content
        elif self.current_data == "titles":
            self.titles += content
        elif self.current_data == "type_of_sport":
            self.type_of_sport += content
        elif self.current_data == "category":
            self.category += content


class SportsmanRepositoryXML:
    def write_to_xml(self, sportsmen_list: list[Sportsman], filename: str):
        try:
            doc = xml.dom.minidom.parse(filename)
            root = doc.documentElement
        except FileNotFoundError:
            doc = xml.dom.minidom.Document()
            root = doc.createElement("sportsmen_records")
            doc.appendChild(root)

        for record in sportsmen_list:
            record_element = doc.createElement("sportsman_record")
            root.appendChild(record_element)

            self.add_text_element(doc, record_element, "sportsman_name", record.name)
            self.add_text_element(doc, record_element, "team", record.team.value)
            self.add_text_element(doc, record_element, "position", record.position.value)
            self.add_text_element(doc, record_element, "titles", str(record.titles))
            self.add_text_element(doc, record_element, "type_of_sport", record.type_of_sport.value)
            self.add_text_element(doc, record_element, "category", record.category.value)

        with open(filename, "w") as file:
            file.write(doc.toprettyxml(indent='', newl=''))

    @staticmethod
    def add_text_element(doc, parent, tag, text):
        element = doc.createElement(tag)
        element.appendChild(doc.createTextNode(text))
        parent.appendChild(element)

    @staticmethod
    def get_all_from_xml(filename: str) -> list[Sportsman]:
        handler = SportsmanRecordHandler()
        parser = xml.sax.make_parser()
        parser.setContentHandler(handler)
        parser.parse(filename)
        return handler.records
