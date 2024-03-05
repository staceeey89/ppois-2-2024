from src.controller.commands.command import Command


class RemoveCommand(Command):
    name = "remove"

    def execute(self):
        args: list[str] = self.args
        try:
            if args[0] == "state":
                state = self.repository.get_state(args[1].replace('_', ' '))
                self.repository.remove_state(state)

                return f"State {state.name} removed"

            elif args[0] == "citizen":
                state = self.repository.get_state(args[2].replace('_', ' '))
                person = state.population.get_citizen(args[1].replace('_', ' '))
                state.population.remove_citizen(person)
                self.repository.add_state(state)

                return f"Citizen {person.name} removed from state {state.name}"

            else:
                raise ValueError("Invalid type of adding object. Must be state or citizen")

        except Exception as e:
            raise Exception("Remove command: " + str(e))

    def can_execute(self) -> bool:
        return self.repository.get_states and len(self.args) in range(2, 4)
