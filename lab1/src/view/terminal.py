from src.controller.interpreter import Interpreter
from src.view.inputer import Inputer
from src.DAO.repository import Repository
from src.exceptions.commandExeption import CommandException


class Terminal:
    def __init__(
            self,
            inputer: Inputer,
            interpreter: Interpreter,
            repository: Repository
    ):
        self._inputer = inputer
        self._interpreter = interpreter
        self._repository = repository

    def work(self):
        input_ = self._inputer.get_input()
        command = self._interpreter.interpret(input_, self._repository)
        if not command.can_execute():
            raise CommandException(command)
        try:
            return command.execute()
        except Exception as ex:
            raise ex
