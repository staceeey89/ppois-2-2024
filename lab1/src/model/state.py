import re

from src.model.legislation import Legislation
from src.model.government import Government
from src.model.economy import Economy
from src.model.population import Population
from src.model.conditionOfRelationBetweenStates import ConditionOfRelationBetweenStates


class State:
    from src.model.citizen import Citizen

    def __init__(self, name: str, head: Citizen):
        self.name = name
        self._government: Government = Government(head)
        self._economy: Economy = Economy()
        self._legislation: Legislation = Legislation()
        self._population: Population = Population()
        self._external_politics: ExternalPolitics = ExternalPolitics()

        self._population.add_citizen(head)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value: str):
        pattern = re.compile(r'((([A-Z][a-z]*) )|of |the )*([A-Z][a-z]*)')
        if pattern.match(value):
            self._name = value
        else:
            raise ValueError("Invalid name of state")

    @property
    def government(self):
        return self._government

    @property
    def economy(self):
        return self._economy

    @property
    def legislation(self):
        return self._legislation

    @property
    def population(self):
        return self._population

    @property
    def external_politics(self):
        return self._external_politics


class ExternalRelation:
    def __init__(self, other_state: State, condition: ConditionOfRelationBetweenStates = 1):
        self._other_state = other_state
        self._condition = condition

    @property
    def other_state(self):
        return self._other_state

    @property
    def condition(self):
        return self._condition

    @condition.setter
    def condition(self, value: ConditionOfRelationBetweenStates):
        self._condition = value


class ExternalPolitics:
    def __init__(self):
        self._external_relations = []

    @property
    def relations(self):
        return self._external_relations

    def add_external_relation(self, external_relation: ExternalRelation):
        self._external_relations.append(external_relation)

    def get_external_relation(self, state_: State):
        try:
            return filter(lambda x: x.other_state == state_, self._external_relations)[0]
        except IndexError:
            raise ValueError()

    def remove_external_relation(self, external_relation: ExternalRelation):
        self._external_relations.remove(external_relation)
