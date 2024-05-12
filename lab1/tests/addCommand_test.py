import pytest
from src.DAO.fileRepository import FileRepository
from src.controller.input import Input
from src.model.state import State
from src.model.citizen import Citizen
from src.controller.commands.addCommand import AddCommand


def test_add_state():
    repo = FileRepository("test")
    command = AddCommand(Input("add", ["state", "New_State", "State_Head"]), repo)
    command.execute()
    state = repo.get_state("New State")
    assert state.name == "New State"
    assert state.government.head.name == "State Head"


def test_add_person():
    repo = FileRepository("test")
    repo.add_state(State("State", Citizen("Head")))
    command = AddCommand(Input("add", ["citizen", "Citizen", "1000", "State"]), repo)
    command.execute()
    person = repo.get_state("State").population.get_citizen("Citizen")
    assert person.name == "Citizen"
