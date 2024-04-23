import enum


class VolleyballPosition(enum.Enum):

    BINDER = "BINDER"
    DIAGONAL = "DIAGONAL"
    FINISHER = "FINISHER"
    CENTRAL = "CENTRAL"
    LIBERO = "LIBERO"


class FootballPosition(enum.Enum):

    DEFENDER = "DEFENDER"
    MIDFIELDER = "MIDFIELDER"
    FORWARD = "FORWARD"
    GOALKEEPER = "GOALKEEPER"


class BasketballPosition(enum.Enum):

    DEFENDER = "DEFENDER"
    CENTRAL = "CENTRAL"
    FORWARD = "FORWARD"


class Category(enum.Enum):

    FIRST = "1st junior"
    SECOND = "2nd class"
    THIRD = "3rd class"
    CANDIDATE_MASTER = "candidate master"
    MASTER_OF_SPORTS = "master of sports"


class Team(enum.Enum):
    MAIN = "MAIN"
    RESERVE = "RESERVE"
    NA = "n/a"


class TypeOfSport(enum.Enum):

    FOOTBALL = "FOOTBALL"
    VOLLEYBALL = "VOLLEYBALL"
    BASKETBALL = "BASKETBALL"
