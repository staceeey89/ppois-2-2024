from src.controller.commands.command import Command


class EnhanceInfrastructureCommand(Command):
    name = "enhance_infrastructure"

    def execute(self):
        try:
            state = self.repository.get_state(self.args[0])
            state.economy.enhance_infrastructure()
        except Exception as e:
            raise Exception("Enhance infrastructure command: " + str(e))

        self.repository.add_state(state)
        return f"Infrastructure of {state.name} successfully enhanced"

    def can_execute(self) -> bool:
        return self.repository.get_states() and len(self.args) == 1
