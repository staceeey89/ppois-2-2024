import random
from enum import Enum
from typing import List

from fish import Fish, FishState
from util.logger_util import LoggerUtil


class Experience(Enum):
    BEGINNER = 2
    INTERMEDIATE = 4
    ADVANCED = 7
    EXPERT = 10


class Fisherman:

    def __init__(self, name: str, experience: Experience) -> None:
        self.name = name
        self.experience = experience
        self.logger = LoggerUtil.setup_logger(name, '../logs/fishing.log')

    def catch_fish(self) -> List[Fish]:
        caught_fish = []
        count_of_fish = random.randint(1, self.experience.value)
        for i in range(count_of_fish):
            fish = Fish(weight=random.randint(1, 10), species=random.choice(Fish.fish_species), state=FishState.CAUGHT)
            caught_fish.append(fish)
            self.logger.info(f"{self.name} поймал рыбу: {fish.species} весом {fish.weight} кг.")
        return caught_fish

    def display_caught_fish(self) -> None:
        for fish in self.catch_fish():
            print(f"{self.name} поймал рыбу: {fish.species} весом {fish.weight} кг.")

    def __str__(self) -> str:
        return f"Рыбак {self.name}, опыт - {str(self.experience.name)}"

    def to_dict(self) -> dict:
        return {
            'name': self.name,
            'experience': self.experience.name
        }
