# this module is responsible for saving and loading state

from .file import File
from Exceptions.exceptions import File_Exception

import pickle   # library for serializing and deserializing object.


class Student_File(File):

    def __init__(self, file_name: str):
        self.__file_name = file_name

    def save(self, list_of_objects):
        with open(self.__file_name, "wb") as out_file: # this structure automatically closes the file
            pickle.dump(list_of_objects, out_file)
        print(f"Completely saved to {self.__file_name}")

    def load(self):
        try:
            with open(self.__file_name, "rb") as in_file:
                list_of_objects = pickle.load(in_file)
            print(f"Completely loaded from {self.__file_name}")
            return list_of_objects
        except FileNotFoundError:

            print(f"Error in loading state from {self.__file_name}\n Default settings have been set")
            raise File_Exception
