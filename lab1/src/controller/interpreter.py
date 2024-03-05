from typing import Callable

from src.controller.commands.command import Command
from src.controller.input import Input
from src.DAO.repository import Repository


class Interpreter:
    def __init__(self, commands: dict[str, Callable[[Input, Repository], Command]]):
        self._commands = commands

    def interpret(self, input_: Input, repository: Repository) -> Command:
        try:
            return self._commands[input_.command_name](input_, repository)
        except Exception as ex:
            raise Exception("Command interpretation error")
