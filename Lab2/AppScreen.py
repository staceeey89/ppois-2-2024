from PyQt5.QtWidgets import QWidget

from AddScreen import AddScreen
from Controller import Controller
from DataBase import DataBase
from DelGroupOptScreen import DelGroupOptScreen
from DelLastNameGroupScreen import DelLastNameGroupScreen
from DelLastNameOptScreen import DelLastNameOptScreen
from DeleteScreen import DeleteScreen
from LastNameGroupScreen import LastNameGroupScreen
from LastNameOptScreen import LastNameOptScreen
from MainScreen import MainScreen
from SearchScreen import SearchScreen
from SelectFileScreen import SelectFileScreen
from TreeScreen import TreeScreen
from WatchScreen import WatchScreen
from GroupOptScreen import GroupOptScreen
from XML import XML


class AppScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(0, 0, 500, 700)
        self.setFixedSize(500, 700)
        self.setWindowTitle('Lab2')

        self.controller = Controller()
        self.data_base = DataBase(self.controller)
        self.xml = XML()
        self.main_screen = MainScreen()
        self.del_group_opt_screen = DelGroupOptScreen(self.data_base, self.controller, self.xml)
        self.del_last_name_opt_screen = DelLastNameOptScreen(self.data_base, self.controller, self.xml)
        self.del_last_name_group_screen = DelLastNameGroupScreen(self.data_base, self.controller, self.xml)
        self.delete_screen = DeleteScreen(self.del_last_name_group_screen, self.del_last_name_opt_screen,
                                          self.del_group_opt_screen)
        self.group_opt_screen = GroupOptScreen(self.controller, self.data_base, self.xml)
        self.last_name_opt_screen = LastNameOptScreen(self.controller, self.data_base, self.xml)
        self.last_name_group_screen = LastNameGroupScreen(self.controller, self.data_base, self.xml)
        self.search_screen = SearchScreen(self.last_name_group_screen, self.last_name_opt_screen, self.group_opt_screen)
        self.select_file_screen = SelectFileScreen(self.controller, self.data_base, self.xml)
        self.add_screen = AddScreen(self.xml, self.data_base, self.controller)
        self.watch_screen = WatchScreen(self.controller, self.data_base, self.xml)
        self.tree_screen = TreeScreen(self.data_base, self.controller, self.xml)

        self.del_group_opt_screen.setParent(self)
        self.del_last_name_opt_screen.setParent(self)
        self.del_last_name_group_screen.setParent(self)
        self.delete_screen.setParent(self)
        self.group_opt_screen.setParent(self)
        self.last_name_opt_screen.setParent(self)
        self.main_screen.setParent(self)
        self.select_file_screen.setParent(self)
        self.add_screen.setParent(self)
        self.watch_screen.setParent(self)
        self.search_screen.setParent(self)
        self.last_name_group_screen.setParent(self)
        self.tree_screen.setParent(self)

        self.main_screen.show()

        self.main_screen.select_file_button.disconnect()
        self.main_screen.select_file_button.clicked.connect(self.hide_main_screen_and_show_select_file_screen)

        self.select_file_screen.home_button.disconnect()
        self.select_file_screen.home_button.clicked.connect(self.hide_select_file_screen_and_show_main_screen)

        self.main_screen.add_button.disconnect()
        self.main_screen.add_button.clicked.connect(self.hide_main_screen_and_show_add_screen)

        self.add_screen.home_button.disconnect()
        self.add_screen.home_button.clicked.connect(self.hide_add_screen_and_show_main_screen)

        self.main_screen.watch_button.disconnect()
        self.main_screen.watch_button.clicked.connect(self.hide_main_screen_and_show_watch_screen)

        self.watch_screen.home_button.disconnect()
        self.watch_screen.home_button.clicked.connect(self.hide_watch_screen_and_show_main_screen)

        self.main_screen.search_button.disconnect()
        self.main_screen.search_button.clicked.connect(self.hide_main_screen_and_show_search_screen)

        self.search_screen.home_button.disconnect()
        self.search_screen.home_button.clicked.connect(self.hide_search_screen_and_show_main_screen)

        self.last_name_group_screen.home_button.disconnect()
        self.last_name_group_screen.home_button.clicked.connect(self.hide_last_name_group_screen_and_show_main_screen)

        self.last_name_opt_screen.home_button.disconnect()
        self.last_name_opt_screen.home_button.clicked.connect(self.hide_last_name_opt_screen_and_show_main_screen)

        self.group_opt_screen.home_button.disconnect()
        self.group_opt_screen.home_button.clicked.connect(self.hide_group_opt_screen_and_show_main_screen)

        self.main_screen.delete_button.disconnect()
        self.main_screen.delete_button.clicked.connect(self.hide_main_screen_and_show_delete_screen)

        self.delete_screen.home_button.disconnect()
        self.delete_screen.home_button.clicked.connect(self.hide_delete_screen_and_show_main_screen)

        self.del_last_name_group_screen.home_button.disconnect()
        self.del_last_name_group_screen.home_button.clicked.connect(
            self.hide_del_last_name_group_screen_and_show_main_screen)

        self.del_last_name_opt_screen.home_button.disconnect()
        self.del_last_name_opt_screen.home_button.clicked.connect(
            self.hide_del_last_name_opt_screen_and_show_main_screen)

        self.del_group_opt_screen.home_button.disconnect()
        self.del_group_opt_screen.home_button.clicked.connect(self.hide_del_group_opt_screen_and_show_main_screen)

        self.main_screen.tree_button.disconnect()
        self.main_screen.tree_button.clicked.connect(self.hide_main_screen_and_show_tree_screen)

        self.tree_screen.home_button.disconnect()
        self.tree_screen.home_button.clicked.connect(self.hide_tree_screen_and_show_main_screen)

        self.show()

    # Прячем главный экран и выводим экран выбора файла
    def hide_main_screen_and_show_select_file_screen(self):
        self.main_screen.hide()
        self.select_file_screen.show()

    def hide_select_file_screen_and_show_main_screen(self):
        self.select_file_screen.hide()
        self.select_file_screen.input_file_name_field.clear()
        if self.controller.open_file_name != "":
            self.main_screen.activate_buttons()
        self.main_screen.show()

    def hide_main_screen_and_show_add_screen(self):
        if self.controller.open_file_name != "":
            self.main_screen.hide()
            self.add_screen.show()

    def hide_add_screen_and_show_main_screen(self):
        self.add_screen.hide()
        self.add_screen.clear_input_fields()
        self.main_screen.show()

    def hide_main_screen_and_show_watch_screen(self):
        if self.controller.open_file_name != "":
            # Для бд
            self.main_screen.hide()
            if not self.controller.check_bd_or_xml_file():
                self.watch_screen.set_num_pages_bd(self.controller, self.data_base)
            else:
                self.watch_screen.set_num_pages_xml(self.controller, self.xml)
            self.watch_screen.start_printing(self.data_base, self.controller, self.xml)
            self.watch_screen.show()

    def hide_watch_screen_and_show_main_screen(self):
        self.watch_screen.hide()
        self.main_screen.show()

    def hide_main_screen_and_show_search_screen(self):
        if self.controller.open_file_name != "":
            self.main_screen.hide()
            self.search_screen.show()

    def hide_search_screen_and_show_main_screen(self):
        self.search_screen.hide()
        self.main_screen.show()

    def hide_last_name_group_screen_and_show_main_screen(self):
        self.last_name_group_screen.hide()
        self.last_name_group_screen.zero_page()
        self.last_name_group_screen.clear_records()
        self.last_name_group_screen.input_last_name_field.clear()
        self.last_name_group_screen.input_group_field.clear()
        self.main_screen.show()

    def hide_last_name_opt_screen_and_show_main_screen(self):
        self.last_name_opt_screen.hide()
        self.last_name_opt_screen.zero_page()
        self.last_name_opt_screen.clear_records()
        self.last_name_opt_screen.input_last_name_field.clear()
        self.last_name_opt_screen.input_low_opt_field.clear()
        self.last_name_opt_screen.input_high_opt_field.clear()
        self.main_screen.show()

    def hide_group_opt_screen_and_show_main_screen(self):
        self.group_opt_screen.hide()
        self.group_opt_screen.zero_page()
        self.group_opt_screen.clear_records()
        self.group_opt_screen.input_group_field.clear()
        self.group_opt_screen.input_low_opt_field.clear()
        self.group_opt_screen.input_high_opt_field.clear()
        self.main_screen.show()

    def hide_main_screen_and_show_delete_screen(self):
        if self.controller.open_file_name != "":
            self.main_screen.hide()
            self.delete_screen.show()

    def hide_delete_screen_and_show_main_screen(self):
        self.delete_screen.hide()
        self.main_screen.show()

    def hide_del_last_name_group_screen_and_show_main_screen(self):
        self.del_last_name_group_screen.hide()
        self.del_last_name_group_screen.input_group_field.clear()
        self.del_last_name_group_screen.input_group_field.clear()
        self.main_screen.show()

    def hide_del_last_name_opt_screen_and_show_main_screen(self):
        self.del_last_name_opt_screen.hide()
        self.del_last_name_opt_screen.input_last_name_field.clear()
        self.del_last_name_opt_screen.input_low_opt_field.clear()
        self.del_last_name_opt_screen.input_high_opt_field.clear()
        self.main_screen.show()

    def hide_del_group_opt_screen_and_show_main_screen(self):
        self.del_group_opt_screen.hide()
        self.del_group_opt_screen.input_group_field.clear()
        self.del_group_opt_screen.input_low_opt_field.clear()
        self.del_group_opt_screen.input_high_opt_field.clear()
        self.main_screen.show()

    def hide_main_screen_and_show_tree_screen(self):
        if self.controller.open_file_name != "":
            self.main_screen.hide()
            self.tree_screen.start_printing(self.data_base, self.xml, self.controller)

    def hide_tree_screen_and_show_main_screen(self):
        self.tree_screen.hide()
        self.tree_screen.hide_main_elements()
        self.main_screen.show()
