from financial_state_machine import FinancialStateMachine
from repository.file_repository import FileRepository, Repository

repository: Repository = FileRepository("appstate.pickle")

state_machine = FinancialStateMachine(repository)

while True:
    state_machine.move_next(input())
