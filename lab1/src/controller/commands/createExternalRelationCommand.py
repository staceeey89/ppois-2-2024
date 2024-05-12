from src.controller.commands.command import Command
from src.model.conditionOfRelationBetweenStates import ConditionOfRelationBetweenStates
from src.model.externalRelation import ExternalRelation


class CreateExternalRelationCommand(Command):
    name = "create_external_relation"

    def execute(self):
        conditions = {
            "war": ConditionOfRelationBetweenStates.WAR,
            "peace": ConditionOfRelationBetweenStates.PEACE,
            "alliance": ConditionOfRelationBetweenStates.ALLIANCE,
        }

        try:
            first = self.repository.get_state(self.args[0])
            second = self.repository.get_state(self.args[1])
            condition = conditions[self.args[2]]
            try:
                first.external_politics.remove_external_relation(first.external_politics.get_external_relation(second))
                second.external_politics.remove_external_relation(second.external_politics.get_external_relation(first))
            except ValueError:
                pass
            first.external_politics.add_external_relation(ExternalRelation(second, condition))
            second.external_politics.add_external_relation(ExternalRelation(first, condition))

            self.repository.add_state(first)
            self.repository.add_state(second)

            return "Relation created"
        except Exception as e:
            raise Exception(f"{self.name}: " + str(e))

    def can_execute(self) -> bool:
        return len(self.args) == 3 and len(self.repository.get_states()) >= 2
