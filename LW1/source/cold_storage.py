from typing import List

from fish import FishState, Fish


class ColdStorage:
    def __init__(self, name: str, fish_from_fishing: List[Fish], fish_after_processing: List[Fish],
                 frozen_fish: List[Fish]) -> None:
        self.name = name
        self.fish_from_fishing = fish_from_fishing
        self.fish_after_processing = fish_after_processing
        self.frozen_fish = frozen_fish

    def store_fish(self, fishes: List[Fish]) -> None:
        print(f"Рыба доставлена в хладокомбинат {self.name}")
        for fish in fishes:
            fish.state = FishState.TRANSPORTED
        self.fish_from_fishing.extend(fishes)

    def process_fish(self) -> None:
        if self.fish_from_fishing:
            print(f"Обработка рыбы в хладокомбинате {self.name}:")
            for fish in self.fish_from_fishing:
                print(f"Обработка рыбы: {str(fish)}")
                fish.state = FishState.PROCESSED
                self.fish_after_processing.append(fish)
            print("Обработка завершена.")
            self.fish_from_fishing.clear()
        else:
            print(f"В хладокомбинате {self.name} нет рыбы для обработки.")

    def freeze_fish(self, target_weight: int) -> None:
        total_weight = 0

        for fish in self.fish_after_processing.copy():
            if total_weight + fish.weight >= target_weight:
                break

            fish.state = FishState.FROZEN
            self.frozen_fish.append(fish)
            total_weight += fish.weight
            self.fish_after_processing.remove(fish)

    def sell_fish_to_market(self, weight_limit: int) -> List[Fish]:
        total_weight = 0
        fish_to_sell = []
        for fish in self.fish_after_processing + self.frozen_fish:
            if total_weight + fish.weight <= weight_limit:
                fish_to_sell.append(fish)
                total_weight += fish.weight
            else:
                break
        if fish_to_sell:
            print(f"Передача рыбы на рынок из хладокомбината {self.name}:")
            for fish in fish_to_sell:
                fish.state = FishState.FOR_SALE
                print(f"Рыба для продажи на рынке: {str(fish)}")
            print("Рыба успешно передана на рынок.")
            for fish in fish_to_sell:
                self.fish_after_processing.remove(fish)
            return fish_to_sell
        else:
            print(f"В хладокомбинате {self.name} нет рыбы для передачи на рынок.")

    def calculate_weight(self, is_for_selling: bool) -> int:
        if is_for_selling:
            frozen_weight = sum(fish.weight for fish in self.frozen_fish)
        else:
            frozen_weight = 0
        processed_weight = sum(fish.weight for fish in self.fish_after_processing)
        total_weight = frozen_weight + processed_weight
        return total_weight

    def to_dict(self) -> dict:
        data = {
            'name': self.name,
            'fish_from_fishing': [fish.to_dict() for fish in self.fish_from_fishing],
            'fish_after_processing': [fish.to_dict() for fish in self.fish_after_processing],
            'frozen_fish': [fish.to_dict() for fish in self.frozen_fish]
        }
        return data
