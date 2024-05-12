class Law:
    def __init__(self, title: str, text: str):
        self._title: str = title
        self._text: str = text

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value: str):
        self._title = value

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value: str):
        self._text = value
