from src.model.conditionOfRelationBetweenStates import ConditionOfRelationBetweenStates
import src.model.state as state


class ExternalRelation:
    def __init__(self, other_state: state.State, condition: ConditionOfRelationBetweenStates = 1):
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
