import pytest
from src.DAO.fileRepository import FileRepository
from src.controller.input import Input
from src.model.state import State
from src.model.citizen import Citizen
from src.controller.commands.removeCommand import RemoveCommand


def test_remove_state():
    repo = FileRepository("test")
    state = State("New State", Citizen("Head"))
    repo.add_state(state)
    command = RemoveCommand(Input("remove", ["state", "New_State"]), repo)
    command.execute()
    assert state not in repo.get_states()


def test_remove_person():
    repo = FileRepository("test")
    state = State("New State", Citizen("Head"))
    person = Citizen("Person")
    state.population.add_citizen(person)
    repo.add_state(state)
    command = RemoveCommand(Input("remove", ["citizen", "Person", "New State"]), repo)
    command.execute()
    persons = repo.get_state("New State").population.citizens
    assert person not in persons
