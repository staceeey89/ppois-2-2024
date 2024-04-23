from enum import Enum
from model.enums import Team, TypeOfSport, Category


class Sportsman:

    def __init__(self, name: str, team: Team, position: Enum, titles: int, type_of_sport: TypeOfSport,
                 category: Category):
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

    def __eq__(self, other):
        if isinstance(other, Sportsman):
            return (self.__name == other.__name and self.__team == other.__team and self.__position == other.__position
                    and self.__titles == other.__titles and self.__type_of_sport == other.__type_of_sport
                    and self.__category == other.__category)
        return False
