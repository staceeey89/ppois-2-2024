from datetime import datetime
from tkinter import messagebox, Toplevel, Label

from app.view import View
from core.players_list import PlayersList


class Controller:
    __PLAYERS_LIMIT = 10
    __offset_search_page = 0
    __offset_main_page = 0

    def switch_to_xml(self, file_path):
        self.players_list.switch_db_to_xml(file_path)
        self.__offset_search_page = 0
        self.__offset_main_page = 0
        self.load_players()
        messagebox.showinfo("Switch Database", f"Switched to XML database: {file_path}")
        self.view.switch_db_dialog.destroy()

    def switch_to_sql(self):
        self.players_list.switch_db_to_sql()
        self.__offset_search_page = 0
        self.__offset_main_page = 0
        self.load_players()
        messagebox.showinfo("Switch Database", f"Switched to mySQL database")
        self.view.switch_db_dialog.destroy()

    def __init__(self, root):
        self.players_list = PlayersList()
        self.view = View(root, self)
        self.load_players()
        self.search_input = {}
        self.search_criteria = {}

    def get_all_players(self):
        result = self.players_list.fetch_players_from_db()
        return result

    def get_players_limit(self):
        return self.__PLAYERS_LIMIT

    def set_players_limit(self, new_limit):
        if 0 < new_limit < 100:
            self.__offset_main_page = 0
            self.__PLAYERS_LIMIT = new_limit
            self.load_players()
        else:
            messagebox.showerror("Error", "0 < players_limit < 100")

    def get_current_page_num(self, offset):
        return (offset // self.__PLAYERS_LIMIT) + 1

    def get_pages_count(self, search_criteria=None):
        players_count = self.players_list.get_players_count(search_criteria)
        pages_count = players_count // self.__PLAYERS_LIMIT
        if players_count % self.__PLAYERS_LIMIT != 0:
            pages_count += 1
        return pages_count

    def get_page_num(self, frame_type):
        current_page = None
        pages_count = None
        if frame_type == "main":
            current_page = self.get_current_page_num(offset=self.__offset_main_page)
            pages_count = self.get_pages_count()
        elif frame_type == "search":
            current_page = self.get_current_page_num(offset=self.__offset_search_page)
            pages_count = self.get_pages_count(self.search_criteria)

        return str(current_page) + "/" + str(pages_count)

    def delete_players(self):
        delete_criteria = self.__configure_search_criteria()
        if len(delete_criteria) == 0:
            self.show_search_fields_empty_error()
            return
        if self.confirm_delete():
            players_deleted = self.players_list.delete_player(delete_criteria)
            if players_deleted > 0:
                self.show_deleted_players_count(players_deleted)
                self.__offset_main_page = 0
                self.load_players()
            else:
                self.show_deletion_error()

    @staticmethod
    def show_deletion_error():
        messagebox.showerror("Error", "No players matched the criteria.\nNothing was deleted.")

    def show_deleted_players_count(self, deleted_count):
        players_deleted_window = Toplevel(self.view.root)
        players_deleted_window.title("Players Deleted")
        message = f"{deleted_count} player(s) deleted successfully."
        confirmation_label = Label(players_deleted_window, text=message)
        confirmation_label.pack(padx=10, pady=10)

    def load_players(self):
        self.players_list.fetch_players_from_db(limit=self.__PLAYERS_LIMIT, offset=self.__offset_main_page,
                                                search_criteria={})
        self.view.update_main_window(self.players_list.players)

    @staticmethod
    def __convert_date_format(date_str):
        try:
            date_obj = datetime.strptime(date_str, "%m/%d/%y")
            result = date_obj.strftime("%Y-%m-%d")
        except:
            Controller.show_invalid_date_error()
            raise Exception("Invalid date")
        return result

    @staticmethod
    def show_search_fields_empty_error():
        messagebox.showerror("Error", "Search fields are empty")

    def search_players(self, frame):
        search_criteria = self.__configure_search_criteria()

        if search_criteria:
            self.players_list.fetch_players_from_db(limit=self.__PLAYERS_LIMIT, offset=self.__offset_search_page,
                                                    search_criteria=search_criteria)
            if frame == "search":
                self.view.update_search_results(self.players_list.players)
            elif frame == "delete":
                self.view.update_delete_results(self.players_list.players)
        else:
            self.show_search_fields_empty_error()
            return

    @staticmethod
    def __get_search_term(criteria, search_term):
        match criteria:
            case "Full Name":
                return {"full_name": search_term}
            case "Birth Date":
                return {"birth_date": search_term}
            case "Position":
                return {"position": search_term}
            case "Squad":
                return {"squad": search_term}
            case "Football Team":
                return {"football_team": search_term}
            case "Home City":
                return {"home_city": search_term}
            case _:
                return None

    def __configure_search_criteria(self):
        self.search_input = {
            "main_search_value": self.view.search_entry.get(),
            "main_criteria": self.view.criteria.get(),
            "additional_search_value": self.view.additional_search_entry.get(),
            "additional_criteria": self.view.additional_criteria.get()
        }

        if self.search_input.get("main_criteria") == 'Birth Date':
            self.search_input["main_search_value"] = self.__convert_date_format(self.view.date_entry.get())

        if self.search_input.get("additional_criteria") == 'Birth Date':
            self.search_input["additional_search_value"] = self.__convert_date_format(
                self.view.additional_date_entry.get())

        main_criteria = self.__get_search_term(self.search_input.get("main_criteria"),
                                               self.search_input.get("main_search_value"))
        additional_criteria_dict = self.__get_search_term(self.search_input.get("additional_criteria"),
                                                          self.search_input.get("additional_search_value"))

        if main_criteria is not None:
            self.search_criteria = main_criteria
            if additional_criteria_dict is not None:
                self.search_criteria.update(additional_criteria_dict)
            return self.search_criteria
        elif additional_criteria_dict is not None:
            self.search_criteria = additional_criteria_dict
            return self.search_criteria
        else:
            self.search_criteria = {}
            return self.search_criteria

    def add_player(self):
        full_name = self.view.full_name_entry.get()
        birth_date = self.__convert_date_format(self.view.birth_date_entry.get())
        football_team = self.view.football_team_entry.get()
        home_city = self.view.home_city_entry.get()
        squad = self.view.squad_entry.get()
        position = self.view.position_entry.get()
        if full_name and birth_date and football_team and home_city and squad and position:
            self.players_list.add_player(full_name, birth_date, football_team, home_city, squad, position)
            messagebox.showinfo("Player successfully added", f"PLayer {full_name} has been successfully added")
            self.load_players()
        else:
            messagebox.showerror("Error", f"Fields are empty")

    def __load_first_search_page(self):
        if self.__offset_search_page > 0:
            self.__offset_search_page = 0
            self.players_list.fetch_players_from_db(limit=self.__PLAYERS_LIMIT, offset=self.__offset_search_page,
                                                    search_criteria=self.search_criteria)
            self.view.update_search_results(players=self.players_list.players)

    def __load_first_main_page(self):
        if self.__offset_main_page > 0:
            self.__offset_main_page = 0
            self.players_list.fetch_players_from_db(limit=self.__PLAYERS_LIMIT, offset=self.__offset_main_page)
            self.view.update_main_window(players=self.players_list.players)

    def __load_last_search_page(self):
        if self.players_list.get_players_count(
                self.search_criteria) <= self.__offset_search_page + self.__PLAYERS_LIMIT:
            return

        full_page = self.players_list.get_players_count(self.search_criteria) % self.__PLAYERS_LIMIT == 0
        if not full_page:
            self.__offset_search_page = self.players_list.get_players_count(
                self.search_criteria) - self.players_list.get_players_count(self.search_criteria) % self.__PLAYERS_LIMIT
        else:
            self.__offset_search_page = self.players_list.get_players_count(self.search_criteria) - self.__PLAYERS_LIMIT
        self.players_list.fetch_players_from_db(limit=self.__PLAYERS_LIMIT, offset=self.__offset_search_page,
                                                search_criteria=self.search_criteria)
        self.view.update_search_results(players=self.players_list.players)

    def __load_last_main_page(self):
        if self.players_list.get_players_count() <= self.__offset_main_page:
            return

        full_page = self.players_list.get_players_count() % self.__PLAYERS_LIMIT == 0
        if not full_page:
            self.__offset_main_page = (self.players_list.get_players_count()
                                       - self.players_list.get_players_count() % self.__PLAYERS_LIMIT)
        else:
            self.__offset_main_page = self.players_list.get_players_count() - self.__PLAYERS_LIMIT
        self.players_list.fetch_players_from_db(limit=self.__PLAYERS_LIMIT, offset=self.__offset_main_page)
        self.view.update_main_window(players=self.players_list.players)

    def __load_prev_search_page(self):
        if self.__offset_search_page >= self.__PLAYERS_LIMIT:
            self.__offset_search_page -= self.__PLAYERS_LIMIT
            self.players_list.fetch_players_from_db(limit=self.__PLAYERS_LIMIT, offset=self.__offset_search_page,
                                                    search_criteria=self.search_criteria)
            self.view.update_search_results(self.players_list.players)

    def __load_prev_main_page(self):
        if self.__offset_main_page >= self.__PLAYERS_LIMIT:
            self.__offset_main_page -= self.__PLAYERS_LIMIT
            self.players_list.fetch_players_from_db(limit=self.__PLAYERS_LIMIT, offset=self.__offset_main_page)
            self.view.update_main_window(players=self.players_list.players)

    def __load_next_search_page(self):
        if self.__offset_search_page < self.players_list.get_players_count(self.search_criteria) - self.__PLAYERS_LIMIT:
            self.__offset_search_page += self.__PLAYERS_LIMIT
            self.players_list.fetch_players_from_db(limit=self.__PLAYERS_LIMIT, offset=self.__offset_search_page,
                                                    search_criteria=self.search_criteria)
            self.view.update_search_results(self.players_list.players)

    def __load_next_main_page(self):
        if self.__offset_main_page < self.players_list.get_players_count() - self.__PLAYERS_LIMIT:
            self.__offset_main_page += self.__PLAYERS_LIMIT
            self.players_list.fetch_players_from_db(limit=self.__PLAYERS_LIMIT, offset=self.__offset_main_page)
            self.view.update_main_window(players=self.players_list.players)

    def pagination(self, frame_type, action):
        if frame_type == "main":
            if action == "first":
                self.__load_first_main_page()
            elif action == "last":
                self.__load_last_main_page()
            elif action == "prev":
                self.__load_prev_main_page()
            elif action == "next":
                self.__load_next_main_page()
        elif frame_type == "search":
            if action == "first":
                self.__load_first_search_page()
            elif action == "last":
                self.__load_last_search_page()
            elif action == "prev":
                self.__load_prev_search_page()
            elif action == "next":
                self.__load_next_search_page()

    def first_page(self, page_type):
        self.pagination(page_type, "first")

    def last_page(self, page_type):
        self.pagination(page_type, "last")

    def prev_page(self, page_type):
        self.pagination(page_type, "prev")

    def next_page(self, page_type):
        self.pagination(page_type, "next")

    def confirm_delete(self):
        result = messagebox.askokcancel("Confirm Deletion", "Are you sure you want to delete this players?",
                                        parent=self.view.delete_frame)
        return result

    @staticmethod
    def show_invalid_date_error():
        messagebox.showerror("Invalid date", "Invalid date type")
