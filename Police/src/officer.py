import datetime
from enum import Enum


class Rank(Enum):
    CONSTABLE = 1
    SERGEANT = 2
    LIEUTENANT = 3
    CAPTAIN = 4
    INSPECTOR = 5
    CHIEF_INSPECTOR = 6
    SUPERINTENDENT = 7
    DEPUTY_CHIEF = 8
    CHIEF = 9

    @classmethod
    def from_string(cls, policerank: str):
        return {
            "Constable": cls.CONSTABLE,
            "Sergeant": cls.SERGEANT,
            "Lieutenant": cls.LIEUTENANT,
            "Captain": cls.CAPTAIN,
            "Inspector": cls.INSPECTOR,
            "Chief Inspector": cls.CHIEF_INSPECTOR,
            "Superintendent": cls.SUPERINTENDENT,
            "Deputy Chief": cls.DEPUTY_CHIEF,
            "Chief": cls.CHIEF
        }.get(policerank)

    def __str__(self):
        return {
            self.CONSTABLE: "Constable",
            self.SERGEANT: "Sergeant",
            self.LIEUTENANT: "Lieutenant",
            self.CAPTAIN: "Captain",
            self.INSPECTOR: "Inspector",
            self.CHIEF_INSPECTOR: "Chief Inspector",
            self.SUPERINTENDENT: "Superintendent",
            self.DEPUTY_CHIEF: "Deputy Chief",
            self.CHIEF: "Chief"
        }.get(self)


class Position(Enum):
    PATROL = 1
    DETECTIVE = 2

    @classmethod
    def from_string(cls, position: str):
        return {
            "Detective": cls.DETECTIVE,
            "Patrol Officer": cls.PATROL
        }[position]


class Officer:
    def __init__(self, fullname: str, rank: Rank, experience: int, unavailable_until: datetime.datetime):
        self.name = fullname
        self.rank = rank
        self.experience = experience
        self.unavailable_until = unavailable_until

    def __str__(self):
        return "{:<10} {:<20} {:<20} {:<10} {:<10}".format("  Officer        ",
                                                           self.name,
                                                           str(self.rank),
                                                           f"★{str(self.experience)}",
                                                           str(self.unavailable_until)
                                                           )


class Detective(Officer):
    def __str__(self):
        return "{:<10} {:<20} {:<20} {:<10} {:<10}".format("🕵️Detective      ",
                                                           self.name,
                                                           str(self.rank),
                                                           f"★{str(self.experience)}",
                                                           str(self.unavailable_until)
                                                           )


class PatrolOfficer(Officer):
    def __str__(self):
        return "{:<10} {:<20} {:<20} {:<10} {:<10}".format("👮Patrol Officer ",
                                                           self.name,
                                                           str(self.rank),
                                                           f"★{str(self.experience)}",
                                                           str(self.unavailable_until)
                                                           )


class OfficerGenerator:
    def __new__(cls, fullname: str, position: Position, rank: Rank, experience: int, unavail_until: datetime.datetime):
        if position == Position.DETECTIVE:
            return Detective(fullname, rank, experience, unavail_until)
        elif position == Position.PATROL:
            return PatrolOfficer(fullname, rank, experience, unavail_until)
        else:
            return Officer(fullname, rank, experience, unavail_until)
