from src.view.delete_user_window import DeleteUserWindow
from src.presenter.delete_user_window_presenter import DeleteUserWindowPresenter
from src.view.abstract.window import Window
from src.model.DAO.repository import Repository


def delete_users(master: Window, repo: Repository) -> None:
    window = DeleteUserWindow(master)
    presenter = DeleteUserWindowPresenter(window, repo)
    window.wait_window()
