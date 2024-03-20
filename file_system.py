from typing import List

from file import File


class FileSystem:
    def __init__(self):
        self.__files: List[File] = []

    def create_file(self, name: str, content: str):
        if len(name) == 0:
            raise Exception("No name for file!")
        file = File(name, content)
        self.__files.append(file)
        return file

    def delete_file(self, file: str):
        for i in self.__files:
            if i.name == file:
                self.__files.remove(i)
                return
        raise Exception("No such file!")

    def show_all_files(self):
        for i in self.__files:
            print(i.name)
    @property
    def files(self):
        return self.__files
