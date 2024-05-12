import os.path

from src.model.DAO.repository import Repository
from src.model.DAO.db_repository import DBRepository


def open_db(file_name: str) -> Repository:
    if not os.path.exists(file_name):
        raise ValueError(f"Invalid file name: file {file_name} not exist")
    repo = DBRepository(file_name)
    return repo
