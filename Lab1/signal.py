class Signal:
    def __init__(self):
        self.__content: str

    @property
    def content(self):
        return self.__content
    
    @content.setter
    def content(self, content):
        self.__content = content
