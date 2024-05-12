from src.view.inputer import Inputer
from src.controller.input import Input


class ConsoleInputer(Inputer):
    def get_input(self) -> Input:
        command_name, *args = input("/").strip().split(" ")
        return Input(command_name, args)
