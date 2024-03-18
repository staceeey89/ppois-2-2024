
class Attraction:

    def __init__(self, name:str, security_requirement, capacity):
        self.name = name
        self.security_requirements = []
        self.add_security_requirement(security_requirement)
        self.capacity = capacity

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def security_requirements(self):
        return self._security_requirements

    @security_requirements.setter
    def security_requirements(self, value):
        self._security_requirements = value

    @property
    def capacity(self):
        return self._capacity

    @capacity.setter
    def capacity(self, value):
        self._capacity = value

    def add_security_requirement(self, rules):
        self.security_requirements.append(rules)

    def show_security_requirements(self):
        print("Security requirements for", self.name + ":")
        for requirement in self.security_requirements:
            print(requirement.rule)