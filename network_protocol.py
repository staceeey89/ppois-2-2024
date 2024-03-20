from typing import List


class NetworkProtocol:

    def __init__(self):
        from main import OperatingSystem
        self.__osc: List['OperatingSystem'] = []

    def show_linked_osc(self):
        if len(self.__osc) == 0:
            raise Exception("No connected systems!")
        for i in self.__osc:
            print(i.name, end=" ")
        print('\n')

    def add(self, os):
        self.__osc.append(os)

    @property
    def osc(self):
        return self.__osc
