class SecurityRequirement:
    def __init__(self, rule, min_height, max_weight, min_age):
        self.rule: str = rule
        self.min_height: float = min_height
        self.max_weight: float = max_weight
        self.min_age: float = min_age

    @property
    def rule(self):
        return self._rule

    @rule.setter
    def rule(self, value):
        self._rule = value

    @property
    def min_height(self):
        return self._min_height

    @min_height.setter
    def min_height(self, value):
        self._min_height = value

    @property
    def max_weight(self):
        return self._max_weight

    @max_weight.setter
    def max_weight(self, value):
        self._max_weight = value

    @property
    def min_age(self):
        return self._min_age

    @min_age.setter
    def min_age(self, value):
        self._min_age = value