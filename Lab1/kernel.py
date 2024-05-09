from typing import List

from signal import Signal
from process import Process


class Kernel:
    def __init__(self):
        self.__processes: List[Process] = []
        self.__signal: Signal = Signal()
        self.__RAM: int = 8000

    def start(self):
        self.create_process("init", 2000)

    def shutdown(self):
        for i in self.__processes[:]:
            self.terminate_process(i)
        self.__signal = None

    def create_signal(self, content: str):
        self.__signal = Signal()
        self.__signal.content = content

    @property
    def signal(self):
        return self.__signal

    @property
    def processes(self):
        return self.__processes

    def create_process(self, name: str, resource: int):
        if resource > self.__RAM:
            raise Exception("Too much resources allocated!")
        if resource <= 0:
            raise Exception("Can not allocate memory!")
        process = Process(name, resource)
        self.__processes.append(process)
        self.__RAM -= resource
        return process

    def terminate_process(self, process: Process):
        self.__RAM += process.resources
        self.__processes.remove(process)

    def show_all_processes(self):
        for i in self.__processes:
            print(i.name, end=" ")
        print('\n')
