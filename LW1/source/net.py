from datetime import datetime, timedelta
from typing import List
from typing import Optional
import random

from fish import Fish, FishState
from util.logger_util import LoggerUtil


class Net:
    def __init__(self, square: int) -> None:
        self.caught_fish: List[Fish] = []
        self.square: int = square
        self.cast_time: datetime = None
        self.caught_time: datetime = None
        self.logger = LoggerUtil.setup_logger(str(square), '../logs/fishing.log')

    # бросок сети
    def cast(self) -> None:
        self.cast_time = datetime.now()
        formatted_cast_time = self.cast_time.strftime("%H:%M:%S")
        self.logger.info(f"Сеть брошена в {formatted_cast_time}")
        self.caught_time = self.cast_time + timedelta(seconds=self.square * 2)
        formatted_caught_time = self.caught_time.strftime("%H:%M:%S")
        self.logger.info(f"Улов стоит ждать в {formatted_caught_time}")

    # поднятие сети
    def retrieve(self) -> bool:
        if self.cast_time is not None:
            if datetime.now() > self.caught_time:
                count_of_fish = random.randint(1, int((self.square + 1) / 2))
                self.caught_fish = []
                for i in range(count_of_fish):
                    fish = Fish(weight=random.randint(1, 10), species=random.choice(Fish.fish_species),
                                state=FishState.CAUGHT)
                    self.caught_fish.append(fish)
                self.logger.info("Сеть была поднята")
                return True
            else:
                self.logger.info(f"Улова еще нет, требуется подождать {(self.caught_time - datetime.now())}")
        else:
            self.logger.info("Cеть не была сброшена")
        return False

    # возвращениe сети
    def store(self) -> List[Fish]:
        if self.caught_fish is not None:
            self.logger.info("Улов, полученный из сети:")
            for fish in self.caught_fish:
                self.logger.info(fish)
            return self.caught_fish

    def display_caught_fish(self) -> None:
        print("Улов, полученный из сети:")
        for fish in self.caught_fish:
            print(fish)

    def __str__(self) -> str:
        return f"Сеть площадью {self.square}"

    def to_dict(self) -> dict:
        return {
            'square': self.square,
            'cast_time': self.cast_time.isoformat() if self.cast_time else None
        }

    def set_time(self, cast_time: datetime) -> None:
        self.cast_time = cast_time
        self.caught_time = self.cast_time + timedelta(seconds=self.square * 2)
