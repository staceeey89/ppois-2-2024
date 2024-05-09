class Driver:
    def __init__(self, name):
        self.__name: str = name

    @property
    def name(self):
        return self.__name