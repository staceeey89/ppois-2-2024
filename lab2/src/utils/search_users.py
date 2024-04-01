from src.view.search_user_window import SearchUserWindow
from src.presenter.search_user_window_presenter import SearchUserWindowPresenter
from src.view.abstract.window import Window
from src.model.DAO.repository import Repository


def search_users(master: Window, repo: Repository) -> None:
    window = SearchUserWindow(master)
    presenter = SearchUserWindowPresenter(window, repo)
    window.wait_window()
