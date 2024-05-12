from src.model.citizen import Citizen


class Population:
    def __init__(self):
        self._citizens: list[Citizen] = []

    @property
    def citizens(self):
        return self._citizens

    def add_citizen(self, citizen: Citizen):
        self._citizens.append(citizen)

    def get_citizen(self, name: str):
        try:
            return list(filter(lambda x: x.name == name, self._citizens))[0]
        except IndexError:
            raise ValueError()

    def remove_citizen(self, citizen: Citizen):
        self._citizens.remove(citizen)
