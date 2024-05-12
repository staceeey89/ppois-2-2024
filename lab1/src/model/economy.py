from src.model.infrastructure import Infrastructure
from src.model.citizen import Citizen


class Economy:
    def __init__(self, treasury: int = 0):
        self._infrastructure = Infrastructure()
        self._treasury = treasury

    @property
    def treasury(self):
        return self._treasury

    @property
    def infrastructure_level(self):
        return self._infrastructure.level

    def enhance_infrastructure(self):
        if self.treasury < self._infrastructure.get_cost_of_enhancing():
            raise AttributeError(f"Not enough money to enhance infrastructure. "
                                 f"You need {self._infrastructure.get_cost_of_enhancing()}")
        self._treasury -= self._infrastructure.get_cost_of_enhancing()
        self._infrastructure.enhance()

    def collect_taxes(self, citizen: Citizen):
        self._treasury += (citizen.income * self._infrastructure.level) // 20
