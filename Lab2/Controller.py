import os
import sqlite3


class Controller:
    def __init__(self):
        self.open_file_name = ""

    def check_bd_or_xml_file(self):
        if self.open_file_name[len(self.open_file_name)-1] == "l":
            return True
        else:
            return False

    def connect_bd_file(self, data_base, path=""):
        if os.path.isfile(path):
            self.set_open_file_name(path)
            data_base.set_connection(self.open_file_name)
            return True
        else:
            return False

    def connect_xml_file(self, xml, path=""):
        if os.path.isfile(path):
            self.set_open_file_name(path)
            xml.set_connection(self.open_file_name)
            return True
        else:
            return False

    def set_open_file_name(self, path=""):
        self.open_file_name = path

    def check_empty_add_user(self, first_name, last_name, patronymic, group):
        if first_name != "" and last_name != "" and patronymic != "" and group != "":
            return True
        else:
            return False

    def calculate_num_pages_bd(self, data_base, num_users):
        if data_base.find_num_watch_pages() % num_users == 0:
            return data_base.find_num_watch_pages() // num_users
        else:
            return data_base.find_num_watch_pages() // num_users + 1

    def calculate_num_pages_xml(self, xml, num_users):
        if xml.get_num_users() % num_users == 0:
            return xml.get_num_users() // num_users
        else:
            return xml.get_num_users() // num_users + 1


    def get_users_on_last_page(self, data_base, xml, num_users):
        if not self.check_bd_or_xml_file():
            if data_base.find_num_watch_pages() % num_users == 0:
                return num_users
            else:
                return data_base.find_num_watch_pages() % num_users
        else:
            if xml.get_num_users() % num_users == 0:
                return num_users
            else:
                return xml.get_num_users() % num_users

    # Методы для страницы поиска по фамилии и группе
    def get_search_last_name_group_pages(self, data_base, last_name, group, xml, num_users):
        # Возвращает кол-во страниц
        if not self.check_bd_or_xml_file():
            if data_base.get_num_users_search_last_name_group(last_name, group) % num_users == 0:
                return data_base.get_num_users_search_last_name_group(last_name, group) // num_users
            else:
                return data_base.get_num_users_search_last_name_group(last_name, group) // num_users + 1
        else:
            if xml.get_num_users_search_last_name_group(last_name, group) % num_users == 0:
                return xml.get_num_users_search_last_name_group(last_name, group) // num_users
            else:
                return xml.get_num_users_search_last_name_group(last_name, group) // num_users + 1

    def get_users_on_last_page_last_name_group(self, data_base, last_name, group, xml, num_users):
        # Возвращает кол-во людей на ласт странице
        if not self.check_bd_or_xml_file():
            if data_base.get_num_users_search_last_name_group(last_name, group) % num_users == 0:
                return num_users
            else:
                return data_base.get_num_users_search_last_name_group(last_name, group) % num_users
        else:
            if xml.get_num_users_search_last_name_group(last_name, group) % num_users == 0:
                return num_users
            else:
                return xml.get_num_users_search_last_name_group(last_name, group) % num_users

    # Метода для страницы поиска по фамилии и колл-ву работы
    def get_search_last_name_opt_pages(self, data_base, last_name, low_opt, high_opt, xml, num_users):
        # Возвращает кол-во страниц
        if not self.check_bd_or_xml_file():
            if data_base.get_num_users_search_last_name_opt(last_name, low_opt, high_opt) % num_users == 0:
                return data_base.get_num_users_search_last_name_opt(last_name, low_opt, high_opt) // num_users
            else:
                return data_base.get_num_users_search_last_name_opt(last_name, low_opt, high_opt) // num_users + 1
        else:
            if xml.get_num_users_search_last_name_opt(last_name, low_opt, high_opt) % num_users == 0:
                return xml.get_num_users_search_last_name_opt(last_name, low_opt, high_opt) // num_users
            else:
                return xml.get_num_users_search_last_name_opt(last_name, low_opt, high_opt) // num_users + 1

    def get_users_on_last_page_last_name_opt(self, data_base, last_name, low_opt, high_opt, xml, num_users):
        # Возвращает кол-во людей на ласт странице
        if not self.check_bd_or_xml_file():
            if data_base.get_num_users_search_last_name_opt(last_name, low_opt, high_opt) % num_users == 0:
                return num_users
            else:
                return data_base.get_num_users_search_last_name_opt(last_name, low_opt, high_opt) % num_users
        else:
            if xml.get_num_users_search_last_name_opt(last_name, low_opt, high_opt) % num_users == 0:
                return num_users
            else:
                return xml.get_num_users_search_last_name_opt(last_name, low_opt, high_opt) % num_users

    # Метода для страницы поиска по группе и колл-ву работы
    def get_search_group_opt_pages(self, data_base, group, low_opt, high_opt, xml, num_users):
        # Возвращает кол-во страниц
        if not self.check_bd_or_xml_file():
            if data_base.get_num_users_search_group_opt(group, low_opt, high_opt) % num_users == 0:
                return data_base.get_num_users_search_group_opt(group, low_opt, high_opt) // num_users
            else:
                return data_base.get_num_users_search_group_opt(group, low_opt, high_opt) // num_users + 1
        else:
            if xml.get_num_users_search_group_opt(group, low_opt, high_opt) % num_users == 0:
                return xml.get_num_users_search_group_opt(group, low_opt, high_opt) // num_users
            else:
                return xml.get_num_users_search_group_opt(group, low_opt, high_opt) // num_users + 1

    def get_users_on_last_page_group_opt(self, data_base, group, low_opt, high_opt, xml, num_users):
        # Возвращает кол-во людей на ласт странице
        if not self.check_bd_or_xml_file():
            if data_base.get_num_users_search_group_opt(group, low_opt, high_opt) % num_users == 0:
                return num_users
            else:
                return data_base.get_num_users_search_group_opt(group, low_opt, high_opt) % num_users
        else:
            if xml.get_num_users_search_group_opt(group, low_opt, high_opt) % num_users == 0:
                return num_users
            else:
                return xml.get_num_users_search_group_opt(group, low_opt, high_opt) % num_users

    def check_empty_db_path(self):
        if self.open_file_name == "":
            return False
        else:
            return True

