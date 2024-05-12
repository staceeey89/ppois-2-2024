class Infrastructure:
    def __init__(self, *, level: int = 1):
        self._level = level

    @property
    def level(self):
        return self._level

    def enhance(self):
        self._level += 1

    def get_cost_of_enhancing(self):
        return self.level * 100
