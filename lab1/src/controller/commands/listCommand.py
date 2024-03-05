from src.controller.commands.command import Command


class ListCommand(Command):
    name = "list"

    def execute(self):
        args = self.args
        if not args:
            states = self.repository.get_states()
            answer = ""
            for state in states:
                answer += f"{state.name}\n"
            return answer
        try:
            state = self.repository.get_state(args[0])
        except ValueError as e:
            raise ValueError("List command: " + str(e))

        conditions = {
            1: "war",
            2: "peace",
            3: "alliance",
        }

        answer = {
            "government": f"Head of government is {state.government.head.name}",
            "economy": (f"Treasure: {state.economy.treasury}\n"
                        f"Infrastructure level: {state.economy.infrastructure_level}"),
            "external_politics": "\n".join([f"{conditions[relation.condition]} with {relation.other_state.name}" for
                                            relation in state.external_politics.relations]),
            "legislation": ("*"*20+"\n").join([f"--{law.title}--\n{law.text}" for law in state.legislation.laws]),
            "population": ("*"*20+"\n").join([f"Name: {person.name}\nIncome: {person.income}\n" for
                                              person in state.population.citizens])
        }

        if args[1] not in answer.keys():
            raise ValueError("Invalid name of state part")

        return answer[args[1]]

    def can_execute(self, *args: str) -> bool:
        return self.repository.get_states and (len_ := len(args)) < 3 and len_ != 1
