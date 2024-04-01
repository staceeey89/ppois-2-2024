import tkinter.messagebox

from src.presenter.abstract.presenter import Presenter
from src.view.search_user_window import SearchUserWindow
import src.utils as utils
from src.model.DAO.db_repository import DBRepository
from src.exception.nothing_found_exception import NothingFoundException


class SearchUserWindowPresenter(Presenter):
    def __init__(self, window: SearchUserWindow, repo):
        super().__init__(window)
        self._repo = repo
        self._window = window
        self.users = []

    def _do_subscriptions(self) -> None:
        self._window.subscribe("<<ok_button_click>>", self.__ok_button_click_handler)
        self._window.subscribe("<<find_button_click>>", self.__find_button_click_handler)

    def __ok_button_click_handler(self):
        self._window.destroy()

    def __find_button_click_handler(self):
        match self._window.notebook.tabs().index(self._window.notebook.select()):
            case 0:
                try:
                    self.users = self._repo.find(
                        "Users.surname == '{0}' AND Users.MobileNumber == '{1}'".format(
                            self._window.search_args["surname"].get(),
                            self._window.search_args["mobile number"].get()
                        )
                    )
                except NothingFoundException:
                    tkinter.messagebox.showinfo(
                        "Message",
                        "Nothing was found",
                        master=self._window
                    )

                utils.clear_tree(self._window.search_tree)
                for user in self.users:
                    utils.add_user_to_tree(self._window.search_tree, user)
            case 1:
                try:
                    self.users = self._repo.find(
                        "Users.address == '{0}' AND Users.account == '{1}'".format(
                            self._window.search_args["address"].get(),
                            self._window.search_args["account"].get()
                        )
                    )
                except NothingFoundException:
                    tkinter.messagebox.showinfo(
                        "Message",
                        "Nothing was found",
                        master=self._window
                    )
                utils.clear_tree(self._window.search_tree)
                for user in self.users:
                    utils.add_user_to_tree(self._window.search_tree, user)
            case 2:
                try:
                    self.users = self._repo.find(
                        "(Users.name == '{0}' OR "
                        "Users.surname == '{1}' OR "
                        "Users.patronym == '{2}') AND "
                        "(Users.MobileNumber REGEXP '\\d*{3}\\d*' OR "
                        "Users.LandlineNumber REGEXP '\\d*{3}\\d*')".format(
                            self._window.search_args["name"].get(),
                            self._window.search_args["surname"].get(),
                            self._window.search_args["patronymic"].get(),
                            self._window.search_args["numbers that included in the one of numbers"].get()
                        )
                    )
                except NothingFoundException:
                    tkinter.messagebox.showinfo(
                        "Message",
                        "Nothing was found",
                        master=self._window
                    )
                utils.clear_tree(self._window.search_tree)
                for user in self.users:
                    utils.add_user_to_tree(self._window.search_tree, user)


if __name__ == "__main__":
    window = SearchUserWindow(None)
    presenter = SearchUserWindowPresenter(window, DBRepository("../../db.sqlite"))
    window.mainloop()
