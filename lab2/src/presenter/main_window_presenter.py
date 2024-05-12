import tkinter.messagebox
import tkinter.filedialog

from src.presenter.abstract.presenter import Presenter
from src.view.main_window import MainWindow
from src.exception.nothing_found_exception import NothingFoundException
import src.utils as utils
from src.model.DAO.db_repository import DBRepository


class MainWindowPresenter(Presenter):
    def __init__(self, window: MainWindow):
        super().__init__(window)
        self._window = window
        self._accounts = []
        self._users = []
        self._page_size = self._window.indexes["page size"]
        self._total_records = self._window.indexes["total records"]
        self._selected_page = self._window.indexes["current page"]
        self._total_pages = self._window.indexes["total pages"]
        self._tree_view = self._window.tree_view_enabled

        self._page_size.set(10)
        self._selected_page.set(1)

    def _do_subscriptions(self) -> None:
        self._window.subscribe("<<add_user_command_click>>", self.__add_user_command_click_handler)
        self._window.subscribe("<<open_data_base_command_click>>", self.__open_db_command_click_handler)
        self._window.subscribe("<<commit_data_base_command_click>>", self.__commit_db_command_click_handler)
        self._window.subscribe("<<delete_user_command_click>>", self.__delete_user_command_click_handler)
        self._window.subscribe("<<search_user_command_click>>", self.__search_user_command_click_handler)
        self._window.subscribe("<<first_button_click>>", self.__first_button_click_handler)
        self._window.subscribe("<<next_button_click>>", self.__next_button_click_handler)
        self._window.subscribe("<<prev_button_click>>", self.__prev_button_click_handler)
        self._window.subscribe("<<last_button_click>>", self.__last_button_click_handler)
        self._window.subscribe("<<inc_button_click>>", self.__inc_button_click_handler)
        self._window.subscribe("<<dec_button_click>>", self.__dec_button_click_handler)
        self._window.subscribe("<<tree_view_checkbutton_click>>", self.__tree_view_checkbutton_click_handler)
        self._window.subscribe("<<save_to_xml_command_click>>", self.__save_to_xml_command_click_handler)
        self._window.subscribe("<<load_from_xml_command_click>>", self.__load_from_xml_command_click_handler)
        self._window.subscribe("<<create_data_base_command_click>>", self.__create_data_base_command_click_handler)

    def __add_user(self, user):
        self._users.append(user)
        utils.add_user_to_tree(self._window.users_tree, user)

    def __load_page(self, page: int = 1):
        if page < 1:
            raise NothingFoundException
        try:
            page_size = self._page_size.get()
            count = self._repo.count()
            self._total_records.set(count)
            self._total_pages.set(count//page_size + (1 if count % page_size != 0 else 0))
            self._users = self._repo.list(
                offset=page_size*(page-1),
                count=page_size
            )
        except NothingFoundException as e:
            raise e
        self.__reload_users_tree(self._window.users_tree)

    def __reload_users_tree(self, tree):
        utils.clear_tree(tree)
        for user in self._users:
            utils.add_user_to_tree(tree, user)

    def __change_page(self, page: int):
        try:
            self.__load_page(page)
        except NothingFoundException as e:
            raise e
        self._selected_page.set(page)

    def __add_user_command_click_handler(self):
        if self.__check_repo_exist():
            return
        utils.get_new_user(self._window, self._repo)
        self.__load_page()

    def __open_db_command_click_handler(self):
        file_name = tkinter.filedialog.askopenfilename(
            filetypes=(("SQLite data base file", "*.sqlite"),),
        )
        if file_name == "":
            return
        self._repo = utils.open_db(file_name)
        self.__load_page()

    def __commit_db_command_click_handler(self):
        self._repo.commit()

    def __first_button_click_handler(self):
        if self.__check_repo_exist():
            return
        self.__change_page(1)

    def __next_button_click_handler(self):
        if self.__check_repo_exist():
            return
        try:
            self.__change_page(self._selected_page.get() + 1)
        except NothingFoundException:
            tkinter.messagebox.showerror("Error", "This page is last.")

    def __prev_button_click_handler(self):
        if self.__check_repo_exist():
            return
        try:
            self.__change_page(self._selected_page.get() - 1)
        except NothingFoundException:
            tkinter.messagebox.showerror("Error", "This page is first.")

    def __last_button_click_handler(self):
        if self.__check_repo_exist():
            return
        self.__change_page(self._total_pages.get())

    def __inc_button_click_handler(self):
        if self.__check_repo_exist():
            return
        self._page_size.set(self._page_size.get() + 1)
        self.__load_page()

    def __dec_button_click_handler(self):
        if self.__check_repo_exist():
            return
        if (page_size := self._page_size.get()) < 2:
            tkinter.messagebox.showerror(
                "Error",
                "Page size can't be less then 1",
                master=self._window
            )
            return
        self._page_size.set(self._page_size.get() - 1)
        self.__load_page()

    def __check_repo_exist(self) -> bool:
        if answer := not self._repo:
            tkinter.messagebox.showerror(
                "Error",
                "Please, open data base.",
                master=self._window
            )
        return answer

    def __delete_user_command_click_handler(self):
        if self.__check_repo_exist():
            return
        utils.delete_users(self._window, self._repo)
        self.__load_page()

    def __search_user_command_click_handler(self):
        if self.__check_repo_exist():
            return
        utils.search_users(self._window, self._repo)

    def __tree_view_checkbutton_click_handler(self):
        if self._tree_view.get():
            self._window.users_tree["displaycolumns"] = ()
            self._window.users_tree["show"] = "tree"
        else:
            self._window.users_tree["displaycolumns"] = tuple(self._window.users_tree_columns.keys())
            self._window.users_tree["show"] = "headings"

    def __save_to_xml_command_click_handler(self):
        utils.save_to_xml(self._users)

    def __load_from_xml_command_click_handler(self):
        try:
            for user in utils.load_from_xml():
                self.__add_user(user)
        except NothingFoundException:
            tkinter.messagebox.showerror("", "Nothing was found.")

    def __create_data_base_command_click_handler(self):
        file_name = tkinter.filedialog.asksaveasfilename(
            title="Create data base",
            filetypes=(("SQLite data base file", "*.sqlite"),)
        )
        self._repo = DBRepository(file_name)
        self._repo.create_table()
        self._users = []
        utils.clear_tree(self._window.users_tree)
