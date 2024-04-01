import tkinter.messagebox

from src.view.add_user_window import AddUserWindow
from src.model.user import User
from src.presenter.user_validator import UserValidator
from src.presenter.abstract.presenter import Presenter


class AddUserWindowPresenter(Presenter):
    def __init__(self, window: AddUserWindow, *, validator=UserValidator()):
        super().__init__(window)
        self._new_user: User | None = None
        self._validator = validator

    def _do_subscriptions(self) -> None:
        self._window.subscribe("<<ok_button_click>>", self.__ok_button_click_handler)

    @property
    def new_user(self):
        return self._new_user

    def __ok_button_click_handler(self, **kwargs):
        try:
            self._new_user = self._validator.validate_user(User(-1, *kwargs.values()))
            self._window.destroy()
        except ValueError as err:
            tkinter.messagebox.showerror("Error", str(err), master=self._window)
