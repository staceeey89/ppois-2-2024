from src.controller.commands.command import Command


class CommandException(Exception):
    def __init__(self, command: Command):
        self.command = command

    def __str__(self):
        s = ", ".join(self.command.args)
        return (f"Command {self.command.name} with arguments "
                f"{s} can't be executed")
