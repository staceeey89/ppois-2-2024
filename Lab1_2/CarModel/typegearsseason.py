from enum import Enum

class TransmissionType(Enum):

    automatic = 0
    mechanical = 1

class Gears(Enum):

    N = 0
    R = 1
    G1 = 2
    G2 = 3
    G3 = 4
    G4 = 5

class Season(Enum):

    winter = 0
    summer = 1