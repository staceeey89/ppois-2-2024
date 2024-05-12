from xml.sax.handler import ContentHandler

from src.model.user import User


class ListUserHandler(ContentHandler):
    def __init__(self):
        super().__init__()
        self._current = ""
        self._current_user: User | None = None
        self.users = []

    def startElement(self, name, attrs):
        self._current = name
        if name == "User":
            self._current_user = User()

    def endElement(self, name):
        if name == "User":
            self.users.append(self._current_user)

    def characters(self, content):
        self._current_user.__dict__[self._current] += content
