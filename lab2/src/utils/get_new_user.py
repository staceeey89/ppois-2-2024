from tkinter.messagebox import showinfo

from src.view.add_user_window import AddUserWindow
from src.presenter.add_user_window_presenter import AddUserWindowPresenter
from src.model.DAO.repository import Repository
from src.exception.nothing_found_exception import NothingFoundException


def get_new_user(main_window, repo: Repository) -> None:
    window = AddUserWindow(main_window)
    presenter = AddUserWindowPresenter(window)
    window.wait_window()
    if user := presenter.new_user:
        try:
            repo.save(user)
        except NothingFoundException:
            showinfo("info", "Nothing are found")
