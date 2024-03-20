class File:
    def __init__(self, name, content):
        self.__name: str = name
        self.__content: str = content

    @property
    def name(self):
        return self.__name

    @property
    def content(self):
        return self.__content
