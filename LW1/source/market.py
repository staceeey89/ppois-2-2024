import random
import threading
import time
from typing import List

from cold_storage import ColdStorage
from fish import Fish
from util.logger_util import LoggerUtil


# Настройка логгирования

class Market:
    def __init__(self, name: str, fish_on_market: List[Fish]) -> None:
        self.name = name
        self.fish_on_market = fish_on_market
        self.market_event = threading.Event()
        self.logger = LoggerUtil.setup_logger("market", '../logs/market.log')

    def receive_fish_from_storage(self, cold_storage: ColdStorage, fish_for_selling: List[Fish]) -> None:
        if fish_for_selling:
            self.logger.info(f"Получение рыбы на рынок {self.name} из хладокомбината {cold_storage.name}:")
            for fish in fish_for_selling:
                self.logger.info(f"Рыба для продажи на рынке: {str(fish)}")
                self.fish_on_market.append(fish)
            self.logger.info("Рыба успешно получена на рынке.")

    def sell_fish(self) -> None:
        while not self.market_event.is_set():
            num_fish_to_sell = random.randint(1, 5)

            sold_fish = []
            for fish in self.fish_on_market:
                if len(sold_fish) < num_fish_to_sell:
                    sold_fish.append(fish)
                else:
                    break
            if sold_fish:
                self.logger.info(f"Продажа рыбы на рынке {self.name}:")
                for fish in sold_fish:
                    self.logger.info(f"Продана рыба: {str(fish)}")
                self.logger.info("Рыба успешно продана на рынке.")
                self.fish_on_market = [fish for fish in self.fish_on_market if fish not in sold_fish]
            else:
                self.logger.info(f"На рынке {self.name} нет рыбы для продажи или превышен лимит веса.")

            time.sleep(5)

    def to_dict(self) -> dict:
        data = {
            'name': self.name,
            'fish_on_market': [fish.to_dict() for fish in self.fish_on_market],
            'market_event_is_set': self.market_event.is_set()  # преобразовываем в булево значение
        }
        return data
