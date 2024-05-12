import os.path
import xml.etree.ElementTree as ET
import xml.sax as sax

from src.model.DAO.repository import Repository
from src.model.user import User
from src.exception.nothing_found_exception import NothingFoundException
import src.model.DAO.user_handler as handler


class XMLRepository(Repository):
    def __init__(self, file_name):
        self.file = file_name
        if os.path.exists(file_name):
            self.tree = ET.parse(file_name)
        else:
            self.tree = ET.ElementTree()
            self.tree._setroot(ET.Element("Users"))

    def save(self, record: User) -> None:
        user = ET.SubElement(self.tree.getroot(), "User")
        for field, value in record:
            field_el = ET.SubElement(user, field)
            field_el.text = value

    def get(self, uid: int) -> tuple:
        pass

    def find(self, conditions: str) -> list[User]: pass

    def list(self, *, offset=0, count=None) -> list[User]:
        parser = sax.make_parser()
        parser.setFeature(sax.handler.feature_namespaces, 0)
        parser.setContentHandler(handler_ := handler.ListUserHandler())
        parser.parse(self.file)
        if users := handler_.users:
            return users
        raise NothingFoundException()

    def erase(self, user: User) -> None:
        pass

    def commit(self) -> None:
        self.tree.write(self.file)

    def count(self) -> int:
        pass
