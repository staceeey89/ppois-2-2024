from typing import List

from file_system import FileSystem
from kernel import Kernel
from network_protocol import NetworkProtocol
from user_interface import UserInterface
from driver import Driver
from save import save_changes
from load import load_changes


class OperatingSystem:
    __num_of_processes: int = 0

    def __init__(self, name: str):
        self.__kernel: Kernel = Kernel()
        self.__user_interface: UserInterface = UserInterface()
        self.__drivers: List[Driver] = []
        self.__file_system: FileSystem = FileSystem()
        self.__password = None
        self.__name: str = name
        self.__network_protocol: NetworkProtocol = NetworkProtocol()

    def start(self):
        self.__kernel.start()
        self.__num_of_processes += 1

    def shutdown(self):
        self.__kernel.shutdown()
        self.__num_of_processes = 0
        save_changes(self)

    def form_network(self, os: 'OperatingSystem'):
        self.__network_protocol.add(os)

    def send(self, content: str, OS: str):
        self.__kernel.create_signal(content)
        for os in self.__network_protocol.osc:
            if os.name == OS:
                os.__kernel.create_signal(content)
                self.__kernel.create_signal("Accepted!")
                return
        raise Exception("No such system!")

    def create_file(self, name: str, content: str):
        return self.__file_system.create_file(name, content)

    def delete_file(self, name: str):
        self.__file_system.delete_file(name)

    def check_driver(self, name: str):
        for i in self.__drivers:
            if i.name == name:
                return True
        return False

    def view_content(self, name: str):
        if self.check_driver("GPU"):
            for i in self.__file_system.files:
                if i.name == name:
                    return self.__user_interface.read_file(i)
            raise Exception("No such file!")
        else:
            raise Exception("No drivers for GPU!")

    def fork(self, resources: int):
        process = self.__kernel.create_process(str(self.__num_of_processes + 1),
                                     resources)
        self.__num_of_processes += 1
        return process

    def terminate_process(self, name: str):
        for i in self.__kernel.processes:
            if i.name == name:
                if name == 'init':
                    raise Exception("Can not delete init process!")
                self.__kernel.terminate_process(i)
                self.__num_of_processes -= 1
                return
        raise Exception("Process not founded!")

    def install_driver(self, name: str):
        for i in self.__drivers:
            if i.name == name:
                raise Exception("Already installed!")
        driver = Driver(name)
        self.__drivers.append(driver)

    @property
    def network_protocol(self):
        return self.__network_protocol

    @property
    def file_system(self):
        return self.__file_system

    @property
    def kernel(self):
        return self.__kernel

    @property
    def password(self):
        return self.__password

    @property
    def name(self):
        return self.__name

    def set_password(self, password: str):
        if len(password) >= 4:
            self.__password = password
        else:
            raise Exception("Minimal length of password is 4 symbols!")


if __name__ == "__main__":
    OS = load_changes()
    OS = OS or OperatingSystem("Olegux")
    while True:
        if OS.password is None:
            break
        else:
            password = input("Enter password: ")
            if password == OS.password:
                print("Successful enter!")
                break
            else:
                print("Wrong password!")
    OS.start()

    print(f"Hello!Operating system {OS.name} meet you!")
    while True:
        print("""Choose what you want:
           1- exit
           2- change password
           3- connect with other OS
           4- send a signal to other OS
           5- create file
           6- delete file
           7- view content of file
           8- create process
           9- terminate process
           10- download driver for GPU
           11- view all files
           12- view all processes
           """)
        n = int(input())
        if n == 1:
            print("Saving data...")
            OS.shutdown()
            print("Bye!")
            break
        elif n == 2:
            try:
                if OS.password is None:
                    new_ps = input("Input new password: ")
                    OS.set_password(new_ps)
                    print("New password was set successfully!")
                else:
                    ps = input("Input current password: ")
                    if ps == OS.password:
                        new_ps = input("Input new password: ")
                        OS.set_password(new_ps)
                        print("New password was set successfully!")
                    else:
                        print("Wrong password!")
            except Exception as e:
                print(e)
        elif n == 3:
            linked_os = (
                OperatingSystem("OS" +
                                str(1 + len(OS.network_protocol.osc)))
            )
            OS.form_network(linked_os)
            linked_os.form_network(OS)
            print("Connected successfully!")
        elif n == 4:
            try:
                content = input("Write the content for signal: ")
                print(f"All linked OS': ", end=" ")
                OS.network_protocol.show_linked_osc()
                otherOS = input("Write to what OS you want to send signal: ")
                OS.send(content, otherOS)
                print("Successful send!")
            except Exception as e:
                print(e)
        elif n == 5:
            try:
                name = input("Write the name of file: ")
                content = input("Write information you want to put in: ")
                OS.create_file(name, content)
            except Exception as e:
                print(e)
        elif n == 6:
            try:
                name = input("Write the name of file you want to delete: ")
                OS.delete_file(name)
            except Exception as e:
                print(e)
        elif n == 7:
            try:
                name = input("Write the name of file from which "
                             "you want to view content: ")
                content = OS.view_content(name)
                print(f"Content of file {name}: {content}")
            except Exception as e:
                print(e)
        elif n == 8:
            try:
                resources = int(input("Write what amount of resources "
                                      "you want to allocate to process: "))
                OS.fork(resources)
            except Exception as e:
                print(e)
        elif n == 9:
            try:
                name = input("Write what process you want to delete: ")
                OS.terminate_process(name)
            except Exception as e:
                print(e)
        elif n == 10:
            try:
                OS.install_driver("GPU")
            except Exception as e:
                print(e)
        elif n == 11:
            OS.file_system.show_all_files()
        elif n == 12:
            OS.kernel.show_all_processes()
