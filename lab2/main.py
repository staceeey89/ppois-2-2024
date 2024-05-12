from util.connection_manager import ConnectionManager
from model.sportsman_dao import SportsmanRepositorySQL, SportsmanRepositoryXML, SportsmanRepositoryList
from controller.controller import Controller
from view.view import View


if __name__ == "__main__":
    conn = ConnectionManager()
    repository_list = SportsmanRepositoryList()
    repository_db = SportsmanRepositorySQL()
    repository_xml = SportsmanRepositoryXML()
    controller = Controller(repository_list, repository_db, repository_xml)
    view = View(controller)
    view.start()
