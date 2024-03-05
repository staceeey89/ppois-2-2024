from src.controller.commands.command import Command


class CollectTaxesCommand(Command):
    name = "collect_taxes"

    def execute(self):
        try:
            state = self.repository.get_state(self.args[0])
        except Exception as e:
            raise ValueError("Collect taxes command: " + str(e))

        old = state.economy.treasury
        for person in state.population.citizens:
            state.economy.collect_taxes(person)

        self.repository.add_state(state)

        return f"{state.economy.treasury - old} collected"

    def can_execute(self) -> bool:
        return len(self.args) == 1
