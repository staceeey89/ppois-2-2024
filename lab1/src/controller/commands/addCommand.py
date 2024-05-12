from src.controller.commands.command import Command
from src.model.state import State
from src.model.citizen import Citizen


class AddCommand(Command):
    name = "add"

    def execute(self):
        args: list[str] = self.args
        try:
            if args[0] == "state":
                head = Citizen(args[2].replace('_', ' '))
                state = State(args[1].replace('_', ' '), head)
                self.repository.add_state(state)

                return f"State {state.name} added"

            elif args[0] == "citizen":
                if not args[2].isdecimal():
                    raise ValueError("Invalid income")

                person = Citizen(args[1].replace('_', ' '), int(args[2]))
                state = self.repository.get_state(args[3])
                state.population.add_citizen(person)
                self.repository.add_state(state)

                return f"Citizen {person.name} added to state {state.name}"

            else:
                raise ValueError("Invalid type of adding object. Must be state or citizen")

        except Exception as e:
            raise Exception("List command:" + str(e))

    def can_execute(self) -> bool:
        return len(self.args) in range(3, 5)
