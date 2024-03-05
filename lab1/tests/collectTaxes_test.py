from src.DAO.fileRepository import FileRepository
from src.controller.input import Input
from src.model.state import State
from src.model.citizen import Citizen
from src.controller.commands.collectTaxesCommand import CollectTaxesCommand


def test_collect_taxes():
    repo = FileRepository("test")
    head = Citizen("Head", 1000)
    repo.add_state(State("State", head))
    command = CollectTaxesCommand(Input("collect_taxes", ["State"]), repo)
    command.execute()
    state = repo.get_state("State")
    assert state.economy.treasury == 50
