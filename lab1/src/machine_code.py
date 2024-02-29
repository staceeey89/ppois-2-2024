from .optimizer import Optimizer


class MachineCode:
    def __init__(self):
        self.__machine_code = ""

    def __str__(self):
        return self.__machine_code

    def translate_to_machine_code(self, optimizer: Optimizer):
        for char in optimizer.result_code:
            ascii_code = ord(char)
            self.__machine_code += bin(ascii_code)[2:].zfill(8)

    def get_machine_code(self) -> str:
        return self.__machine_code
