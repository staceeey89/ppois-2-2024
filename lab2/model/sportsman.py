from enum import Enum
from enums.position import BasketballPosition, VolleyballPosition, FootballPosition
from enums.team import Team
from enums.type_of_sport import TypeOfSport
from enums.category import Category


class Sportsman:

    def __init__(self, name: str, team: Team, position: Enum, titles: int, type_of_sport: TypeOfSport, category: Category):
        self.__name = name
        self.__team = team
        self.__position = position
        self.__titles = titles
        self.__type_of_sport = type_of_sport
        self.__category = category

    @property
    def name(self):
        return self.__name

    @property
    def team(self):
        return self.__team

    @property
    def position(self):
        return self.__position

    @property
    def titles(self):
        return self.__titles

    @property
    def type_of_sport(self):
        return self.__type_of_sport

    @property
    def category(self):
        return self.__category
