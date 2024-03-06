import json
import random
from enum import Enum


class FishState(Enum):
    CAUGHT = 1
    PROCESSED = 2
    TRANSPORTED = 3
    FROZEN = 4
    FOR_SALE = 5


class Fish:
    fish_species = ["karp", "pike", "trout", "salmon", "bass"]

    def __init__(self, weight: int, species: str, state: FishState) -> None:
        self.weight = weight
        self.species = species
        self.state: FishState = state

    def __str__(self) -> str:
        return f"{self.species} : {str(self.weight)} кг"

    def to_dict(self) -> dict:
        return {
            'species': self.species,
            'weight': self.weight,
            'state': self.state.name
        }
