from controller.controller import Controller
from repository.clinic_repository import PetRecordRepositoryList, PetRecordRepositorySQL, PetRecordRepositoryXML
from util.connection_manager import ConnectionManager
from view.view import View

if __name__ == "__main__":
    conn = ConnectionManager("veterinary_clinic.db")
    repository_list = PetRecordRepositoryList()
    repository_db = PetRecordRepositorySQL(conn)
    repository_xml = PetRecordRepositoryXML()
    controller = Controller(repository_list, repository_db, repository_xml)
    view = View(controller)
    view.start()
