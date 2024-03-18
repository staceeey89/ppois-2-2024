class SecurityRequirement:
    def __init__(self, rule:str):
        self._rule = rule
    @property
    def rule(self):
        return self._rule

    @rule.setter
    def rule(self, value):
        self._rule = value