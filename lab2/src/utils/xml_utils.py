import tkinter.filedialog

from src.model.DAO.xml_repository import XMLRepository
from src.model.user import User


def save_to_xml(users: list[User]):
    file = tkinter.filedialog.asksaveasfilename(filetypes=(("XML file", "*.xml"),))
    repo = XMLRepository(file)
    for user in users:
        repo.save(user)
    repo.commit()


def load_from_xml() -> list[User]:
    file = tkinter.filedialog.askopenfilename(filetypes=(("XML file", "*.xml"),))
    repo = XMLRepository(file)
    return repo.list()
