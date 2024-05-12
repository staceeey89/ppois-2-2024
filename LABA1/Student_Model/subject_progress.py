class Subject_Progress:
    def __init__(self, name):
        self.__progress = 0
        self.__name: str = name

    def get_progress(self) -> int:
        return self.__progress

    def set_progress(self, num: int) -> None:
        self.__progress = num

    def get_name(self):
        return self.__name

