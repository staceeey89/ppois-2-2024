import uuid


class Manufacturer:
    def __init__(self, id: uuid.UUID, name: str, UNP: int):
        self.__id = id
        self.__name = name
        self.__UNP = int(UNP)

    @property
    def name(self):
        return self.__name

    @property
    def id(self):
        return self.__id

    @property
    def UNP(self):
        return self.__UNP

    def __eq__(self, other):
        return self.__name == other.name and self.__UNP == other.UNP

