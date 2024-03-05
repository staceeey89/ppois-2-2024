from src.DAO.fileRepository import FileRepository
from src.controller.input import Input
from src.model.state import State
from src.model.citizen import Citizen
from src.controller.commands.enhanceInfrastructureCommand import EnhanceInfrastructureCommand


def test_enhance_infrastructure():
    repo = FileRepository("test")

