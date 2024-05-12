from src.controller.commands.command import Command


class ExitCommand(Command):
    name = "exit"

    def execute(self):
        exit(0)

    def can_execute(self) -> bool:
        return len(self.args) == 0