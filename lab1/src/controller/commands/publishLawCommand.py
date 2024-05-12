from src.controller.commands.command import Command
from src.model.law import Law


class PublishLawCommand(Command):
    name = "publish_law"

    def execute(self):
        args: list[str] = self.args
        title = args[1].replace('_', ' ')
        text = args[2].replace('_', ' ')
        law = Law(title, text)
        try:
            state = self.repository.get_state(args[0])
        except Exception as e:
            raise ValueError("Publish law command: " + str(e))
        state.legislation.publish_law(law)
        self.repository.add_state(state)

    def can_execute(self) -> bool:
        return self.repository.get_states() and len(self.args) == 3
