class Process:
    def __init__(self, name, resources):
        self.__name: str = name
        self.__resources: str = resources

    @property
    def name(self):
        return self.__name

    @property
    def resources(self):
        return self.__resources
