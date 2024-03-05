from src.controller.commands.command import Command


class ProvideSecurityCommand(Command):
    name = "provide_security"

    def execute(self):
        try:
            state = self.repository.get_state(self.args[0])
            person = state.population.get_citizen(self.args[1])
        except ValueError as e:
            raise ValueError("Provide security command: " + str(e))

        return state.government.provide_security(person)

    def can_execute(self) -> bool:
        return self.repository.get_states() and len(self.args) == 2
