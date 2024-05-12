from .subject_progress import Subject_Progress

class Student:
    def __init__(self, name):
        self.__name: str = name
        self.__subjects_progress: list[Subject_Progress] = []

    def get_name(self):
        return self.__name

    def get_subjects_progress(self):
        return self.__subjects_progress

